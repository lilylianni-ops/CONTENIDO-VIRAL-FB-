import os
import time
import json
from playwright.sync_api import sync_playwright

def ejecutar_bot_facebook():
    raw_cookies = os.environ.get("FB_COOKIES")
    
    if not raw_cookies:
        print("Error: No se encontraron las cookies en los Secrets de GitHub.")
        return

    # Definimos el nombre exacto del archivo que subiste al repositorio
    nombre_video = "IMG_7334.MOV"
    ruta_video = os.path.abspath(nombre_video)
    
    if not os.path.exists(ruta_video):
        print(f"❌ Error: No se encontró el archivo {nombre_video} en el repositorio.")
        return
    else:
        print(f"📁 Archivo de video localizado correctamente: {ruta_video}")

    with sync_playwright() as p:
        print("Iniciando navegador emulado...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        
        print("Cargando y formateando lista de cookies...")
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
            print("✅ Sesión clonada exitosamente.")
            
        except Exception as e:
            print(f"❌ Error al procesar formato de cookies: {e}")
            browser.close()
            return
        
        page = context.new_page()
        print("Abriendo Facebook...")
        page.goto("https://www.facebook.com/")
        time.sleep(5)
        
        if "login" in page.url or "checkpoint" in page.url:
            print("❌ Error: Sesión inválida.")
            browser.close()
            return
            
        print("Navegando al creador de Reels...")
        page.goto("https://www.facebook.com/reels/create")
        time.sleep(6)
        
        try:
            print("Buscando el botón de carga de archivos de Facebook...")
            # Localizamos el input invisible donde se arrastran los archivos multimedia
            file_input = page.locator("input[type='file']")
            
            if file_input.count() > 0:
                print("¡Input de carga encontrado! Inyectando video...")
                # Forzamos la subida del archivo al navegador emulado
                file_input.first.set_input_files(ruta_video)
                print("⏳ Video enviado. Esperando 15 segundos para que cargue en Meta...")
                time.sleep(15)
                print("✅ Proceso de carga simulado completado con éxito.")
            else:
                print("⚠️ No se detectó el formulario de subida estándar. Es posible que el diseño de la página haya variado.")
                
        except Exception as e:
            print(f"❌ Ocurrió un inconveniente al interactuar con el cargador: {e}")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
