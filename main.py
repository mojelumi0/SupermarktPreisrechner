#  Hey danke das du mein "Programm" heruntergeladen hast. Hoffe es gefällt dir.
#  
#  
#  Coded by mojelumi (~ mojelumi0)

# -----------------------------------------------------------------------------------------------------------------------------

# Hey, thanks for downloading my "program". Hope you like it.
# 
#
# Coded by mojelumi (~ mojelumi0)

import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET
import locale
import json
import os

locale.setlocale(locale.LC_NUMERIC, "")

# ---- Config-Funktionen (Laden / Speichern) ----
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
        # Standardwerte falls nicht vorhanden
        config.setdefault("history_file", "history.xml")
        config.setdefault("max_history", 5)
        config.setdefault("deduction_amount", 0.05)
        config.setdefault("fullscreen_mode", False)
        config.setdefault("history_enabled", True)
        config.setdefault("theme", "light")
        return config
    else:
        return {
            "history_file": "history.xml",
            "max_history": 5,
            "deduction_amount": 0.05,
            "fullscreen_mode": False,
            "history_enabled": True,
            "theme": "light"
        }

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

# ---- Übersetzungen ----
texts = {
    "de": {
        "title": "Supermarkt Preisrechner",
        "input_label": "Gib eine Zahl ein:",
        "calculate": "Berechnen",
        "result": "Ergebnis: {}",
        "error": "Bitte eine gültige Zahl eingeben!",
        "history_disabled": "Historie ist deaktiviert.",
        "language": "Sprache:",
        "settings_title": "Einstellungen",
        "history_file": "Historie Datei",
        "max_history": "Maximale Historie",
        "deduction_amount": "Abzugsbetrag",
        "theme": "Thema",
        "theme_option_light": "light",
        "theme_option_dark": "dark",
        "fullscreen_mode": "Vollbildmodus",
        "history_enabled": "Historie aktiviert",
        "save": "Speichern",
        "cancel": "Abbrechen",
        "debug_menu": "Debug",
        "show_debug_info": "Debug-Informationen anzeigen",
        "close": "Schließen"
    },
    "en": {
        "title": "Supermarket Price Calculator",
        "input_label": "Enter a number:",
        "calculate": "Calculate",
        "result": "Result: {}",
        "error": "Please enter a valid number!",
        "history_disabled": "History is disabled.",
        "language": "Language:",
        "settings_title": "Settings",
        "history_file": "History File",
        "max_history": "Max History",
        "deduction_amount": "Deduction Amount",
        "theme": "Theme",
        "theme_option_light": "light",
        "theme_option_dark": "dark",
        "fullscreen_mode": "Fullscreen Mode",
        "history_enabled": "History Enabled",
        "save": "Save",
        "cancel": "Cancel",
        "debug_menu": "Debug",
        "show_debug_info": "Show Debug Info",
        "close": "Close"
    }
}

# ---- Settings-Fenster ----
class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, current_settings, language, on_save_callback):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.on_save_callback = on_save_callback
        self.language = language
        self.title(texts[self.language]["settings_title"])
        
        row = 0
        # History-Datei
        ttk.Label(self, text=texts[self.language]["history_file"]).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.history_file_var = tk.StringVar(value=current_settings["history_file"])
        ttk.Entry(self, textvariable=self.history_file_var).grid(row=row, column=1, padx=10, pady=5)
        
        # Maximale Historie
        row += 1
        ttk.Label(self, text=texts[self.language]["max_history"]).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.max_history_var = tk.IntVar(value=current_settings["max_history"])
        ttk.Spinbox(self, from_=1, to=100, textvariable=self.max_history_var, width=5).grid(row=row, column=1, padx=10, pady=5, sticky="w")
        
        # Abzugsbetrag
        row += 1
        ttk.Label(self, text=texts[self.language]["deduction_amount"]).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.deduction_amount_var = tk.DoubleVar(value=current_settings["deduction_amount"])
        ttk.Entry(self, textvariable=self.deduction_amount_var).grid(row=row, column=1, padx=10, pady=5)
        
        # Theme (Light / Dark)
        row += 1
        ttk.Label(self, text=texts[self.language]["theme"]).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.theme_var = tk.StringVar(value=current_settings.get("theme", "light"))
        theme_options = [texts[self.language]["theme_option_light"], texts[self.language]["theme_option_dark"]]
        self.theme_menu = ttk.OptionMenu(self, self.theme_var, current_settings.get("theme", "light"), *theme_options)
        self.theme_menu.grid(row=row, column=1, padx=10, pady=5)
        
        # Vollbildmodus
        row += 1
        self.fullscreen_mode_var = tk.BooleanVar(value=current_settings["fullscreen_mode"])
        ttk.Checkbutton(self, text=texts[self.language]["fullscreen_mode"], variable=self.fullscreen_mode_var).grid(row=row, column=0, padx=10, pady=5, columnspan=2, sticky="w")
        
        # Historie aktiviert
        row += 1
        self.history_enabled_var = tk.BooleanVar(value=current_settings["history_enabled"])
        ttk.Checkbutton(self, text=texts[self.language]["history_enabled"], variable=self.history_enabled_var).grid(row=row, column=0, padx=10, pady=5, columnspan=2, sticky="w")
        
        # Buttons: Speichern und Abbrechen
        row += 1
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
        save_btn = ttk.Button(btn_frame, text=texts[self.language]["save"], command=self.save_settings)
        save_btn.pack(side="left", padx=5)
        cancel_btn = ttk.Button(btn_frame, text=texts[self.language]["cancel"], command=self.destroy)
        cancel_btn.pack(side="left", padx=5)
    
    def save_settings(self):
        new_settings = {
            "history_file": self.history_file_var.get(),
            "max_history": self.max_history_var.get(),
            "deduction_amount": self.deduction_amount_var.get(),
            "theme": self.theme_var.get(),
            "fullscreen_mode": self.fullscreen_mode_var.get(),
            "history_enabled": self.history_enabled_var.get()
        }
        self.on_save_callback(new_settings)
        self.destroy()

