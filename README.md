# 📸 Shoot-It

> Automate screenshots for your projects — press a hotkey, pick your capture type, and images are auto-numbered in a `proof/` folder.

No more manually cropping, renaming, or dragging files. Shoot-It saves numbered screenshots (`01.png`, `02.png`, ...) directly into a `proof/` folder inside whatever directory you're working in. The hotkey opens a clean, floating capture menu so you can choose exactly what gets captured before it is saved.

---

## ✨ What It Does

- Type `shoot` in any folder's terminal to set your capture target.
- Press `Ctrl + Alt + S` from anywhere to pop open the floating menu.
- Select **Area**, **Window**, or **Full** screen capture.
- Images automatically save and number themselves (`01.png`, `02.png`) inside a `proof/` folder.
- A native desktop notification pops up — click it to instantly preview your shot.
- Fully customizable: tweak UI colors, notification times, and hotkeys via `settings.json`.
- Press `Ctrl+C` in the terminal when you're done to stop capture mode.

---

## 🚀 Getting Started

Clone the repo:

```bash
git clone [https://github.com/EladCohen08/Shoot-It](https://github.com/EladCohen08/Shoot-It) shoot_it
cd shoot_it
```

**Pick your OS below — skip the other one.**

---

## 🐧 Linux Setup

<details>
<summary><strong>▶ Click to expand — Ubuntu / GNOME / Bash</strong></summary>

<br>

### 1 — Run the installer

```bash
bash linux/install.sh
source ~/.bashrc
```

### 2 — Create the shortcut

Go to **Settings → Keyboard → View and Customize Shortcuts → Custom Shortcuts** and click `+`:

| Field | Value |
|---|---|
| **Name** | `Shoot-It Menu` |
| **Command** | `python3 /path/to/your/shoot_it/linux/shoot_it.py` |
| **Shortcut** | `Ctrl + Alt + S` — or any combo you prefer |

<br>

**👉 Setup finished! Move to [Daily Usage](#-daily-usage).**

</details>

---

## 🪟 Windows Setup

<details>
<summary><strong>▶ Click to expand — Windows 10/11 / CMD / PowerShell</strong></summary>

<br>

> **Prerequisite:** [Python 3.x](https://www.python.org/downloads/) must be installed. (Make sure to check **"Add Python to PATH"** during installation).

<br>

### 1 — Run the installer

Open a terminal inside the `windows/` folder and run:

```bat
install.bat
```

### 2 — Restart your terminal

Close your current terminal window and open a fresh one for the changes to take effect.

<br>

**👉 Setup finished! Move to [Daily Usage](#-daily-usage).**

</details>

---

## 📖 Daily Usage

**1.** Open a terminal inside your project folder.

**2.** Enable Capture Mode:
```bash
shoot
```
*Keep this terminal open while you work.*

**3.** Press `Ctrl + Alt + S` from anywhere. Choose `Area`, `Window`, or `Full`. The capture is saved to `proof/` and copied to your clipboard:

```text
your-project/
└── proof/
    ├── 01.png
    ├── 02.png
    └── 03.png
```

**4.** Click the desktop notification to preview the image.

**5.** When done, go back to the terminal and press **`Ctrl + C`** to stop.

---

## 👋 About

Hi! I’m Elad Cohen, a second-year CS student at Bar-Ilan University. I built Shoot-It because submitting screenshots for Advanced System Programming exercises was a headache — manually cropping, renaming, and organizing just takes too long. Special thanks to Dorian(dorian123456785@gmail.com) for helping me build the windows version!

📬 Contact: cohenelad08@gmail.com
---

<div align="center">
  <sub>Made for the people who just want to get their work done.</sub>
</div>
