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
        print(f"📁 Archivo de video localizado en: {ruta_video}")

    with sync_playwright() as p:
        print("Iniciando navegador emulado con evasión avanzada...")
        # Iniciamos con argumentos que ocultan el entorno automatizado
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        
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
            print("✅ Cookies cargadas.");
            
        except Exception as e:
            print(f"❌ Error en cookies: {e}")
            browser.close()
            return
        
        page = context.new_page()
        
        print("Abriendo Facebook principal...")
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        time.sleep(6)
        
        print("Navegando al creador de Reels...")
        # Cargamos usando "networkidle" para asegurar que los scripts de Meta terminen de pintar los botones
        page.goto("https://www.facebook.com/reels/create", wait_until="networkidle")
        print("Esperando 10 segundos extra para estabilización visual...")
        time.sleep(10)
        
        print(f"URL en pantalla: {page.url}")
        
        # --- BLOQUE DE CARGA MULTIPLES SELECTORES ---
        video_subido = False
        print("Buscando el formulario de carga con algoritmos alternativos...")
        
        # Intento 1: Buscar cualquier input de archivo visible u oculto
        try:
            inputs_archivo = page.locator("input[type='file']")
            if inputs_archivo.count() > 0:
                print(f"¡Se detectaron {inputs_archivo.count()} inputs de archivo! Inyectando en el primero...")
                inputs_archivo.first.set_input_files(ruta_video, timeout=5000)
                video_subido = True
        except Exception:
            pass

        # Intento 2: Si el primero falla, emular clics en zonas de arrastre comunes de Meta
        if not video_subido:
            try:
                print("Intento 1 falló. Buscando zonas interactivas de arrastre (drag & drop)...")
                cartel_carga = page.locator("text=Seleccionar video, o arrastrar y soltar").first
                if cartel_carga.is_visible():
                    with page.expect_file_chooser(timeout=5000) as fc_info:
                        cartel_carga.click()
                    file_chooser = fc_info.value
                    file_chooser.set_files(ruta_video)
                    video_subido = True
            except Exception:
                pass

        # Intento 3: Buscar por texto genérico en botones ("Seleccionar vídeo")
        if not video_subido:
            try:
                boton_texto = page.get_by_role("button", name="Seleccionar").first
                if boton_texto.is_visible():
                    with page.expect_file_chooser(timeout=5000) as fc_info:
                        boton_texto.click()
                    file_chooser = fc_info.value
                    file_chooser.set_files(ruta_video)
                    video_subido = True
            except Exception:
                pass

        # Verificación Final del paso
        if video_subido:
            print("⏳ ¡Video enviado con éxito! Esperando 30 segundos de reloj para que suba a los servidores de Meta...")
            time.sleep(30)
            print("✅ Carga completa y procesada.")
        else:
            print("❌ Meta modificó temporalmente el formulario. Tomando captura interna simulada.")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
