# Raspberry Pi Display Image Compare

Bildvergleichssystem auf Basis eines Raspberry Pi 5 und eines Raspberry Pi Camera Module 3.  
Der Raspberry Pi nimmt ein Referenzbild eines Fahrzeug-Displays auf und vergleicht anschließend fortlaufend neue Bilder mit diesem Referenzbild.  
Aus den Unterschieden wird ein Score berechnet. Wird ein konfigurierter Schwellwert überschritten, meldet das System einen **ALARM**, ansonsten **OK**.

Dieses Projekt wird am Prüfplatz eingesetzt, um visuelle Änderungen auf Infotainment-/Kombi-Displays zu detektieren und die vom TestRack angestoßenen Funktionen bildseitig zu verifizieren.

---

## Funktionsumfang

- Aufnahme eines **Referenzbildes** beim Start
- Zyklische Aufnahme von **Vergleichsbildern**
- Bildvergleich Referenzbild ↔ aktuelles Bild mit OpenCV
- Berechnung eines Abweichungs-Scores pro Bildpaar
- Entscheidung:
  - `OK` – Abweichung unterhalb Schwellwert  
  - `ALARM` – Abweichung oberhalb Schwellwert
- Logging aller Ereignisse (Start, Stop, OK/ALARM, Score) in eine Logdatei
- Ablage der aufgenommenen Bilder in einem Projektordner

---

## Hardware

Getestete Konfiguration:

- **Raspberry Pi 5** (16 GB)
- **Raspberry Pi Camera Module 3**
- Netzteil, SD-Karte
- Monitor, Tastatur, Maus für Setup
- Fahrzeug-Display als Prüfobjekt (z. B. Navi, Kombiinstrument, Infotainment),
  typischerweise per **LVDS** angebunden (nur zur Info, LVDS wird nicht direkt ausgewertet).

Die Kamera wird mechanisch in einer **stabilen Halterung** vor dem Display positioniert.  
Die Halterung sollte so ausgelegt sein, dass sich der Bildausschnitt während der Messung nicht verändert.

---

## Verwendete Software / Bibliotheken

Auf dem Raspberry Pi:

- **Raspberry Pi OS** (64‑bit, aktueller Stand)
- **Python 3** (z. B. Python 3.13.x)
- Python-Bibliotheken:
  - `picamera2` – Zugriff auf die Kamera über libcamera
  - `opencv-python` (`cv2`) – Bildverarbeitung
  - `numpy` – numerische Operationen (wird von OpenCV genutzt)
- Kamera-Tools:
  - `rpicam-hello`, `rpicam-still` – Funktionstest der Kamera (Nachfolger von `libcamera-hello`/`libcamera-still`)

---

## Installation auf dem Raspberry Pi

### 1. System aktualisieren

```bash
sudo apt update
sudo apt full-upgrade -y
