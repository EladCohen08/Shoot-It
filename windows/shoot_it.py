import locale
import os
import subprocess
import threading
import time

from PIL import ImageGrab
from pynput import keyboard

STATE_FILE = os.path.join(os.path.expanduser("~"), ".shoot_it_dir")
SNIP_TIMEOUT_SECONDS = 45
CAPTURE_LOCK = threading.Lock()


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


def _launch_snipping_ui():
    subprocess.run(
        ["cmd", "/c", "start", "", "ms-screenclip:"],
        check=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def _wait_for_snip_image(timeout_seconds):
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            image = ImageGrab.grabclipboard()
        except OSError:
            time.sleep(0.15)
            continue

        if hasattr(image, "save"):
            return image

        time.sleep(0.15)

    return None


def take_shot():
    if not os.path.exists(STATE_FILE):
        _notify("Shoot-It Not Set", "Run 'shoot' in your terminal first!")
        return

    try:
        project_path = _read_project_path()
    except UnicodeDecodeError:
        _notify("Shoot-It Error", "Could not read the saved folder. Run 'shoot' again.")
        return

    if not project_path:
        _notify("Shoot-It Error", "Saved folder is empty. Run 'shoot' again.")
        return

    if not os.path.isdir(project_path):
        _notify("Folder Missing", "The target folder was moved. Run 'shoot' again.")
        _remove_state_file()
        return

    filename, filepath = _next_capture_path(project_path)
    _notify("Shoot-It", "Select an area, window, or full screen to capture.")

    try:
        _launch_snipping_ui()
    except (OSError, subprocess.SubprocessError) as exc:
        _notify("Shoot-It Error", f"Could not open the Windows snipping UI: {exc}")
        return

    image = _wait_for_snip_image(SNIP_TIMEOUT_SECONDS)
    if image is None:
        _notify("Snip Cancelled", "No screenshot was captured.")
        return

    image.save(filepath)
    _notify(f"Captured {filename}", "Saved to proof folder.")


def start_capture():
    if not CAPTURE_LOCK.acquire(blocking=False):
        _notify("Capture Busy", "Finish the current snip before starting another one.")
        return

    def worker():
        try:
            take_shot()
        finally:
            CAPTURE_LOCK.release()

    threading.Thread(target=worker, daemon=True).start()


def main():
    print("Shoot-It (Windows) is running!")
    print("Press Ctrl+Alt+S to start a snip. Use the Windows snipping UI to choose the capture area.")

    with keyboard.GlobalHotKeys({"<ctrl>+<alt>+s": start_capture}) as hotkeys:
        hotkeys.join()


if __name__ == "__main__":
    main()
