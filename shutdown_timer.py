import subprocess
import os
import sys
import tkinter as tk
import winreg
import json
import threading
import urllib.request
import webbrowser
import winsound
import socket
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timedelta
from math import ceil
from tkinter import filedialog, messagebox, ttk

import pystray
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageTk

CURRENT_VERSION = "1.7.3"
UPDATE_MANIFEST_URL = "https://raw.githubusercontent.com/MrDylanVERO/shutdown-timer/main/update.json"

TEXTS = {
    "italian": {
        "subtitle": "Scegli l'ora. Al resto pensa Shutdown Timer.",
        "hours": "Ora",
        "minutes": "Minuti",
        "ready": "Pronto",
        "start": "AVVIA TIMER",
        "background": "Chiudendo la finestra, l'app resta attiva nell'area di notifica.",
        "open": "Apri Shutdown Timer",
        "exit": "Esci",
        "confirm_title": "Avvia timer",
        "confirm": "Spegnere davvero il computer alle {time} ({day})?",
        "today": "oggi",
        "tomorrow": "domani",
        "invalid": "Inserisci un orario valido.",
        "running": "Timer attivo - spegnimento programmato",
        "shutdown": "Spegnimento del computer...",
        "settings": "Impostazioni",
        "choose_theme": "Scegli il tema",
        "theme_green": "Verde",
        "theme_blue": "Blu",
        "theme_purple": "Viola",
        "theme_red": "Rosso",
        "sound": "Suono di avviso",
        "sound_default": "Suono di sistema",
        "sound_none": "Nessun suono",
        "sound_info": "Informazione",
        "sound_warning": "Avviso",
        "sound_error": "Errore",
        "sound_question": "Domanda",
        "sound_custom": "Scegli file WAV",
        "test_sound": "Prova suono",
        "scheduled_notice": "Spegnimento programmato alle {time}.",
        "warning_notice": "Il computer si spegnerà tra {minutes} minuti.",
        "one_minute_notice": "Il computer si spegnerà tra un minuto.",
        "update_title": "Aggiornamento disponibile",
        "update_message": "È disponibile la versione {version}. Vuoi scaricarla ora?",
        "remote": "Telecomando Android",
        "remote_address": "Indirizzo PC: {address}:8765",
        "remote_pin": "PIN: {pin}",
        "remote_scheduled": "Spegnimento Android programmato alle {time}.",
        "background_image": "Sfondo personalizzato",
        "choose_background": "Scegli immagine",
        "remove_background": "Rimuovi sfondo",
        "timer_cancelled": "Timer annullato.",
    },
    "german": {
        "subtitle": "Wähle die Uhrzeit. Shutdown Timer erledigt den Rest.",
        "hours": "Stunde",
        "minutes": "Minuten",
        "ready": "Bereit",
        "start": "TIMER STARTEN",
        "background": "Beim Schliessen bleibt die App im Infobereich aktiv.",
        "open": "Shutdown Timer oeffnen",
        "exit": "Beenden",
        "confirm_title": "Timer starten",
        "confirm": "Computer wirklich um {time} Uhr ({day}) herunterfahren?",
        "today": "heute",
        "tomorrow": "morgen",
        "invalid": "Gib eine gueltige Uhrzeit ein.",
        "running": "Timer laeuft - Abschaltung ist geplant",
        "shutdown": "Computer wird heruntergefahren...",
        "settings": "Einstellungen",
        "choose_theme": "Design waehlen",
        "theme_green": "Gruen",
        "theme_blue": "Blau",
        "theme_purple": "Violett",
        "theme_red": "Rot",
        "sound": "Warnton",
        "sound_default": "Systemton",
        "sound_none": "Kein Ton",
        "sound_info": "Information",
        "sound_warning": "Warnung",
        "sound_error": "Fehler",
        "sound_question": "Frage",
        "sound_custom": "WAV-Datei waehlen",
        "test_sound": "Ton testen",
        "scheduled_notice": "Ausschalten um {time} Uhr geplant.",
        "warning_notice": "Der Computer wird in {minutes} Minuten ausgeschaltet.",
        "one_minute_notice": "Der Computer wird in einer Minute ausgeschaltet.",
        "update_title": "Update verfuegbar",
        "update_message": "Version {version} ist verfuegbar. Jetzt herunterladen?",
        "remote": "Android-Fernbedienung",
        "remote_address": "PC-Adresse: {address}:8765",
        "remote_pin": "PIN: {pin}",
        "remote_scheduled": "Android-Abschaltung fuer {time} Uhr geplant.",
        "background_image": "Eigenes Hintergrundbild",
        "choose_background": "Bild auswählen",
        "remove_background": "Hintergrund entfernen",
        "timer_cancelled": "Timer abgebrochen.",
    },
    "english": {
        "subtitle": "Choose the time. Shutdown Timer handles the rest.",
        "hours": "Hour",
        "minutes": "Minutes",
        "ready": "Ready",
        "start": "START TIMER",
        "background": "Closing the window keeps the app running in the system tray.",
        "open": "Open Shutdown Timer",
        "exit": "Exit",
        "confirm_title": "Start timer",
        "confirm": "Really shut down the computer at {time} ({day})?",
        "today": "today",
        "tomorrow": "tomorrow",
        "invalid": "Enter a valid time.",
        "running": "Timer running - shutdown scheduled",
        "shutdown": "Shutting down the computer...",
        "settings": "Settings",
        "choose_theme": "Choose a theme",
        "theme_green": "Green",
        "theme_blue": "Blue",
        "theme_purple": "Purple",
        "theme_red": "Red",
        "sound": "Warning sound",
        "sound_default": "System sound",
        "sound_none": "No sound",
        "sound_info": "Information",
        "sound_warning": "Warning",
        "sound_error": "Error",
        "sound_question": "Question",
        "sound_custom": "Choose WAV file",
        "test_sound": "Test sound",
        "scheduled_notice": "Shutdown scheduled for {time}.",
        "warning_notice": "The computer will shut down in {minutes} minutes.",
        "one_minute_notice": "The computer will shut down in one minute.",
        "update_title": "Update available",
        "update_message": "Version {version} is available. Download it now?",
        "remote": "Android remote control",
        "remote_address": "PC address: {address}:8765",
        "remote_pin": "PIN: {pin}",
        "remote_scheduled": "Android shutdown scheduled for {time}.",
        "background_image": "Custom background",
        "choose_background": "Choose image",
        "remove_background": "Remove background",
        "timer_cancelled": "Timer cancelled.",
    },
}

