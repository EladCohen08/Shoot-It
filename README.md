# 📸 Shoot-It

> Automated, sequential screenshot capture for developers. Set a folder, press a hotkey, done.

No more manually cropping, renaming, or dragging files. Shoot-It saves numbered screenshots (`01.png`, `02.png`, ...) directly into a `proof/` folder inside whatever directory you're working in — triggered instantly from anywhere on your screen.

Built for students and developers documenting Jira tickets, CS assignments, or any proof-of-work workflow.

---

## ✨ What It Does

- Press **`Ctrl + Alt + S`** from anywhere — browser, IDE, doesn't matter
- Screenshots land in a `proof/` folder inside your current project directory, auto-numbered
- Native OS notifications confirm every capture
- One-word commands: `shoot` to arm it, `unshoot` to clear it

---

## 🚀 Getting Started

Clone the repo and move into it:

```bash
git clone https://github.com/EladCohen08/Shoot-It.git
cd Shoot-It
```

**Pick your OS below and follow only those steps — skip the other one.**

---

## 🐧 Linux Setup

<details>
<summary><strong>▶ Click to expand — Ubuntu / GNOME / Bash</strong></summary>

<br>

> **Compatibility:** Built for **GNOME-based** distros (Ubuntu, Pop!\_OS, Fedora) running **Bash**.
> If you're on KDE, XFCE, or using Zsh — the script will need minor manual tweaks (swap `gnome-screenshot` in `autoshot.sh` for your distro's screenshot tool, and add the aliases to `~/.zshrc` instead).
> On Ubuntu, you're good to go as-is.

<br>

### 1 — Install dependencies

```bash
sudo apt install gnome-screenshot libnotify-bin
```

### 2 — Run the installer

From the root of the repo:

```bash
bash linux/install.sh
source ~/.bashrc
```

This sets up the `shoot` and `unshoot` aliases globally in your terminal.

### 3 — Bind the global shortcut

Open **Settings → Keyboard → View and Customize Shortcuts → Custom Shortcuts** and click `+`:

| Field | Value |
|---|---|
| **Name** | `Shoot-It` |
| **Command** | The path printed by the installer (e.g. `/home/yourname/projects/Shoot-It/linux/autoshot.sh`) |
| **Shortcut** | `Ctrl + Alt + S` |

Done. The shortcut is now active system-wide.

</details>

---

## 🪟 Windows Setup

<details>
<summary><strong>▶ Click to expand — Windows 10/11 / CMD / PowerShell</strong></summary>

<br>

> **Prerequisite:** Make sure **Python 3.x** is installed — [download it here](https://www.python.org/downloads/) if needed.

<br>

### 1 — Run the installer

Navigate into the `windows/` folder and double-click `install.bat`.

This will:
- Install the required Python packages (`pyautogui`, `pynput`, `win10toast`)
- Automatically add Shoot-It to your System PATH so `shoot` and `unshoot` work from any terminal, anywhere

### 2 — Restart your terminal

Close your current CMD or PowerShell window and open a fresh one for the PATH changes to take effect.

> 💡 **Want a different hotkey?** Open `windows/shoot_it.py` and edit the `HOTKEY` variable at the bottom of the file.

</details>

---

## 📖 Daily Usage

**The workflow is identical on both platforms.**

**1.** Open a terminal inside your project or assignment folder

**2.** Arm Shoot-It:
```bash
shoot
```
> On Windows, this also starts the background listener — keep the terminal open and minimized while you work.

**3.** Press `Ctrl + Alt + S` whenever you need a screenshot. Each capture is saved to `proof/` inside your folder, auto-numbered:

```
your-project/
└── proof/
    ├── 01.png
    ├── 02.png
    └── 03.png
```

**4.** When you're done, disarm:
```bash
unshoot
```
> On Windows, closing the terminal window also stops the listener.

---

<div align="center">
  <sub>Made for the people who just want to get their work done.</sub>
</div>
