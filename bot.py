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

    with sync_playwright() as p:
        print("Iniciando navegador con cámara de diagnóstico...")
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        try:
            cookie_list = json.loads(raw_cookies)
            for cookie in cookie_list:
                if "expirationDate" in cookie:
                    val = cookie.pop("expirationDate")
                    if val and val > 0:
                        cookie["expires"] = int(val / 1000) if val > 9999999999 else int(val)
                if "sameSite" in cookie:
                    s_site = str(cookie["sameSite"]).capitalize()
                    cookie["sameSite"] = s_site if s_site in ["Strict", "Lax", "None"] else "Lax"
                cookie.pop("storeId", None)
                cookie.pop("session", None)
                cookie.pop("hostOnly", None)
                
            context.add_cookies(cookie_list)
            print("✅ Cookies cargadas en el sistema.")
        except Exception as e:
            print(f"❌ Error en cookies: {e}")
            browser.close()
            return
        
        page = context.new_page()
        
        print("Abriendo Facebook para validar sesión...")
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        time.sleep(5)
        
        print("Navegando al creador de Reels...")
        page.goto("https://www.facebook.com/reels/create")
        time.sleep(8)
        
        print(f"URL final en pantalla: {page.url}")
        
        # --- DIAGNÓSTICO VISUAL ---
        # El bot guardará una foto exacta de lo que ve en la pantalla
        print("📸 Tomando captura de pantalla de diagnóstico...")
        page.screenshot(path="evidencia_pantalla.png")
        print("✅ Captura guardada como 'evidencia_pantalla.png'.")
        
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
