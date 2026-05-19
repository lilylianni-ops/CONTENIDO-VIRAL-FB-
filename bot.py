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
        print(f"📁 Archivo de video localizado correctamente: {ruta_video}")

    with sync_playwright() as p:
        print("Iniciando navegador emulado...")
        browser = p.chromium.launch(headless=True)
        
        # FORZADO DE ESCRITORIO: Configuramos una resolución amplia y un User Agent de PC fija
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
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
        
        # Abrimos primero la página principal para asentar la sesión de escritorio
        print("Abriendo Facebook versión Escritorio...")
        page.goto("https://www.facebook.com/?theme=desktop", wait_until="networkidle")
        time.sleep(5)
        
        if "login" in page.url or "checkpoint" in page.url:
            print("❌ Error: Sesión inválida.")
            browser.close()
            return
            
        print("Navegando de forma directa al creador de Reels de escritorio...")
        page.goto("https://www.facebook.com/reels/create", wait_until="networkidle")
        time.sleep(8)
        
        print(f"URL actual cargada en el servidor: {page.url}")
        
        try:
            print("Buscando el formulario de carga...")
            # Selector flexible diseñado para capturar el input de subida de video en la versión PC
            file_input = page.locator("input[type='file'][accept*='video']")
            
            if file_input.count() == 0:
                # Si falla el específico, intentamos con el genérico de archivos
                file_input = page.locator("input[type='file']")
                
            if file_input.count() > 0:
                print("¡Input de carga detectado con éxito! Subiendo archivo multimedia...")
                file_input.first.set_input_files(ruta_video)
                print("⏳ Archivo enviado a la interfaz de Meta. Esperando 20 segundos para procesamiento...")
                time.sleep(20)
                print("✅ Video cargado en el formulario. Listo para la fase de textos.")
            else:
                print("⚠️ No se logró detectar el input de carga en esta vista. Analizando estructura...")
                # Tomamos nota del HTML de los inputs disponibles para mapear si Meta cambió algo interno
                inputs = page.locator("input").all_meta_info if hasattr(page.locator("input"), 'all_meta_info') else "No accesible"
                print(f"Estructura detectada: Se encontraron {page.locator('input').count()} campos de entrada.")
                
        except Exception as e:
            print(f"❌ Ocurrió un inconveniente al interactuar con el cargador: {e}")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
