import os
import time
import pyautogui
from pynput import keyboard
from win10toast import ToastNotifier

# 1. Setup
toaster = ToastNotifier()
STATE_FILE = os.path.join(os.path.expanduser("~"), ".shoot_it_dir")

def take_shot():
    # 2. Safety Check 1: Is it set?
    if not os.path.exists(STATE_FILE):
        toaster.show_toast("🚫 Shoot-It Not Set", "Run 'shoot' in your terminal first!", duration=3)
        return

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        project_path = f.read().strip()

    # 3. Safety Check 2: Does the folder still exist?
    if not os.path.exists(project_path):
        toaster.show_toast("⚠️ Folder Missing", "The target folder was moved. Run 'shoot' again.", duration=3)
        os.remove(STATE_FILE)
        return

    # 4. Create Directory
    proof_dir = os.path.join(project_path, "proof")
    os.makedirs(proof_dir, exist_ok=True)

    # 5. Sequential Naming Logic
    existing = [f for f in os.listdir(proof_dir) if f.endswith('.png') and f[:2].isdigit()]
    count = 1
    if existing:
        numbers = [int(f[:2]) for f in existing]
        count = max(numbers) + 1
    
    filename = f"{count:02d}.png"
    filepath = os.path.join(proof_dir, filename)

    # 6. Capture the Screen
    time.sleep(0.2)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    # 7. Send Windows Notification
    toaster.show_toast(f"📸 Captured {filename}", f"Saved to proof folder.", duration=3)

# 8. Start Background Listener
print("🚀 Shoot-It (Windows) is running!")
print("Press Ctrl+Alt+S to take a shot. Close this terminal window to stop.")

with keyboard.GlobalHotKeys({'<ctrl>+<alt>+s': take_shot}) as h:
    h.join()
