import os, subprocess, json
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
STATE_FILE = os.path.join(os.path.expanduser("~"), ".shoot-it-dir")

DEFAULT_SETTINGS = {
    "accent_color": "#2A7FFF",
    "bg_color": "#1A1A1B",
    "toast_duration_ms": 4000
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f: json.dump(DEFAULT_SETTINGS, f, indent=4)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r") as f: return json.load(f)

CONF = load_settings()
BG, ACCENT, TEXT = CONF["bg_color"], CONF["accent_color"], "#FFFFFF"

class ShootItApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                self.target_dir = os.path.join(f.read().strip(), "proof")
        except:
            subprocess.run(["notify-send", "🚫 Shoot-It Not Armed", "Run 'shoot' in a terminal first!", "--icon=dialog-error"])
            self.root.destroy()
            return

        self._ui()

    def _notify_success(self, filepath, filename):
        try:
            res = subprocess.run(
                ["notify-send", f"📸 Captured {filename}", "Click here to preview",
                 "--icon=camera-photo", "--action=default=Open", f"--expire-time={CONF['toast_duration_ms']}"],
                capture_output=True, text=True
            )
            if "default" in res.stdout:
                subprocess.Popen(["xdg-open", filepath])
        except Exception: 
            pass

    def _save(self, mode):
        try:
            os.makedirs(self.target_dir, exist_ok=True)
            exist = [f for f in os.listdir(self.target_dir) if f.endswith(".png") and f[:2].isdigit()]
            num = max([int(f[:2]) for f in exist] + [0]) + 1
            name, fpath = f"{num:02d}.png", os.path.join(self.target_dir, f"{num:02d}.png")

            cmd = ["gnome-screenshot", "-f", fpath]
            if mode == "Area": cmd.insert(1, "-a")
            elif mode == "Window": cmd.insert(1, "-w")

            subprocess.run(cmd, check=True)

            if not os.path.exists(fpath): return

            subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-i", fpath], check=True)
            self._notify_success(fpath, name)
            
        except subprocess.CalledProcessError:
            pass

    def _ui(self):
        self.root.attributes("-type", "splash")
        self.root.attributes("-topmost", True)
        
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"340x100+{(sw-340)//2}+{(sh-100)//2}")
        self.root.configure(bg=BG, highlightbackground=ACCENT, highlightthickness=2)

        cont = tk.Frame(self.root, bg=BG)
        cont.pack(expand=True, fill="both", pady=5)
        
        btns = tk.Frame(cont, bg=BG)
        btns.pack()

        for m in ["Area", "Window", "Full"]:
            b = tk.Button(btns, text=m, font=("sans-serif", 10, "bold"), bg=BG, fg=TEXT, 
                          activebackground=ACCENT, activeforeground="white", relief="flat", 
                          width=9, cursor="hand2", command=lambda mode=m: self._trigger(mode))
            b.pack(side="left", padx=5, pady=5)
            b.bind("<Enter>", lambda e, x=b: x.configure(bg="#252526"))
            b.bind("<Leave>", lambda e, x=b: x.configure(bg=BG))
        
        tk.Label(cont, text="ESC to cancel", fg="#666666", bg=BG, font=("sans-serif", 8)).pack()
        
        self.root.deiconify()
        
        self.root.after(100, self.root.focus_force)
        self.root.bind_all("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<FocusOut>", lambda e: self.root.destroy())

    def _trigger(self, mode):
        self.root.withdraw() 
        self.root.update()   
        self._save(mode)
        self.root.destroy()  

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ShootItApp().run()