# ---- Hauptanwendung ----
class PriceCalculatorApp:
    def __init__(self, master):
        self.master = master
        self.settings = load_config()
        self.language = "de"
        self.master.title(texts[self.language]["title"])
        
        if self.settings["fullscreen_mode"]:
            self.master.attributes("-fullscreen", True)
        else:
            self.master.geometry("800x600")
        
        self.style = ttk.Style()
        # Standardtheme setzen (wird in apply_theme() überschrieben)
        self.style.theme_use("clam")
        
        self.main_frame = ttk.Frame(master, padding=20)
        self.main_frame.pack(expand=True, fill='both')
        
        self.create_menu()
        self.create_widgets()
        
        self.master.bind("<Escape>", lambda event: self.master.quit())
        self.update_history()
        self.apply_theme()
    
    def create_menu(self):
        # Menüleiste mit Debug-Menü
        self.menu_bar = tk.Menu(self.master)
        debug_menu = tk.Menu(self.menu_bar, tearoff=0)
        debug_menu.add_command(label=texts[self.language]["show_debug_info"], command=self.open_debug_menu)
        self.menu_bar.add_cascade(label=texts[self.language]["debug_menu"], menu=debug_menu)
        self.master.config(menu=self.menu_bar)
    
    def update_menu(self):
        # Aktualisiert die Menüleiste (z.B. bei Sprachwechsel)
        self.menu_bar.delete(0, 'end')
        debug_menu = tk.Menu(self.menu_bar, tearoff=0)
        debug_menu.add_command(label=texts[self.language]["show_debug_info"], command=self.open_debug_menu)
        self.menu_bar.add_cascade(label=texts[self.language]["debug_menu"], menu=debug_menu)
        self.master.config(menu=self.menu_bar)
    
    def create_widgets(self):
        # Oberer Frame: Sprachwahl links, Settings-Button rechts
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Sprachwahl
        lang_frame = ttk.Frame(top_frame)
        lang_frame.pack(side="left")
        ttk.Label(lang_frame, text=texts[self.language]["language"]).pack(side="left", padx=(0, 5))
        self.language_var = tk.StringVar(value=self.language)
        lang_menu = ttk.OptionMenu(lang_frame, self.language_var, self.language, "de", "en", command=self.set_language)
        lang_menu.pack(side="left")
        
        # Settings-Button (rechts oben)
        self.settings_btn = ttk.Button(top_frame, text=texts[self.language]["settings_title"], command=self.open_settings)
        self.settings_btn.pack(side="right")
        
        # Eingabefeld
        self.input_label = ttk.Label(self.main_frame, text=texts[self.language]["input_label"], font=("Arial", 16))
        self.input_label.pack(pady=10)
        self.input_entry = ttk.Entry(self.main_frame, font=("Arial", 14), justify="center")
        self.input_entry.pack(pady=5, ipadx=5, ipady=5)
        self.input_entry.bind("<Return>", self.calculate_price)
        
        # Berechnen-Button
        self.calculate_button = ttk.Button(self.main_frame, text=texts[self.language]["calculate"], command=self.calculate_price)
        self.calculate_button.pack(pady=10)
        
        # Ergebnisanzeige
        self.result_label = ttk.Label(self.main_frame, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)
        
        # Historieanzeige
        self.history_label = ttk.Label(self.main_frame, text="", font=("Arial", 12), justify="left")
        self.history_label.pack(pady=10)
    
    def set_language(self, new_language):
        self.language = new_language
        self.master.title(texts[self.language]["title"])
        self.input_label.config(text=texts[self.language]["input_label"])
        self.calculate_button.config(text=texts[self.language]["calculate"])
        self.settings_btn.config(text=texts[self.language]["settings_title"])
        self.update_menu()
        self.update_history()
    
    def open_settings(self):
        SettingsWindow(self.master, self.settings, self.language, self.update_settings)
    
    def update_settings(self, new_settings):
        self.settings = new_settings
        save_config(self.settings)
        if self.settings["fullscreen_mode"]:
            self.master.attributes("-fullscreen", True)
        else:
            self.master.attributes("-fullscreen", False)
            self.master.geometry("800x600")
        self.update_history()
        self.apply_theme()
    
    def apply_theme(self):
        # Wendet Dark/Light Theme an
        if self.settings.get("theme", "light") == "dark":
            dark_bg = "#2e2e2e"
            dark_fg = "#ffffff"
            self.master.configure(bg=dark_bg)
            self.main_frame.configure(style="Dark.TFrame")
            self.style.configure("Dark.TFrame", background=dark_bg)
            self.style.configure("Dark.TLabel", background=dark_bg, foreground=dark_fg)
            self.style.configure("Dark.TButton", background="#444444", foreground=dark_fg)
            # Aktualisiere alle Widgets im main_frame (sofern möglich)
            for child in self.main_frame.winfo_children():
                if isinstance(child, ttk.Label):
                    child.configure(style="Dark.TLabel")
                elif isinstance(child, ttk.Button):
                    child.configure(style="Dark.TButton")
        else:
            light_bg = "#f0f0f0"
            light_fg = "#000000"
            self.master.configure(bg=light_bg)
            self.main_frame.configure(style="TFrame")
            self.style.configure("TFrame", background=light_bg)
            self.style.configure("TLabel", background=light_bg, foreground=light_fg)
            self.style.configure("TButton", background="#e0e0e0", foreground=light_fg)
            for child in self.main_frame.winfo_children():
                if isinstance(child, ttk.Label):
                    child.configure(style="TLabel")
                elif isinstance(child, ttk.Button):
                    child.configure(style="TButton")
    
    def save_history(self, value):
        if not self.settings["history_enabled"]:
            return
        try:
            tree = ET.parse(self.settings["history_file"])
            root = tree.getroot()
        except (ET.ParseError, FileNotFoundError):
            root = ET.Element("history")
        formatted_value = f"{value:.2f}"
        ET.SubElement(root, "entry").text = formatted_value
        while len(root) > self.settings["max_history"]:
            root.remove(root[0])
        tree = ET.ElementTree(root)
        tree.write(self.settings["history_file"])
        self.update_history()
    
    def calculate_price(self, event=None):
        try:
            input_text = self.input_entry.get().replace(",", ".")
            number = float(input_text)
            result = (number * 2) - self.settings["deduction_amount"]
            # Ergebnis auf 2 Dezimalstellen gerundet anzeigen
            self.result_label.config(text=texts[self.language]["result"].format(f"{result:.2f}"))
            self.save_history(result)
        except ValueError:
            self.result_label.config(text=texts[self.language]["error"])
    
    def update_history(self):
        if not self.settings["history_enabled"]:
            self.history_label.config(text=texts[self.language]["history_disabled"])
            return
        try:
            tree = ET.parse(self.settings["history_file"])
            root = tree.getroot()
            entries = [entry.text for entry in root][-self.settings["max_history"]:]
        except (ET.ParseError, FileNotFoundError):
            entries = []
        self.history_label.config(text="\n".join(entries))
    
    def open_debug_menu(self):
        # Öffnet ein Fenster mit Debug-Informationen
        debug_window = tk.Toplevel(self.master)
        debug_window.title(texts[self.language]["debug_menu"])
        debug_info = f"Settings:\n{json.dumps(self.settings, indent=4)}\n\nLanguage: {self.language}"
        debug_label = ttk.Label(debug_window, text=debug_info, font=("Arial", 12))
        debug_label.pack(padx=10, pady=10)
        close_btn = ttk.Button(debug_window, text=texts[self.language]["close"], command=debug_window.destroy)
        close_btn.pack(pady=5)


def main():
    root = tk.Tk()
    app = PriceCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
