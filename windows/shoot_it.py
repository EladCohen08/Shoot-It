import ctypes
import locale
import os
import queue
import threading
import tkinter as tk

from PIL import ImageGrab
from pynput import keyboard, mouse
import win32gui

STATE_FILE = os.path.join(os.path.expanduser("~"), ".shoot_it_dir")
PICKER_WIDTH = 320
PICKER_HEIGHT = 140
MIN_AREA_SIZE = 4
DWMWA_EXTENDED_FRAME_BOUNDS = 9
GA_ROOT = 2

USER32 = ctypes.windll.user32
DWMAPI = ctypes.windll.dwmapi


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def _state_file_encodings():
    encodings = ["utf-8-sig", locale.getpreferredencoding(False), "mbcs", "cp862", "cp1255"]
    seen = set()

    for encoding in encodings:
        if encoding and encoding not in seen:
            seen.add(encoding)
            yield encoding


def _read_project_path():
    with open(STATE_FILE, "rb") as state_file:
        raw_bytes = state_file.read()

    for encoding in _state_file_encodings():
        try:
            return raw_bytes.decode(encoding).strip()
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError("state-file", raw_bytes, 0, len(raw_bytes), "unable to decode path")


def _notify(title, message):
    print(f"[Shoot-It] {title}: {message}")


def _remove_state_file():
    try:
        os.remove(STATE_FILE)
    except OSError:
        pass


def _next_capture_path(project_path):
    proof_dir = os.path.join(project_path, "proof")
    os.makedirs(proof_dir, exist_ok=True)

    existing = [name for name in os.listdir(proof_dir) if name.endswith(".png") and name[:2].isdigit()]
    count = 1
    if existing:
        numbers = [int(name[:2]) for name in existing]
        count = max(numbers) + 1

    filename = f"{count:02d}.png"
    return filename, os.path.join(proof_dir, filename)


def _virtual_screen_geometry():
    left = USER32.GetSystemMetrics(76)
    top = USER32.GetSystemMetrics(77)
    width = USER32.GetSystemMetrics(78)
    height = USER32.GetSystemMetrics(79)
    return left, top, width, height


def _capture_image_from_bbox(bbox):
    left, top, right, bottom = bbox
    return ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True)


def _capture_fullscreen_image():
    return ImageGrab.grab(all_screens=True)


def _window_rect(hwnd):
    rect = RECT()
    result = DWMAPI.DwmGetWindowAttribute(
        int(hwnd),
        DWMWA_EXTENDED_FRAME_BOUNDS,
        ctypes.byref(rect),
        ctypes.sizeof(rect),
    )
    if result == 0:
        return rect.left, rect.top, rect.right, rect.bottom

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return left, top, right, bottom


class AreaSelector:
    def __init__(self, root, on_selected, on_cancelled):
        self.root = root
        self.on_selected = on_selected
        self.on_cancelled = on_cancelled
        self.screen_left, self.screen_top, self.screen_width, self.screen_height = _virtual_screen_geometry()
        self.start_x = None
        self.start_y = None
        self.selection_id = None

        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.20)
        self.window.configure(bg="black")
        self.window.geometry(
            f"{self.screen_width}x{self.screen_height}+{self.screen_left}+{self.screen_top}"
        )
        self.window.bind("<Escape>", lambda _event: self.cancel())

        self.canvas = tk.Canvas(self.window, bg="black", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_text(
            24,
            24,
            anchor="nw",
            text="Drag to capture an area. Press Esc to cancel.",
            fill="white",
            font=("Segoe UI", 12, "bold"),
        )
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def cancel(self):
        self.window.destroy()
        self.on_cancelled()

    def _canvas_coords(self, event):
        return event.x_root - self.screen_left, event.y_root - self.screen_top

    def _on_press(self, event):
        self.start_x, self.start_y = self._canvas_coords(event)
        self.selection_id = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="white",
            width=2,
        )

    def _on_drag(self, event):
        if self.selection_id is None:
            return

        current_x, current_y = self._canvas_coords(event)
        self.canvas.coords(self.selection_id, self.start_x, self.start_y, current_x, current_y)

    def _on_release(self, event):
        if self.selection_id is None:
            self.cancel()
            return

        end_x, end_y = self._canvas_coords(event)
        left = min(self.start_x, end_x) + self.screen_left
        top = min(self.start_y, end_y) + self.screen_top
        right = max(self.start_x, end_x) + self.screen_left
        bottom = max(self.start_y, end_y) + self.screen_top

        self.window.destroy()
        if right - left < MIN_AREA_SIZE or bottom - top < MIN_AREA_SIZE:
            self.on_cancelled()
            return

        self.root.after(60, lambda: self.on_selected((left, top, right, bottom)))


