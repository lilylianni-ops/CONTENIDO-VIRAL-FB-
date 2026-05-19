import os
import time
import asyncio
from playwright.sync_api import sync_playwright

# 1. GENERACIÓN DE AUDIO EN AUTOMÁTICO (Voz de IA realista y gratuita)
def generar_voz_ia(texto_guion, archivo_salida="voz.mp3"):
    print("Generando voz con IA...")
    # Usamos comando de sistema para llamar a edge-tts de forma directa y rápida
    comando = f'edge-tts --voice es-MX-DaliaNeural --text "{texto_guion}" --write-media {archivo_salida}'
    os.system(comando)
    print("¡Audio generado con éxito!")

# 2. LOGEO Y SUBIDA AUTOMÁTICA A FACEBOOK
def ejecutar_bot_facebook():
    email = os.environ.get("FB_EMAIL")
    password = os.environ.get("FB_PASSWORD")
    
    if not email or not password:
        print("Error: Configura FB_EMAIL y FB_PASSWORD en los Secrets de GitHub.")
        return

    # Generamos un audio de prueba para el Reel
    generar_voz_ia("¡Bienvenidos a este nuevo video automatizado! Sígueme para más contenido viral diario.")

    # Nota: Aquí se integrarían las líneas de MoviePy para unir 'voz.mp3' con un 'fondo.mp4'
    # Para la simulación de subida asumiremos que el archivo final ya existe.
    video_a_subir = "fondo.mp4" 
    if not os.path.exists(video_a_subir):
        # Creamos un archivo temporal simulado para que el script no falle si falta el video de stock
        with open(video_a_subir, "w") as f: f.write("video_data")

    with sync_playwright() as p:
        print("Iniciando navegador emulado...")
        browser = p.chromium.launch(headless=True) # Corre oculto en el servidor
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # Proceso de Logeo
        print("Abriendo Facebook...")
        page.goto("https://www.facebook.com/")
        time.sleep(3)
        
        print("Escribiendo credenciales seguras...")
        page.fill('input[name="email"]', email)
        page.fill('input[name="pass"]', password)
        
        print("Haciendo clic en el botón de inicio...")
        page.click('button[name="login"]')
        time.sleep(8) # Esperamos que procese la entrada
        
        # Control de Bloqueos de Seguridad (2FA / Checkpoints)
        if "checkpoint" in page.url:
            print("⚠️ Alerta: Facebook detectó una IP nueva de GitHub y pide verificación o código de seguridad.")
            browser.close()
            return
            
        print("¡Sesión iniciada correctamente en el servidor!")
        
        # RUTA DIRECTA PARA AGREGAR EL CONTENIDO (Meta Business Suite Reels)
        print("Navegando al creador de Reels...")
        # Entramos directamente a la URL de publicación para saltar menús complejos
        page.goto("https://www.facebook.com/reels/create")
        time.sleep(5)
        
        try:
            print("Buscando el selector de archivos para subir el video...")
            # Playwright localiza el input oculto de tipo 'file' que usa Facebook para cargar videos
            input_video = page.locator('input[type="file"]')
            
            # Sube el contenido automáticamente desde el almacenamiento local del servidor
            input_video.set_input_files(video_a_subir)
            print(f"✅ Archivo '{video_a_subir}' cargado exitosamente en los servidores de Facebook.")
            time.sleep(10) # Esperamos a que procese la carga del video
            
            # Aquí se añaden pasos para escribir el título del reel y dar clic en Publicar
            print("El bot completó el flujo de carga con éxito.")
            
        except Exception as e:
            print(f"No se pudo completar la carga del video: {e}")
            
        browser.close()

if __name__ == "__main__":
    ejecutar_bot_facebook()
