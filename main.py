#  Hey danke das du mein "Programm" heruntergeladen hast. Hoffe es gefällt dir.
#  Fullscreen-Modus und so weiter einfach einstellen in den Zeilen 10 - 13.
#  
#  Coded by mojelumi (~ mojelumi0)

# -----------------------------------------------------------------------------------------------------------------------------

# Hey, thanks for downloading my "program". Hope you like it.
# Just set fullscreen mode and so on in lines 10 - 13.
#
# Coded by mojelumi (~ mojelumi0)

import tkinter as tk
import xml.etree.ElementTree as ET
import locale

# Einstellungen
HISTORY_FILE = "history.xml"  # Hier kann man den Namen der .xml Datei ändern (.xml muss bleiben!)
MAX_HISTORY = 5  # Hier kann man die maximale Anzahl an den Einträgen in der Historie-Datei ändern
MINUSABWEICHUNG = 0.05  # Hier kann man die Abweichung ändern (z.B. 6,53 * 2 - 0,05 = ??)
FULLSCREEN_MODE = False  # Hier kann der Vollbildmodus aktiviert oder deaktiviert werden
HISTORY_ENABLED = True # Hier kann die Historie aktiviert oder deaktiviert werden

# Lokale Zahlenformate für Komma als Dezimaltrennzeichen
locale.setlocale(locale.LC_NUMERIC, "")

def speichere_historie(zahl):
    if not HISTORY_ENABLED:
        return  # Historie ist deaktiviert, nichts speichern

    try:
        tree = ET.parse(HISTORY_FILE)
        root = tree.getroot()
    except (ET.ParseError, FileNotFoundError):
        root = ET.Element("history")
    
    # Zahl auf 2 Dezimalstellen formatieren
    formatted_number = f"{zahl:.2f}"
    ET.SubElement(root, "entry").text = formatted_number
    
    while len(root) > MAX_HISTORY:
        root.remove(root[0])
    
    tree = ET.ElementTree(root)
    tree.write(HISTORY_FILE)
    aktualisiere_historie()

def berechne_preis(event=None):
    try:
        eingabe_text = eingabe.get().replace(",", ".")  # Erlaubt x,xx oder x.xx Format
        zahl = float(eingabe_text)
        ergebnis = (zahl * 2) - (MINUSABWEICHUNG)  # Berechnung durchführen
        ausgabe_label.config(text=f"Ergebnis: {ergebnis:.2f}")  # Ergebnis anzeigen
        speichere_historie(ergebnis)
    except ValueError:
        ausgabe_label.config(text="Bitte eine gültige Zahl eingeben!")  # Wenn man eine falsche Ziffer eingibt

def loesche_ausgabe(event):
    ausgabe_label.config(text="")

def beenden(event): 
    root.quit()

def aktualisiere_historie():
    if not HISTORY_ENABLED:
        historie_label.config(text="Historie ist deaktiviert.")
        return  # Historie ist deaktiviert, nichts anzeigen

    try:
        tree = ET.parse(HISTORY_FILE)
        root = tree.getroot()
        eintraege = [entry.text for entry in root][-MAX_HISTORY:]
    except (ET.ParseError, FileNotFoundError):
        eintraege = []
    
    historie_label.config(text="\n".join(eintraege))

# Hauptfenster erstellen
root = tk.Tk()
root.title("Supermarket Together Preisrechner")

# Vollbildmodus aktivieren oder deaktivieren
if FULLSCREEN_MODE:
    root.attributes("-fullscreen", True)
else:
    root.geometry("800x600")  # Beispielgröße für das Fenster

root.bind("<Escape>", beenden)

# Dark Mode Farben
bg_color = "#1e1e1e"
fg_color = "#ffffff"
button_color = "#444444"
button_hover_color = "#555555"

root.configure(bg=bg_color)

# Eingabefeld
label = tk.Label(root, text="Gib eine Zahl ein:", bg=bg_color, fg=fg_color, font=("Arial", 16))
label.pack(pady=20)

eingabe = tk.Entry(root, font=("Arial", 14), bg="#333333", fg=fg_color, insertbackground=fg_color, justify="center")
eingabe.pack(pady=10, ipadx=5, ipady=5)

eingabe.bind("<Return>", berechne_preis)
eingabe.bind("<BackSpace>", loesche_ausgabe)
eingabe.bind("<Delete>", loesche_ausgabe)

def on_enter(event):
    button.config(bg=button_hover_color)

def on_leave(event):
    button.config(bg=button_color)

# Button zur Berechnung
button = tk.Button(root, text="Berechnen", command=berechne_preis, font=("Arial", 14), bg=button_color, fg=fg_color, activebackground=button_hover_color, activeforeground=fg_color, relief="flat")
button.pack(pady=20, ipadx=10, ipady=5)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# Label zur Anzeige des Ergebnisses
ausgabe_label = tk.Label(root, text="", bg=bg_color, fg=fg_color, font=("Arial", 16))
ausgabe_label.pack(pady=20)

# Historie anzeigen
historie_label = tk.Label(root, text="", bg=bg_color, fg=fg_color, font=("Arial", 12), justify="left")
historie_label.pack(pady=20)

aktualisiere_historie()

# GUI starten
root.mainloop()
