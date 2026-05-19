import os
import time
import json
from playwright.sync_api import sync_playwright

def ejecutar_bot_facebook():
    raw_cookies = os.environ.get("FB_COOKIES")
    
    if not raw_cookies:
        print("Error: No se encontraron las cookies en los Secrets de GitHub.")
        return

    nombre_video = "IMG_7334.MOV"
    ruta_video = os.path.abspath(nombre_video)
    
    if not os.path.exists(ruta_video):
        print(f"❌ Error: No se encontró el archivo {nombre_video} en el repositorio.")
        return
    else:
        print(f"📁 Archivo multimedia listo para inyección: {ruta_video}")

    with sync_playwright() as p:
        print("Iniciando emulación nativa de dispositivo móvil...")
        # Usamos la configuración de hardware oficial de un iPhone 11/12 para emparejar las cookies
        dispositivo = p.devices["iPhone 12"]
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**dispositivo)
        
        print("Cargando y formateando cookies...")
        try:
            cookie_list = json.loads(raw_cookies)
            for cookie in cookie_list:
                if "expirationDate" in cookie:
                    val = cookie.pop("expirationDate")
                    if val and val > 0:
                        cookie["expires"] = int(val / 1000) if val > 9999999999 else int(val)
                
                if "sameSite" in cookie:
                    s_site = str(cookie["sameSite"]).capitalize()
                    if s_site in ["Strict", "Lax", "None"]:
                        cookie["sameSite"] = s_site
                    else:
                        cookie["sameSite"] = "Lax"
                
                cookie.pop("storeId", None)
                cookie.pop("session", None)
                cookie.pop("hostOnly", None)
                
            context.add_cookies(cookie_list)
            print("✅ Sesión móvil sincronizada correctamente.")
            
        except Exception as e:
            print(f"❌ Error en procesamiento de cookies: {e}")
            browser.close()
            return
        
        page = context.new_page()
        
        # Entramos directamente a la suite de publicación móvil de Facebook
        print("Abriendo creador de Reels móvil...")
        page.goto("https://m.facebook.com/reels/create", wait_until="domcontentloaded")
        time.sleep(8)
        
        print(f"URL cargada en pantalla: {page.url}")
        
        if "login" in page.url or "checkpoint" in page.url:
            print("❌ Error: Facebook rechazó el acceso. Es necesario refrescar el archivo JSON de cookies.")
            browser.close()
            return
            
        try:
            print("Analizando inputs multimedia en entorno móvil...")
            
            # En la versión móvil, Facebook suele usar inputs genéricos ocultos detrás del botón táctil.
            # Buscaremos cualquier input de tipo archivo disponible en el DOM móvil.
            formulario_subida = page.locator("input[type='file']")
            conteo_inputs = formulario_subida.count()
            print(f"Campos de subida detectados en la página: {conteo_inputs}")
            
            if conteo_inputs > 0:
                print("¡Input móvil localizado! Subiendo video de manera automatizada...")
                # Inyectamos el archivo en el primer cargador disponible
                formulario_subida.first.set_input_files(ruta_video)
                print("⏳ Archivo enviado con éxito. Esperando 25 segundos para asegurar el procesamiento en los servidores de Meta...")
                time.sleep(25)
                print("✅ Proceso de subida móvil finalizado correctamente.")
            else:
                print("⚠️ No se encontró un cargador multimedia estándar en este diseño de página.")
                
        except Exception as e:
            print(f"❌ Ocurrió un inconveniente durante el proceso de carga: {e}")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
