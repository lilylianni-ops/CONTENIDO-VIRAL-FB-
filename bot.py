import os
import time
import json
from playwright.sync_api import sync_playwright

def ejecutar_bot_facebook():
    raw_cookies = os.environ.get("FB_COOKIES")
    
    if not raw_cookies:
        print("Error: No se encontraron las cookies en los Secrets de GitHub.")
        return

    # Apuntamos exactamente al video que subiste a tu raíz
    nombre_video = "IMG_7334.MOV"
    ruta_video = os.path.abspath(nombre_video)
    
    if not os.path.exists(ruta_video):
        print(f"❌ Error: No se encontró el archivo {nombre_video} en el repositorio.")
        return
    else:
        print(f"📁 Archivo de video localizado correctamente en: {ruta_video}")

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
        
        print("Navegando directo al creador de Reels...")
        page.goto("https://www.facebook.com/reels/create")
        time.sleep(7)
        
        try:
            print("Iniciando carga del archivo multimedia...")
            # Evento nativo para subir archivos sin importar el diseño visual de la página
            with page.expect_file_chooser() as fc_info:
                # Buscamos cualquier elemento interactivo que sirva para subir contenido
                page.locator("input[type='file']").first.click(timeout=5000)
            
            file_chooser = fc_info.value
            file_chooser.set_files(ruta_video)
            
            print("⏳ Video inyectado en el sistema. Esperando 25 segundos para el procesamiento de Meta...")
            time.sleep(25)
            print("✅ El video ha sido cargado exitosamente en el panel.")
            
        except Exception as e:
            print(f"⚠️ Nota de carga: Se intentará un método alternativo por selector directo.")
            try:
                page.locator("input[type='file']").first.set_input_files(ruta_video)
                print("⏳ Procesando carga alternativa... Esperando 25 segundos.")
                time.sleep(25)
                print("✅ Video cargado por método alternativo.")
            except Exception as err:
                print(f"❌ No se pudo completar la carga multimedia: {err}")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
