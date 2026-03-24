# 📸 Shoot-It

> Automate screenshots for your projects — press a hotkey, pick your capture type, and images are auto-numbered in a `proof/` folder.

No more manually cropping, renaming, or dragging files. Shoot-It saves numbered screenshots (`01.png`, `02.png`, ...) directly into a `proof/` folder inside whatever directory you're working in. The hotkey opens a clean, floating capture menu so you can choose exactly what gets captured before it is saved.

---

## ✨ What It Does

- Press **`Ctrl + Alt + S`** from anywhere — browser, IDE, terminal, doesn't matter.
- A minimalist, floating UI pops up asking if you want to capture an **Area**, a specific **Window**, or the **Full** screen.
- Screenshots land directly in a `proof/` folder inside your current project directory, strictly auto-numbered.
- **Clickable native notifications:** Click the popup to instantly open and view the captured image.
- **Customizable:** A local `settings.json` file lets you change UI colors, notification duration, and hotkeys.
- **One-word activation:** Type `shoot` to enable capture mode. Press `Ctrl+C` in the terminal to stop. 

---

## 🚀 Getting Started

Clone the repo into a clean, lowercase folder:

```bash
git clone [https://github.com/EladCohen08/Shoot-It.git](https://github.com/EladCohen08/Shoot-It.git) shoot_it
cd shoot_it
```

**Pick your OS below — skip the other one.**

---

## 🐧 Linux Setup

<details>
<summary><strong>▶ Click to expand — Ubuntu / GNOME / Bash</strong></summary>

<br>

> **Heads up:** Built for **GNOME-based** distros (Ubuntu, Pop!\_OS, Fedora) running **Wayland/X11**. It relies on native tools like `gnome-screenshot` and `xclip` for a flawless, native feel.

<br>

### 1 — Run the installer

From the root of the repo, run the installer to grab the system dependencies and setup your bash alias:

```bash
bash linux/install.sh
source ~/.bashrc
```

The installer will print the **exact command** you need for the next step.

### 2 — Bind the global shortcut

Because modern Linux (Wayland) blocks background keyloggers for security, you tie the UI directly to your OS settings. 

Go to **Settings → Keyboard → View and Customize Shortcuts → Custom Shortcuts** and click `+`:

| Field | Value |
|---|---|
| **Name** | `Shoot-It Menu` |
| **Command** | `python3 /path/to/your/shoot_it/linux/shoot_it.py` *(Use the exact path the installer gave you)* |
| **Shortcut** | `Ctrl + Alt + S` — or any combo you prefer |

</details>

---

## 🪟 Windows Setup

<details>
<summary><strong>▶ Click to expand — Windows 10/11 / CMD / PowerShell</strong></summary>

<br>

> **Prerequisite:** [Python 3.x](https://www.python.org/downloads/) must be installed.

<br>

### 1 — Run the installer

Open a terminal inside the `windows/` folder and run:

```bat
install.bat
```

This installs the required Python packages (`Pillow`, `pynput`, `pywin32`) and automatically adds Shoot-It to your System PATH so the `shoot` command works globally.

### 2 — Restart your terminal

Close your current CMD or PowerShell window and open a fresh one for the PATH changes to take effect.

</details>

---

## 📖 Daily Usage

**The core workflow is identical on both platforms.**

**1.** Open a terminal inside your project or assignment folder.

**2.** Enable Capture Mode:
```bash
shoot
```
> The terminal will lock in, print **SHOOT-IT IS READY TO CAPTURE**, and stay "live". Keep it minimized while you work.

**3.** Press `Ctrl + Alt + S` from anywhere. The custom menu will pop up. Choose `Area`, `Window`, or `Full`. The capture is taken, copied to your clipboard, and saved to `proof/` inside your folder:

```text
your-project/
└── proof/
    ├── 01.png
    ├── 02.png
    └── 03.png
```

**4.** Click the desktop notification if you want to preview the image.

**5.** When you're done working, go back to the terminal and press **`Ctrl + C`**. This cleanly stops the capture tool and releases the folder.

---

## ⚙️ Preferences (`settings.json`)

The first time you run `shoot`, a `settings.json` file is automatically generated in your `Shoot-It` folder. You can open it to tweak the tool to your liking:

```json
{
    "hotkey": "<ctrl>+<alt>+s", 
    "accent_color": "#2A7FFF",
    "bg_color": "#1A1A1B",
    "toast_duration_ms": 4000
}
```
* **Linux Users:** The `hotkey` field is ignored (since GNOME handles the shortcut), but you can fully customize the `accent_color` and `bg_color` of the popup menu.
* **Windows Users:** Edit the `hotkey` string here to change your shortcut without touching the code.

---

## 👋 About

Hi! I’m Elad Cohen, a second-year CS student at Bar-Ilan University. I built Shoot-It because submitting screenshots for every Advanced System Programming exercise was a headache — manually cropping, renaming, and organizing just takes too long.

Shoot-It automates it: pick a folder, press a hotkey, select your area, and your screenshots are saved and numbered automatically.

📬 Contact: cohenelad08@gmail.com
---

<div align="center">
  <sub>Made for the people who just want to get their work done.</sub>
</div>