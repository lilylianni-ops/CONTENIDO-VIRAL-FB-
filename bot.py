import os
import time
import json
from playwright.sync_api import sync_playwright

def ejecutar_bot_facebook():
    # Recuperamos el texto de las cookies desde los Secrets de GitHub
    raw_cookies = os.environ.get("FB_COOKIES")
    
    if not raw_cookies:
        print("Error: No se encontraron las cookies en los Secrets de GitHub.")
        return

    with sync_playwright() as p:
        print("Iniciando navegador emulado...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        
        print("Cargando y formateando lista de cookies del iPhone...")
        try:
            # Convertimos el texto JSON guardado en una lista real de Python
            cookie_list = json.loads(raw_cookies)
            
            # Limpiamos campos innecesarios que Playwright no utiliza para evitar conflictos
            for cookie in cookie_list:
                if "expirationDate" in cookie:
                    cookie["expires"] = int(cookie.pop("expirationDate"))
                # Removemos valores nulos o incompatibles
                cookie.pop("storeId", None)
                cookie.pop("session", None)
                cookie.pop("hostOnly", None)
                
            # Inyectamos las cookies directamente en el contexto del navegador emulado
            context.add_cookies(cookie_list)
            print("✅ Sesión clonada exitosamente en el navegador.")
            
        except Exception as e:
            print(f"❌ Error al procesar el formato de las cookies: {e}")
            browser.close()
            return
        
        page = context.new_page()
        print("Abriendo Facebook con la sesión activa...")
        page.goto("https://www.facebook.com/")
        time.sleep(5)
        
        # Comprobamos si la sesión pegó correctamente evaluando la URL actual
        if "login" in page.url or "checkpoint" in page.url:
            print("❌ Error: Facebook invalidó la sesión. Es posible que requieras renovar las cookies.")
        else:
            print(f"¡Inicio de sesión exitoso! Título de la página: {page.title()}")
            
            print("Navegando de forma directa al creador de Reels...")
            page.goto("https://www.facebook.com/reels/create")
            time.sleep(5)
            print("¡Entorno verificado y listo para la carga automática de contenidos!")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