class WindowSelector:
    def __init__(self, root, own_window_ids, on_selected, on_cancelled):
        self.root = root
        self.own_window_ids = own_window_ids
        self.on_selected = on_selected
        self.on_cancelled = on_cancelled
        self.listener = None

        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="#111111")
        self.window.geometry("+40+40")
        self.window.bind("<Escape>", lambda _event: self.cancel())
        self.own_window_ids = set(own_window_ids)
        self.own_window_ids.add(self.window.winfo_id())

        label = tk.Label(
            self.window,
            text="Click a window to capture.\nRight-click or Esc to cancel.",
            bg="#111111",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=14,
            pady=10,
            justify="left",
        )
        label.pack()

        self.listener = mouse.Listener(on_click=self._on_click)
        self.listener.start()

    def cancel(self):
        self._stop_listener()
        self.window.destroy()
        self.on_cancelled()

    def _stop_listener(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

    def _on_click(self, x, y, button, pressed):
        if not pressed:
            return

        if button == mouse.Button.right:
            self.root.after(0, self.cancel)
            return False

        if button != mouse.Button.left:
            return

        hwnd = win32gui.WindowFromPoint((x, y))
        hwnd = win32gui.GetAncestor(hwnd, GA_ROOT)
        if not hwnd or hwnd in self.own_window_ids or not win32gui.IsWindowVisible(hwnd):
            return

        try:
            bbox = _window_rect(hwnd)
        except win32gui.error:
            return

        self._stop_listener()
        self.window.destroy()
        self.root.after(60, lambda: self.on_selected(bbox))
        return False


class ShootItApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Shoot-It")
        self.actions = queue.SimpleQueue()
        self.capture_active = False
        self.capture_lock = threading.Lock()
        self.selector = None
        self.hotkey_listener = None

    def run(self):
        print("Shoot-It (Windows) is running!")
        print("Press Ctrl+Alt+S to open the capture picker. Close this terminal window to stop.")

        self._start_hotkey_listener()
        self.root.after(50, self._process_actions)
        self.root.mainloop()

    def _start_hotkey_listener(self):
        hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+<alt>+s"), self._request_picker)

        def on_press(key):
            hotkey.press(self.hotkey_listener.canonical(key))

        def on_release(key):
            hotkey.release(self.hotkey_listener.canonical(key))

        self.hotkey_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.hotkey_listener.daemon = True
        self.hotkey_listener.start()

    def _request_picker(self):
        self.actions.put(("open_picker", None))

    def _process_actions(self):
        while True:
            try:
                action, payload = self.actions.get_nowait()
            except queue.Empty:
                break

            if action == "open_picker":
                self._show_picker()
            elif action == "save_fullscreen":
                self._save_capture(_capture_fullscreen_image)
            elif action == "save_bbox":
                self._save_capture(lambda: _capture_image_from_bbox(payload))
            elif action == "cancel":
                self._cancel_capture(payload)

        self.root.after(50, self._process_actions)

    def _show_picker(self):
        if self.capture_active:
            return

        if not self._target_is_ready():
            return

        self.capture_active = True
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = max((screen_width - PICKER_WIDTH) // 2, 20)
        position_y = max((screen_height - PICKER_HEIGHT) // 2, 20)
        self.root.geometry(f"{PICKER_WIDTH}x{PICKER_HEIGHT}+{position_x}+{position_y}")
        self.root.configure(bg="#101418")

        for child in self.root.winfo_children():
            child.destroy()

        frame = tk.Frame(self.root, bg="#101418", padx=16, pady=14)
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text="Choose capture mode",
            bg="#101418",
            fg="white",
            font=("Segoe UI", 13, "bold"),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            frame,
            text="Area, window, or fullscreen.",
            bg="#101418",
            fg="#B8C2CC",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w", pady=(4, 12))

        buttons = tk.Frame(frame, bg="#101418")
        buttons.pack(fill="x")

        self._picker_button(buttons, "Area", self._start_area_capture).pack(side="left", expand=True, fill="x")
        self._picker_button(buttons, "Window", self._start_window_capture).pack(side="left", expand=True, fill="x", padx=8)
        self._picker_button(buttons, "Fullscreen", self._start_fullscreen_capture).pack(side="left", expand=True, fill="x")

        cancel = tk.Button(
            frame,
            text="Cancel",
            command=lambda: self._cancel_capture("Cancelled before capture."),
            bg="#202833",
            fg="white",
            activebackground="#2F3947",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        )
        cancel.pack(anchor="e", pady=(12, 0))

        self.root.bind("<Escape>", lambda _event: self._cancel_capture("Cancelled before capture."))
        _notify("Shoot-It", "Choose Area, Window, or Fullscreen.")

    def _picker_button(self, parent, label, command):
        return tk.Button(
            parent,
            text=label,
            command=command,
            bg="#2A7FFF",
            fg="white",
            activebackground="#5C99FF",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=12,
            font=("Segoe UI", 10, "bold"),
        )

    def _hide_picker(self):
        self.root.unbind("<Escape>")
        self.root.withdraw()

    def _target_is_ready(self):
        if not os.path.exists(STATE_FILE):
            _notify("Shoot-It Not Set", "Run 'shoot' in your terminal first!")
            return False

        try:
            project_path = _read_project_path()
        except UnicodeDecodeError:
            _notify("Shoot-It Error", "Could not read the saved folder. Run 'shoot' again.")
            return False

        if not project_path:
            _notify("Shoot-It Error", "Saved folder is empty. Run 'shoot' again.")
            return False

        if not os.path.isdir(project_path):
            _notify("Folder Missing", "The target folder was moved. Run 'shoot' again.")
            _remove_state_file()
            return False

        return True

    def _resolve_capture_destination(self):
        if not self._target_is_ready():
            raise FileNotFoundError("Saved folder is not available.")

        project_path = _read_project_path()
        return _next_capture_path(project_path)

    def _start_fullscreen_capture(self):
        self._hide_picker()
        self.actions.put(("save_fullscreen", None))

    def _start_area_capture(self):
        self._hide_picker()
        self.selector = AreaSelector(
            self.root,
            lambda bbox: self.actions.put(("save_bbox", bbox)),
            lambda: self.actions.put(("cancel", "Area selection cancelled.")),
        )

    def _start_window_capture(self):
        self._hide_picker()
        own_window_ids = {self.root.winfo_id()}
        self.selector = WindowSelector(
            self.root,
            own_window_ids,
            lambda bbox: self.actions.put(("save_bbox", bbox)),
            lambda: self.actions.put(("cancel", "Window selection cancelled.")),
        )

    def _save_capture(self, capture_fn):
        if not self.capture_lock.acquire(blocking=False):
            self._finish_capture()
            return

        try:
            filename, filepath = self._resolve_capture_destination()
            image = capture_fn()
            image.save(filepath)
            _notify(f"Captured {filename}", "Saved to proof folder.")
        except FileNotFoundError:
            _notify("Shoot-It Error", "Saved folder is not available. Run 'shoot' again.")
        except UnicodeDecodeError:
            _notify("Shoot-It Error", "Could not read the saved folder. Run 'shoot' again.")
        except OSError as exc:
            _notify("Shoot-It Error", f"Could not save the screenshot: {exc}")
        finally:
            self.capture_lock.release()
            self._finish_capture()

    def _cancel_capture(self, reason):
        _notify("Shoot-It", reason)
        self._finish_capture()

    def _finish_capture(self):
        self.selector = None
        self.capture_active = False
        self._hide_picker()


if __name__ == "__main__":
    ShootItApp().run()
