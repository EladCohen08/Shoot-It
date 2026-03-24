# 📸 Shoot-It

> Automate screenshots for your projects — press a hotkey, pick your capture type, and images are auto-numbered in a `proof/` folder.

No more manually cropping, renaming, or dragging files. Shoot-It saves numbered screenshots (`01.png`, `02.png`, ...) directly into a `proof/` folder inside whatever directory you're working in. The hotkey opens a clean, floating capture menu so you can choose exactly what gets captured before it is saved.

---

## ✨ What It Does

- Type `shoot` in any folder's terminal to lock it in as your capture target.
- Press `Ctrl + Alt + S` from anywhere to pop open the floating menu.
- Select **Area**, **Window**, or **Full** screen capture.
- Images automatically save and number themselves (`01.png`, `02.png`) inside a `proof/` folder.
- A native desktop notification pops up — click it to instantly preview your shot.
- Fully customizable: tweak UI colors, notification times, and hotkeys via a local `settings.json` file.
- Press `Ctrl+C` in the terminal when you're done to cleanly stop capture mode.

---

## 🚀 Getting Started

Clone the repo:

```bash
git clone https://github.com/EladCohen08/Shoot-It shoot_it
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
| **Command** | `python3 /path/to/your/shoot_it/linux/shoot_it.py` |
| **Shortcut** | `Ctrl + Alt + S` — or any combo you prefer |

### 3 — Preferences (`settings.json`)

The first time you run `shoot`, a `settings.json` file is automatically generated. You can tweak the tool to your liking:

```json
{
    "accent_color": "#2A7FFF",
    "bg_color": "#1A1A1B",
    "toast_duration_ms": 4000
}
```
*To change your hotkey on Linux, edit the custom shortcut in your Ubuntu System Settings.*

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

### 3 — Preferences (`settings.json`)

The first time you run `shoot`, a `settings.json` file is automatically generated. You can tweak the tool to your liking:

```json
{
    "hotkey": "<ctrl>+<alt>+s",
    "accent_color": "#2A7FFF",
    "bg_color": "#1A1A1B",
    "toast_duration_ms": 3000
}
```
*To change your hotkey on Windows, edit the `hotkey` string right here in the JSON.*

</details>

---

## 📖 Daily Usage

**The core workflow is identical on both platforms.**

**1.** Open a terminal inside your project or assignment folder.

**2.** Enable Capture Mode:
```bash
shoot
```
> Keep this terminal open and minimized while you work.

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

## 👋 About

Hi! I’m Elad Cohen, a second-year CS student at Bar-Ilan University. I built Shoot-It because submitting screenshots for Advanced System Programming exercises was a headache — manually cropping, renaming, and organizing just takes too long.

Shoot-It automates it: pick a folder, press a hotkey, select your area, and your screenshots are saved and numbered automatically.

📬 Contact: cohenelad08@gmail.com
---

<div align="center">
  <sub>Made for the people who just want to get their work done.</sub>
</div>
