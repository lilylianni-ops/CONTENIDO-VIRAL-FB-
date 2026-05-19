import os
import time
import json
from playwright.sync_api import sync_playwright

def ejecutar_bot_facebook():
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
            cookie_list = json.loads(raw_cookies)
            
            for cookie in cookie_list:
                # CORRECCIÓN DE EXPIRACIÓN: Convertir milisegundos de iOS a segundos de Unix
                if "expirationDate" in cookie:
                    val = cookie.pop("expirationDate")
                    if val and val > 0:
                        # Si tiene 13 dígitos o más, viene en milisegundos y lo dividimos por 1000
                        cookie["expires"] = int(val / 1000) if val > 9999999999 else int(val)
                
                # Adaptación estricta de SameSite para Playwright
                if "sameSite" in cookie:
                    s_site = str(cookie["sameSite"]).capitalize()
                    if s_site in ["Strict", "Lax", "None"]:
                        cookie["sameSite"] = s_site
                    else:
                        cookie["sameSite"] = "Lax"
                
                # Limpieza de parámetros incompatibles
                cookie.pop("storeId", None)
                cookie.pop("session", None)
                cookie.pop("hostOnly", None)
                
            context.add_cookies(cookie_list)
            print("✅ Sesión clonada y adaptada exitosamente en el navegador.")
            
        except Exception as e:
            print(f"❌ Error al procesar el formato de las cookies: {e}")
            browser.close()
            return
        
        page = context.new_page()
        print("Abriendo Facebook con la sesión activa...")
        page.goto("https://www.facebook.com/")
        time.sleep(5)
        
        if "login" in page.url or "checkpoint" in page.url:
            print("❌ Error: Facebook invalidó la sesión o las cookies no tienen los permisos correctos.")
        else:
            print(f"¡Inicio de sesión exitoso! Título de la página: {page.title()}")
            
            print("Navegando de forma directa al creador de Reels...")
            page.goto("https://www.facebook.com/reels/create")
            time.sleep(5)
            print("¡Entorno verificado y listo para la carga automática de contenidos!")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
