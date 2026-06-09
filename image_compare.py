from picamera2 import Picamera2
from time import sleep
from datetime import datetime
import os
import cv2
import numpy as np

# Ordner
IMAGE_DIR = "images"
LOG_DIR = "logs"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "image_compare.log")

# Schwellwert für Alarm (wurde durch Tests festgelegt)
THRESHOLD = 10.0  # je größer, desto unempfindlicher

def log(message: str):
    """Schreibt eine Zeile mit Zeitstempel in die Logdatei und auf die Konsole."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def capture_image(picam2, prefix: str) -> str:
    """Nimmt ein Bild auf und speichert es mit Prefix (z.B. 'ref' oder 'cap')."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(IMAGE_DIR, f"{prefix}_{timestamp}.jpg")
    picam2.capture_file(filename)
    return filename

def compute_difference_score(ref_path: str, curr_path: str) -> float:
    """Berechnet eine Kennzahl für die Bilddifferenz zwischen zwei Dateien."""
    # Bilder einlesen
    ref = cv2.imread(ref_path)
    curr = cv2.imread(curr_path)

    if ref is None or curr is None:
        raise RuntimeError("Konnte eines der Bilder nicht laden.")

    # Auf gleiche Größe bringen (falls minimal unterschiedlich)
    if ref.shape != curr.shape:
        curr = cv2.resize(curr, (ref.shape[1], ref.shape[0]))

    # In Graustufen umwandeln
    ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

    # Leicht weichzeichnen, um Rauschen zu reduzieren
    ref_gray = cv2.GaussianBlur(ref_gray, (5, 5), 0)
    curr_gray = cv2.GaussianBlur(curr_gray, (5, 5), 0)

    # Absolute Differenz berechnen
    diff = cv2.absdiff(ref_gray, curr_gray)

    # Score als Mittelwert der Differenz
    score = float(np.mean(diff))
    return score

def main():
    # Kamera initialisieren
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)

    picam2.start()
    log("Kamera gestartet, warte kurz...")
    sleep(2)

    # Referenzbild aufnehmen
    log("Nehme Referenzbild auf...")
    ref_path = capture_image(picam2, "ref")
    log(f"Referenzbild gespeichert: {ref_path}")

    try:
        while True:
            log("Nehme Vergleichsbild auf...")
            curr_path = capture_image(picam2, "cap")

            # Differenz berechnen
            score = compute_difference_score(ref_path, curr_path)
            msg = f"Abweichungsscore = {score:.2f}"

            if score > THRESHOLD:
                log("ALARM: Bildabweichung über Schwellwert! " + msg)
            else:
                log("OK: Abweichung unterhalb Schwellwert. " + msg)

            # Wartezeit zwischen Messungen (in Sekunden)
            sleep(5)

    except KeyboardInterrupt:
        log("Beende Bildvergleich (Strg+C gedrückt).")
    finally:
        picam2.stop()
        log("Kamera gestoppt.")

if __name__ == "__main__":
    main()
