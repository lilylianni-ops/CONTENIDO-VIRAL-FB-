import os
import time
from playwright.sync_api import sync_playwright

def login_facebook():
    # Recuperar credenciales ocultas de los Secrets de GitHub
    email = os.environ.get("FB_EMAIL")
    password = os.environ.get("FB_PASSWORD")
    
    if not email or not password:
        print("Error: Credenciales no configuradas en los Secrets.")
        return

    with sync_playwright() as p:
        # Iniciamos el navegador en modo "headless" (sin interfaz gráfica)
        browser = p.chromium.launch(headless=True)
        # Usamos un User-Agent común para simular un navegador real
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Abriendo Facebook...")
        page.goto("https://www.facebook.com")
        time.sleep(2)
        
        # Llenar el formulario de inicio de sesión
        print("Introduciendo credenciales...")
        page.fill('input[name="email"]', email)
        page.fill('input[name="pass"]', password)
        
        # Hacer clic en el botón de entrar
        page.click('button[name="login"]')
        print("Iniciando sesión...")
        time.sleep(5)  # Esperar a que cargue la página de inicio
        
        # Verificar si el inicio de sesión fue exitoso buscando elementos comunes
        if "checkpoint" in page.url:
            print("Alerta: Facebook solicita verificación de seguridad (2FA o captcha).")
        elif page.locator('a[aria-label="Facebook"]').is_visible() or "home" in page.url:
            print("¡Inicio de sesión exitoso!")
            # Aquí irá más adelante la lógica para subir el Reel
        else:
            print(f"Estado indeterminado. URL actual: {page.url}")
            
        browser.close()

if __name__ == "__main__":
    login_facebook()