THEMES = {
    "green": {"background": "#141926", "panel": "#222a3d", "accent": "#23af5a", "active": "#1e954d"},
    "blue": {"background": "#111827", "panel": "#1e293b", "accent": "#2589e8", "active": "#1d70c1"},
    "purple": {"background": "#1b1426", "panel": "#30213f", "accent": "#9b59e6", "active": "#7d43bd"},
    "red": {"background": "#261518", "panel": "#3b2227", "accent": "#e05252", "active": "#ba4040"},
}


def resource_path(filename):
    """Find bundled assets both in Python and in a PyInstaller EXE."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, filename)


def installed_language():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
            language, _ = winreg.QueryValueEx(key, "Language")
            return language if language in TEXTS else "italian"
    except OSError:
        return "italian"


def saved_theme():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
            theme, _ = winreg.QueryValueEx(key, "Theme")
            return theme if theme in THEMES else "green"
    except OSError:
        return "green"


def save_theme(theme):
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
        winreg.SetValueEx(key, "Theme", 0, winreg.REG_SZ, theme)


def saved_sound():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
            sound, _ = winreg.QueryValueEx(key, "WarningSound")
            return sound
    except OSError:
        return "default"


def save_sound(sound):
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
        winreg.SetValueEx(key, "WarningSound", 0, winreg.REG_SZ, sound)


def saved_background():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
            path, _ = winreg.QueryValueEx(key, "BackgroundImage")
            return path if os.path.isfile(path) else ""
    except OSError:
        return ""


def save_background(path):
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
        winreg.SetValueEx(key, "BackgroundImage", 0, winreg.REG_SZ, path)


def remote_pin():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
            pin, _ = winreg.QueryValueEx(key, "RemotePin")
            if len(pin) == 6 and pin.isdigit():
                return pin
    except OSError:
        pass
    pin = f"{secrets.randbelow(1000000):06d}"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\ShutdownTimer") as key:
        winreg.SetValueEx(key, "RemotePin", 0, winreg.REG_SZ, pin)
    return pin


class ShutdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.remaining = 3600
        self.running = False
        self.tray_icon = None
        self.text = TEXTS[installed_language()]
        self.theme_name = saved_theme()
        self.theme = THEMES[self.theme_name]
        self.warning_sound = saved_sound()
        self.background_path = saved_background()
        self.background_photo = None
        self.notified_minutes = set()
        self.remote_pin = remote_pin()
        self.remote_server = None
        self.discovery_socket = None

        root.title("Shutdown Timer")
        root.geometry("520x500")
        root.resizable(False, False)
        root.configure(bg=self.theme["background"])
        self.apply_background_image()
        root.iconbitmap(resource_path("logo.ico"))
        root.protocol("WM_DELETE_WINDOW", self.keep_running_in_background)
        root.bind("<Control-Shift-X>", self.cancel_shutdown)
        root.bind("<Control-Shift-x>", self.cancel_shutdown)
        self.create_tray_icon()
        self.start_remote_server()
        self.check_for_updates()

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure(
            "Timer.TCombobox",
            fieldbackground=self.theme["panel"],
            background=self.theme["accent"],
            foreground="white",
            arrowcolor="white",
            bordercolor=self.theme["accent"],
            lightcolor=self.theme["accent"],
            darkcolor=self.theme["accent"],
            padding=8,
        )
        style.map(
            "Timer.TCombobox",
            fieldbackground=[("readonly", self.theme["panel"])],
            foreground=[("readonly", "white")],
            selectbackground=[("readonly", self.theme["panel"])],
            selectforeground=[("readonly", "white")],
        )

        self.title_photo = self.create_title_image()
        tk.Label(
            root,
            image=self.title_photo,
            borderwidth=0,
            highlightthickness=0,
            bg=self.theme["background"],
        ).pack(pady=(27, 0))

        self.settings_button = tk.Button(
            root,
            text="⚙",
            command=self.open_settings,
            font=("Segoe UI Symbol", 15),
            fg="white",
            bg=self.theme["panel"],
            activebackground=self.theme["accent"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=3,
        )
        self.settings_button.place(x=458, y=22)

        subtitle_frame = tk.Frame(
            root,
            bg=self.theme["panel"],
            highlightbackground="#20d3ee",
            highlightthickness=1,
            padx=16,
            pady=6,
        )
        subtitle_frame.pack(pady=(0, 3))
        tk.Label(
            subtitle_frame,
            text=self.text["subtitle"],
            font=("Segoe UI Semibold", 11),
            fg="#c7f3ff",
            bg=self.theme["panel"],
        ).pack()

        self.clock = tk.Label(
            root,
            text="01:00:00",
            font=("Consolas", 42, "bold"),
            fg=self.theme["accent"],
            bg=self.theme["background"],
        )
        self.clock.pack(pady=(20, 5))

        selector = tk.Frame(root, bg=self.theme["background"])
        selector.pack(pady=(5, 12))

        default_time = datetime.now() + timedelta(hours=1)
        self.hours_var = tk.StringVar(value=f"{default_time.hour:02d}")
        self.minutes_var = tk.StringVar(value=f"{default_time.minute:02d}")
        self.hours_var.trace_add("write", self.update_preview)
        self.minutes_var.trace_add("write", self.update_preview)

        hours_box = tk.Frame(selector, bg=self.theme["background"])
        hours_box.pack(side="left", padx=16)
        tk.Label(
            hours_box, text=self.text["hours"], font=("Segoe UI", 10),
            fg="#aab4c8", bg=self.theme["background"]
        ).pack()
        self.hours_spin = ttk.Combobox(
            hours_box,
            textvariable=self.hours_var,
            values=[f"{value:02d}" for value in range(24)],
            width=5,
            justify="center",
            font=("Segoe UI", 14, "bold"),
            state="readonly",
            style="Timer.TCombobox",
        )
        self.hours_spin.pack(pady=4)

        minutes_box = tk.Frame(selector, bg=self.theme["background"])
        minutes_box.pack(side="left", padx=16)
        tk.Label(
            minutes_box, text=self.text["minutes"], font=("Segoe UI", 10),
            fg="#aab4c8", bg=self.theme["background"]
        ).pack()
        self.minutes_spin = ttk.Combobox(
            minutes_box,
            textvariable=self.minutes_var,
            values=[f"{value:02d}" for value in range(60)],
            width=5,
            justify="center",
            font=("Segoe UI", 14, "bold"),
            state="readonly",
            style="Timer.TCombobox",
        )
        self.minutes_spin.pack(pady=4)

        self.status = tk.Label(
            root,
            text=self.text["ready"],
            font=("Segoe UI", 11),
            fg="#aab4c8",
            bg=self.theme["background"],
        )
        self.status.pack(pady=(0, 16))

        self.start_button = tk.Button(
            root,
            text=self.text["start"],
            command=self.start_shutdown,
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=self.theme["accent"],
            activebackground=self.theme["active"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=20,
            height=2,
        )
        self.start_button.pack()

        tk.Label(
            root,
            text=self.text["background"],
            font=("Segoe UI", 9),
            fg="#737d91",
            bg=self.theme["background"],
        ).pack(pady=18)

    def create_title_image(self):
        width, height = 430, 68
        font_path = os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"), "Fonts", "seguisb.ttf"
        )
        try:
            font = ImageFont.truetype(font_path, 36)
        except OSError:
            font = ImageFont.load_default()

        mask = Image.new("L", (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        text = "SHUTDOWN TIMER"
        box = mask_draw.textbbox((0, 0), text, font=font)
        text_width = box[2] - box[0]
        x = (width - text_width) // 2
        mask_draw.text((x, 4), text, font=font, fill=255)

        gradient = Image.new("RGBA", (width, height))
        pixels = gradient.load()
        colors = ((46, 230, 138), (32, 211, 238), (59, 130, 246))
        for px in range(width):
            position = px / max(1, width - 1)
            if position < 0.5:
                mix = position * 2
                start, end = colors[0], colors[1]
            else:
                mix = (position - 0.5) * 2
                start, end = colors[1], colors[2]
            color = tuple(int(start[i] + (end[i] - start[i]) * mix) for i in range(3))
            for py in range(height):
                pixels[px, py] = (*color, 255)

        glow_mask = mask.filter(ImageFilter.GaussianBlur(7))
        result = Image.new("RGBA", (width, height), self.theme["background"])
        glow = Image.new("RGBA", (width, height), (35, 210, 185, 135))
        empty = Image.new("RGBA", (width, height))
        result.alpha_composite(Image.composite(glow, empty, glow_mask))
        result.alpha_composite(Image.composite(gradient, empty, mask))
        line_draw = ImageDraw.Draw(result)
        line_draw.rounded_rectangle((95, 57, 335, 61), radius=2, fill=(34, 211, 238, 210))
        return ImageTk.PhotoImage(result)

    def open_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.text["settings"])
        dialog.geometry("420x640")
        dialog.resizable(False, False)
        dialog.configure(bg=self.theme["background"])
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.iconbitmap(resource_path("logo.ico"))

        tk.Label(
            dialog,
            text=self.text["choose_theme"],
            font=("Segoe UI", 17, "bold"),
            fg="white",
            bg=self.theme["background"],
        ).pack(pady=(25, 18))

        buttons = tk.Frame(dialog, bg=self.theme["background"])
        buttons.pack()
        for index, theme_name in enumerate(("green", "blue", "purple", "red")):
            theme = THEMES[theme_name]
            button = tk.Button(
                buttons,
                text=self.text[f"theme_{theme_name}"],
                command=lambda name=theme_name, window=dialog: self.select_theme(name, window),
                font=("Segoe UI", 11, "bold"),
                fg="white",
                bg=theme["accent"],
                activebackground=theme["active"],
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                width=11,
                height=2,
            )
            button.grid(row=index // 2, column=index % 2, padx=8, pady=8)

        tk.Label(
            dialog, text=self.text["sound"], font=("Segoe UI", 13, "bold"),
            fg="white", bg=self.theme["background"],
        ).pack(pady=(18, 7))
        self.sound_choices = {
            self.text["sound_default"]: "default",
            self.text["sound_info"]: "info",
            self.text["sound_warning"]: "warning",
            self.text["sound_error"]: "error",
            self.text["sound_question"]: "question",
            self.text["sound_none"]: "none",
        }
        selected_key = self.warning_sound if self.warning_sound in self.sound_choices.values() else "default"
        selected_label = next(label for label, key in self.sound_choices.items() if key == selected_key)
        self.sound_choice_var = tk.StringVar(value=selected_label)
        sound_list = ttk.Combobox(
            dialog,
            textvariable=self.sound_choice_var,
            values=list(self.sound_choices.keys()),
            state="readonly",
            width=24,
            justify="center",
            font=("Segoe UI", 10),
            style="Timer.TCombobox",
        )
        sound_list.pack(pady=4)
        sound_list.bind("<<ComboboxSelected>>", self.on_sound_selected)

        sound_buttons = tk.Frame(dialog, bg=self.theme["background"])
        sound_buttons.pack(pady=7)
        for column, (label, command) in enumerate((
            (self.text["sound_custom"], self.choose_custom_sound),
            (self.text["test_sound"], self.play_warning_sound),
        )):
            tk.Button(
                sound_buttons, text=label, command=command,
                font=("Segoe UI", 9), fg="white",
                bg=self.theme["accent"] if column == 1 else self.theme["panel"],
                activebackground=self.theme["active"], activeforeground="white",
                relief="flat", cursor="hand2", width=17,
            ).grid(row=0, column=column, padx=5)

        tk.Label(
            dialog, text=self.text["background_image"], font=("Segoe UI", 13, "bold"),
            fg="white", bg=self.theme["background"],
        ).pack(pady=(18, 7))
        background_buttons = tk.Frame(dialog, bg=self.theme["background"])
        background_buttons.pack(pady=4)
        tk.Button(
            background_buttons, text=self.text["choose_background"],
            command=lambda window=dialog: self.choose_background(window),
            font=("Segoe UI", 9), fg="white", bg=self.theme["accent"],
            activebackground=self.theme["active"], activeforeground="white",
            relief="flat", cursor="hand2", width=17,
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            background_buttons, text=self.text["remove_background"],
            command=lambda window=dialog: self.remove_background(window),
            font=("Segoe UI", 9), fg="white", bg=self.theme["panel"],
            activebackground=self.theme["active"], activeforeground="white",
            relief="flat", cursor="hand2", width=19,
        ).grid(row=0, column=1, padx=5)

        tk.Label(
            dialog, text=self.text["remote"], font=("Segoe UI", 13, "bold"),
            fg="white", bg=self.theme["background"],
        ).pack(pady=(18, 5))
        tk.Label(
            dialog,
            text=self.text["remote_address"].format(address=self.local_ip()),
            font=("Consolas", 10), fg="#aab4c8", bg=self.theme["background"],
        ).pack()
        tk.Label(
            dialog,
            text=self.text["remote_pin"].format(pin=self.remote_pin),
            font=("Consolas", 13, "bold"), fg=self.theme["accent"],
            bg=self.theme["background"],
        ).pack(pady=3)

    @staticmethod
    def local_ip():
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            connection.connect(("8.8.8.8", 80))
            address = connection.getsockname()[0]
            connection.close()
            return address
        except OSError:
            return "127.0.0.1"

    def apply_background_image(self):
        if not self.background_path:
            return
        try:
            image = Image.open(self.background_path).convert("RGB")
            image = image.resize((520, 500), Image.Resampling.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.root, image=self.background_photo, borderwidth=0)
            label.place(x=0, y=0, relwidth=1, relheight=1)
            label.lower()
        except (OSError, ValueError):
            self.background_path = ""
            save_background("")

    def choose_background(self, dialog):
        path = filedialog.askopenfilename(
            parent=dialog,
            title=self.text["choose_background"],
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")],
        )
        if path:
            save_background(path)
            dialog.destroy()
            self.restart_interface()

    def remove_background(self, dialog):
        save_background("")
        dialog.destroy()
        self.restart_interface()

    def start_remote_server(self):
        app = self

        class RemoteHandler(BaseHTTPRequestHandler):
            def send_json(self, status, payload):
                body = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                if self.path != "/schedule":
                    self.send_json(404, {"ok": False})
                    return
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    payload = json.loads(self.rfile.read(length))
                    if str(payload.get("pin", "")) != app.remote_pin:
                        self.send_json(403, {"ok": False, "error": "wrong_pin"})
                        return
                    hour = int(payload["hour"])
                    minute = int(payload["minute"])
                    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
                        raise ValueError
                    if app.running:
                        self.send_json(409, {"ok": False, "error": "timer_running"})
                        return
                    app.root.after(0, app.schedule_from_remote, hour, minute)
                    self.send_json(200, {"ok": True, "time": f"{hour:02d}:{minute:02d}"})
                except (ValueError, KeyError, json.JSONDecodeError):
                    self.send_json(400, {"ok": False, "error": "invalid_request"})

            def log_message(self, format, *args):
                return

        try:
            self.remote_server = ThreadingHTTPServer(("0.0.0.0", 8765), RemoteHandler)
            threading.Thread(target=self.remote_server.serve_forever, daemon=True).start()
            threading.Thread(target=self.discovery_loop, daemon=True).start()
        except OSError:
            self.remote_server = None

    def discovery_loop(self):
        """Let the Android app find this PC using only the six-digit PIN."""
        try:
            discovery = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            discovery.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            discovery.bind(("0.0.0.0", 8766))
            discovery.settimeout(1)
            self.discovery_socket = discovery
            expected = f"SHUTDOWN_TIMER_DISCOVER:{self.remote_pin}"
            while self.remote_server:
                try:
                    data, sender = discovery.recvfrom(1024)
                    if data.decode("utf-8", errors="ignore").strip() == expected:
                        reply = json.dumps(
                            {"service": "shutdown_timer", "port": 8765}
                        ).encode("utf-8")
                        discovery.sendto(reply, sender)
                except socket.timeout:
                    continue
                except OSError:
                    break
        except OSError:
            self.discovery_socket = None

    def stop_remote_server(self):
        if self.discovery_socket:
            self.discovery_socket.close()
            self.discovery_socket = None
        if self.remote_server:
            self.remote_server.shutdown()
            self.remote_server.server_close()
            self.remote_server = None

    def schedule_from_remote(self, hour, minute):
        self.hours_var.set(f"{hour:02d}")
        self.minutes_var.set(f"{minute:02d}")
        seconds, target, _ = self.selected_target()
        self.request_windows_shutdown(seconds)
        self.remaining = seconds
        self.running = True
        self.notified_minutes.clear()
        self.start_button.config(state="disabled", bg="#355443")
        self.settings_button.config(state="disabled")
        self.hours_spin.config(state="disabled")
        self.minutes_spin.config(state="disabled")
        self.status.config(text=self.text["running"], fg=self.theme["accent"])
        self.show_notification(
            self.text["remote_scheduled"].format(time=target.strftime("%H:%M"))
        )
        self.tick()

    @staticmethod
    def request_windows_shutdown(seconds):
        """Start the Windows shutdown command without blocking the interface."""
        shutdown_exe = os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"),
            "System32",
            "shutdown.exe",
        )
        subprocess.Popen(
            [shutdown_exe, "/s", "/t", str(seconds)],
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True,
        )

    def on_sound_selected(self, event=None):
        sound = self.sound_choices[self.sound_choice_var.get()]
        self.set_warning_sound(sound)

    def set_warning_sound(self, sound):
        self.warning_sound = sound
        save_sound(sound)
        self.play_warning_sound()

    def choose_custom_sound(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title=self.text["sound_custom"],
            filetypes=[("WAV audio", "*.wav")],
        )
        if path:
            self.warning_sound = path
            save_sound(path)
            self.play_warning_sound()

    def play_warning_sound(self):
        if self.warning_sound == "none":
            return
        try:
            if self.warning_sound == "default":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif self.warning_sound == "info":
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            elif self.warning_sound == "warning":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif self.warning_sound == "error":
                winsound.MessageBeep(winsound.MB_ICONHAND)
            elif self.warning_sound == "question":
                winsound.MessageBeep(winsound.MB_ICONQUESTION)
            elif os.path.isfile(self.warning_sound):
                winsound.PlaySound(
                    self.warning_sound,
                    winsound.SND_FILENAME | winsound.SND_ASYNC,
                )
        except RuntimeError:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    def show_notification(self, message):
        try:
            self.tray_icon.notify(message, "Shutdown Timer")
        except Exception:
            pass

    def check_for_updates(self):
        if not UPDATE_MANIFEST_URL:
            return
        threading.Thread(target=self._fetch_update, daemon=True).start()

    def _fetch_update(self):
        try:
            request = urllib.request.Request(
                UPDATE_MANIFEST_URL,
                headers={"User-Agent": "Shutdown-Timer-Updater"},
            )
            with urllib.request.urlopen(request, timeout=6) as response:
                update = json.load(response)
            latest = str(update["version"])
            download_url = str(update["download_url"])
            if self.version_tuple(latest) > self.version_tuple(CURRENT_VERSION):
                self.root.after(0, self.offer_update, latest, download_url)
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            pass

    @staticmethod
    def version_tuple(version):
        try:
            return tuple(int(part) for part in version.split("."))
        except ValueError:
            return (0,)

    def offer_update(self, version, download_url):
        self.show_notification(self.text["update_title"])
        if messagebox.askyesno(
            self.text["update_title"],
            self.text["update_message"].format(version=version),
        ):
            webbrowser.open(download_url)

    def select_theme(self, theme_name, dialog):
        self.theme_name = theme_name
        self.theme = THEMES[theme_name]
        save_theme(theme_name)
        dialog.destroy()
        messagebox.showinfo(
            self.text["settings"],
            self.text["settings"] + ": " + self.text[f"theme_{theme_name}"],
        )
        self.restart_interface()

    def restart_interface(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.stop_remote_server()
        self.root.destroy()
        new_root = tk.Tk()
        ShutdownTimerApp(new_root)
        new_root.mainloop()

    def selected_target(self):
        try:
            hour = int(self.hours_var.get())
            minute = int(self.minutes_var.get())
            if not 0 <= hour <= 23 or not 0 <= minute <= 59:
                raise ValueError

            now = datetime.now()
            target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            is_tomorrow = target <= now
            if is_tomorrow:
                target += timedelta(days=1)
            seconds = max(1, ceil((target - now).total_seconds()))
            return seconds, target, is_tomorrow
        except ValueError:
            return 0, None, False

    def update_preview(self, *args):
        if self.running or not hasattr(self, "clock"):
            return
        seconds, _, _ = self.selected_target()
        hours, rest = divmod(seconds, 3600)
        minutes, secs = divmod(rest, 60)
        self.clock.config(text=f"{hours:02d}:{minutes:02d}:{secs:02d}")

    def keep_running_in_background(self):
        """Keep the timer alive if the window is closed accidentally."""
        self.root.withdraw()

    def create_tray_icon(self):
        """Create the Windows notification-area icon and its menu."""
        image = Image.open(resource_path("logo.png")).convert("RGBA")

        menu = pystray.Menu(
            pystray.MenuItem(self.text["open"], self.show_window, default=True),
            pystray.MenuItem(self.text["exit"], self.exit_application),
        )
        self.tray_icon = pystray.Icon(
            "shutdown_timer",
            image,
            "Shutdown Timer",
            menu,
        )
        self.tray_icon.run_detached()

    def show_window(self, icon=None, item=None):
        self.root.after(0, self._restore_window)

    def _restore_window(self):
        self.root.deiconify()
        self.root.state("normal")
        self.root.lift()
        self.root.focus_force()

    def exit_application(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.stop_remote_server()
        self.root.after(0, self.root.destroy)

    def start_shutdown(self):
        if self.running:
            return

        seconds, target, is_tomorrow = self.selected_target()
        if target is None:
            messagebox.showwarning(self.text["confirm_title"], self.text["invalid"])
            return

        confirmed = messagebox.askyesno(
            self.text["confirm_title"],
            self.text["confirm"].format(
                time=target.strftime("%H:%M"),
                day=self.text["tomorrow" if is_tomorrow else "today"],
            ),
        )
        if not confirmed:
            return

        self.request_windows_shutdown(seconds)
        self.remaining = seconds
        self.running = True
        self.notified_minutes.clear()
        self.start_button.config(state="disabled", bg="#355443")
        self.settings_button.config(state="disabled")
        self.hours_spin.config(state="disabled")
        self.minutes_spin.config(state="disabled")
        self.status.config(text=self.text["running"], fg=self.theme["accent"])
        self.show_notification(
            self.text["scheduled_notice"].format(time=target.strftime("%H:%M"))
        )
        self.tick()

    def tick(self):
        if not self.running:
            return
        hours, rest = divmod(self.remaining, 3600)
        minutes, seconds = divmod(rest, 60)
        self.clock.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        minutes_left = ceil(self.remaining / 60)
        if minutes_left in (10, 5, 1) and minutes_left not in self.notified_minutes:
            self.notified_minutes.add(minutes_left)
            notice = (
                self.text["one_minute_notice"]
                if minutes_left == 1
                else self.text["warning_notice"].format(minutes=minutes_left)
            )
            self.show_notification(notice)
            self.play_warning_sound()

        if self.remaining > 0:
            self.remaining -= 1
            self.root.after(1000, self.tick)
        else:
            self.status.config(text=self.text["shutdown"])

    def cancel_shutdown(self, event=None):
        if not self.running:
            return
        shutdown_exe = os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"), "System32", "shutdown.exe"
        )
        subprocess.Popen(
            [shutdown_exe, "/a"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True,
        )
        self.running = False
        self.remaining = 0
        self.notified_minutes.clear()
        self.start_button.config(state="normal", bg=self.theme["accent"])
        self.settings_button.config(state="normal")
        self.hours_spin.config(state="readonly")
        self.minutes_spin.config(state="readonly")
        self.status.config(text=self.text["timer_cancelled"], fg="#aab4c8")
        self.update_preview()
        self.show_notification(self.text["timer_cancelled"])


if __name__ == "__main__":
    window = tk.Tk()
    ShutdownTimerApp(window)
    window.mainloop()
