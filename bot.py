import os
import time
import json
from playwright.sync_api import sync_playwright

def ejecutar_bot_facebook():
    raw_cookies = os.environ.get("FB_COOKIES")
    
    # Configuración de Proxy Residencial
    # Reemplaza con los datos reales de tu proveedor de proxy si deseas activarlo
    PROXY_SERVER = "http://tu_proxy_residencial:puerto" 
    PROXY_USER = "tu_usuario"
    PROXY_PASS = "tu_contraseña"
    
    if not raw_cookies:
        print("Error: No se encontraron las cookies en los Secrets de GitHub.")
        return

    nombre_video = "IMG_7334.MOV"
    ruta_video = os.path.abspath(nombre_video)

    with sync_playwright() as p:
        print("Iniciando navegador emulado con túnel de red...")
        
        # Parámetros de lanzamiento del navegador
        launch_args = ["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        
        # Estructura de proxy para Playwright
        proxy_config = {
            "server": PROXY_SERVER,
            "username": PROXY_USER,
            "password": PROXY_PASS
        } if PROXY_SERVER and "tu_proxy" not in PROXY_SERVER else None

        browser = p.chromium.launch(
            headless=True, 
            args=launch_args,
            proxy=proxy_config
        )
        
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
            print("✅ Parámetros de sesión inyectados en el contexto.")
        except Exception as e:
            print(f"❌ Error al procesar cookies: {e}")
            browser.close()
            return
        
        page = context.new_page()
        
        print("Validando respuesta de red en Facebook...")
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        time.sleep(5)
        
        print("Navegando a la sección de destino...")
        page.goto("https://www.facebook.com/reels/create")
        time.sleep(8)
        
        print(f"URL de respuesta obtenida: {page.url}")
        
        print("📸 Registrando diagnóstico visual de la vista actual...")
        page.screenshot(path="evidencia_pantalla.png")
        print("✅ Diagnóstico guardado.")
        
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
