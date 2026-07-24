SHUTDOWN TIMER
==============

Start:
  Doppelklick auf "Shutdown-Timer-starten.bat"

Das Programm wurde mit Python erstellt.
Der gruene Knopf plant die Abschaltung nach 60 Minuten.
In der App gibt es keine Abbrechen-Funktion.

Wichtig:
Wenn du das Fenster mit X schliesst, verschwindet es in den Infobereich
(System Tray) neben der Windows-Uhr. Das Programm und der Countdown bleiben
im Hintergrund aktiv. Ein Doppelklick auf das gruene Symbol oeffnet das
Fenster wieder. Mit Rechtsklick erreichst du das Menue.

Abhaengigkeiten installieren:
  python -m pip install -r requirements.txt

EXE erstellen:
  python -m PyInstaller --onefile --windowed --name Shutdown-Timer --icon logo.ico --add-data "logo.png;." --add-data "logo.ico;." shutdown_timer.py
