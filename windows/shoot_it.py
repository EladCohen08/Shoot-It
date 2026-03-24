import ctypes, io, os, queue, threading, winsound, json, datetime
import tkinter as tk
from PIL import ImageGrab
from pynput import keyboard
import win32gui, win32clipboard

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
STATE_FILE = os.path.join(os.path.expanduser("~"), ".shoot-it-dir")

DEFAULT_SETTINGS = {
    "hotkey": "<ctrl>+<alt>+s",
    "accent_color": "#2A7FFF",
    "bg_color": "#1A1A1B",
    "toast_duration_ms": 3000
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

CONF = load_settings()
BG, ACCENT, TEXT = CONF["bg_color"], CONF["accent_color"], "#FFFFFF"
PICKER_SIZE = "340x100"
DWMWA_EXTENDED_FRAME_BOUNDS = 9

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()

def log(action, message):
    t = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {action:10} | {message}")

class LinuxToast:
    def __init__(self, root, filepath, filename):
        self.filepath = filepath
        self.win = tk.Toplevel(root)
        self.win.withdraw()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=BG, highlightbackground=ACCENT, highlightthickness=1)
        w, h = 300, 60
        sw = self.win.winfo_screenwidth()
        self.win.geometry(f"{w}x{h}+{(sw-w)//2}+30")
        tk.Label(self.win, text=f"Captured {filename}", fg=TEXT, bg=BG, font=("Segoe UI", 10, "bold")).pack(pady=(8, 0))
        tk.Label(self.win, text="Click to open image", fg="#888888", bg=BG, font=("Segoe UI", 8)).pack()
        self.win.deiconify()
        for widget in [self.win, *self.win.winfo_children()]:
            widget.bind("<Button-1>", self._open)
        root.after(CONF["toast_duration_ms"], self.win.destroy)

    def _open(self, e):
        os.startfile(self.filepath)
        self.win.destroy()

class AreaSelector:
    def __init__(self, root, on_selected, on_cancelled):
        self.root, self.on_selected, self.on_cancelled = root, on_selected, on_cancelled
        self.win = tk.Toplevel(root)
        self.win.withdraw()
        self.win.attributes("-fullscreen", True, "-topmost", True, "-alpha", 0.3)
        self.win.overrideredirect(True)
        self.win.configure(bg="black", cursor="crosshair")
        self.canvas = tk.Canvas(self.win, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.rect = None
        self.start_x = self.start_y = 0
        self.win.bind("<ButtonPress-1>", self._start)
        self.win.bind("<B1-Motion>", self._drag)
        self.win.bind("<ButtonRelease-1>", self._stop)
        self.win.bind("<Escape>", lambda e: self._close())
        self.win.deiconify()

    def _start(self, e):
        self.start_x, self.start_y = e.x, e.y
        self.rect = self.canvas.create_rectangle(e.x, e.y, e.x, e.y, outline=ACCENT, width=3)

    def _drag(self, e):
        self.canvas.coords(self.rect, self.start_x, self.start_y, e.x, e.y)

    def _stop(self, e):
        bbox = (min(self.start_x, e.x), min(self.start_y, e.y), max(self.start_x, e.x), max(self.start_y, e.y))
        self.win.destroy()
        if (bbox[2] - bbox[0]) > 10: self.on_selected(bbox)
        else: self.on_cancelled()

    def _close(self):
        self.win.destroy()
        self.on_cancelled()

class ShootItApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.queue = queue.SimpleQueue()
        self.lock = threading.Lock()
        self.active = False

    def _feedback(self):
        try:
            winsound.PlaySound(r"C:\Windows\Media\camera_click.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            winsound.MessageBeep()

    def _save(self, grab_fn):
        with self.lock:
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f: path = f.read().strip()
                p_dir = os.path.join(path, "proof")
                os.makedirs(p_dir, exist_ok=True)
                exist = [f for f in os.listdir(p_dir) if f.endswith(".png") and f[:2].isdigit()]
                num = max([int(f[:2]) for f in exist] + [0]) + 1
                name, fpath = f"{num:02d}.png", os.path.join(p_dir, f"{num:02d}.png")
                img = grab_fn()
                img.save(fpath)
                out = io.BytesIO()
                img.convert("RGB").save(out, "BMP")
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, out.getvalue()[14:])
                win32clipboard.CloseClipboard()
                self._feedback()
                log("SAVE", f"Captured {name}")
                LinuxToast(self.root, fpath, name)
            except Exception as e: log("ERROR", str(e))
            finally:
                self.active = False
                self.root.withdraw()

    def _ui(self):
        if self.active: return
        self.active = True
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{PICKER_SIZE}+{(sw-340)//2}+{(sh-100)//2}")
        self.root.configure(bg=BG, highlightbackground=ACCENT, highlightthickness=2)
        for c in self.root.winfo_children(): c.destroy()
        cont = tk.Frame(self.root, bg=BG); cont.pack(expand=True, fill="both", pady=5)
        btns = tk.Frame(cont, bg=BG); btns.pack()
        for m in ["Area", "Window", "Full"]:
            b = tk.Button(btns, text=m, font=("Segoe UI", 10, "bold"), bg=BG, fg=TEXT, 
                          activebackground=ACCENT, activeforeground="white", relief="flat", 
                          width=9, cursor="hand2", command=lambda mode=m: self._trigger(mode))
            b.pack(side="left", padx=5, pady=5)
            b.bind("<Enter>", lambda e, x=b: x.configure(bg="#252526"))
            b.bind("<Leave>", lambda e, x=b: x.configure(bg=BG))
        tk.Label(cont, text="ESC to cancel", fg="#666666", bg=BG, font=("Segoe UI", 8)).pack()
        self.root.deiconify()
        self.root.bind("<Escape>", lambda e: self._cancel())

    def _trigger(self, mode):
        self.root.withdraw()
        if mode == "Full": self.queue.put(("save", lambda: ImageGrab.grab(all_screens=True)))
        elif mode == "Area": AreaSelector(self.root, lambda b: self.queue.put(("save", lambda: ImageGrab.grab(bbox=b, all_screens=True))), self._cancel)
        elif mode == "Window": self.queue.put(("save", self._get_win))

    def _get_win(self):
        hwnd = win32gui.GetForegroundWindow()
        r = ctypes.wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(ctypes.wintypes.HWND(hwnd), DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.byref(r), ctypes.sizeof(r))
        return ImageGrab.grab(bbox=(r.left, r.top, r.right, r.bottom), all_screens=True)

    def _cancel(self):
        self.active = False
        log("STATUS", "Cancelled")
        self.root.withdraw()

    def _poll(self):
        while not self.queue.empty():
            act, data = self.queue.get()
            if act == "open": self._ui()
            if act == "save": self._save(data)
        self.root.after(50, self._poll)

    def run(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                p_path = f.read().strip()
                proof_path = os.path.join(p_path, "proof")
        except: proof_path = "Undefined"
        print("\n" + "="*50 + "\n SHOOT-IT IS ARMED \n" + "="*50)
        print(f" Saving to: {proof_path}\n Settings:  {SETTINGS_FILE}\n Hotkey:    {CONF['hotkey']}\n" + "="*50)
        log("STATUS", "Ready")
        hk = keyboard.HotKey(keyboard.HotKey.parse(CONF["hotkey"]), lambda: self.queue.put(("open", None)))
        l = keyboard.Listener(on_press=lambda k: hk.press(l.canonical(k)), on_release=lambda k: hk.release(l.canonical(k)))
        l.daemon = True; l.start(); self.root.after(50, self._poll); self.root.mainloop()

if __name__ == "__main__":
    ShootItApp().run()