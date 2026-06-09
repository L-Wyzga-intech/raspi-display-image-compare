from picamera2 import Picamera2
from time import sleep
from datetime import datetime
import os

# Ordner für Bilder
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def main():
    # Kamera initialisieren
    picam2 = Picamera2()

    # Konfiguration für ein einfaches Standbild
    config = picam2.create_still_configuration()
    picam2.configure(config)

    picam2.start()
    print("Kamera gestartet, warte kurz...")
    sleep(2)  # Kamera „warmlaufen“ lassen

    # Dateiname mit Zeitstempel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(IMAGE_DIR, f"test_capture_{timestamp}.jpg")

    print(f"Nehme Bild auf: {filename}")
    picam2.capture_file(filename)

    picam2.stop()
    print("Fertig. Bild wurde gespeichert.")

if __name__ == "__main__":
    main()
