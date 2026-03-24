# 📸 Shoot-It

> Automate screenshots for your projects — press a hotkey, and images are auto-numbered in a proof/ folder.

No more manually cropping, renaming, or dragging files. Shoot-It saves numbered screenshots (`01.png`, `02.png`, ...) directly into a `proof/` folder inside whatever directory you're working in — triggered instantly from anywhere on your screen.

---

## ✨ What It Does

- Press **`Ctrl + Alt + S`** from anywhere — browser, IDE, doesn't matter
- Screenshots land in a `proof/` folder inside your current project directory, auto-numbered
- Native OS notifications confirm every capture
- One-word commands: `shoot` to arm it, `unshoot` to clear it

---

## 🚀 Getting Started

Clone the repo:

```bash
git clone https://github.com/EladCohen08/Shoot-It.git
cd Shoot-It
```

**Pick your OS below — skip the other one.**

---

## 🐧 Linux Setup

<details>
<summary><strong>▶ Click to expand — Ubuntu / GNOME / Bash</strong></summary>

<br>

> **Heads up:** Built for **GNOME-based** distros (Ubuntu, Pop!\_OS, Fedora) on **Bash**.
> If you're on KDE/XFCE or using Zsh — swap `gnome-screenshot` in `autoshot.sh` for your distro's screenshot tool, and add the aliases to `~/.zshrc` manually instead.

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

The installer will print the **exact path** to `autoshot.sh` — copy it, you'll need it in the next step.

### 3 — Bind the global shortcut

Go to **Settings → Keyboard → View and Customize Shortcuts → Custom Shortcuts** and click `+`:

| Field | Value |
|---|---|
| **Name** | `Shoot-It` |
| **Command** | The path printed by the installer (e.g. `/home/yourname/projects/Shoot-It/linux/autoshot.sh`) |
| **Shortcut** | `Ctrl + Alt + S` — or any combo you prefer |

> 💡 **Want a different shortcut?** Just pick any other combo in that same Settings screen — it's purely a GNOME setting, nothing to touch in the code.

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

This installs the required Python packages and automatically adds Shoot-It to your System PATH so `shoot` and `unshoot` work from any terminal, anywhere.

### 2 — Restart your terminal

Close your current CMD or PowerShell window and open a fresh one for the PATH changes to take effect.

### 3 — Change the hotkey (optional)

The default hotkey is `Ctrl + Alt + S`. To change it, open `windows/shoot_it.py` and edit the very last line:

```python
# Examples: '<ctrl>+<shift>+p'  or  '<alt>+x'
with keyboard.GlobalHotKeys({'<ctrl>+<alt>+s': take_shot}) as h:
```

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

**3.** Press `Ctrl + Alt + S` from anywhere. Each capture saves to `proof/` inside your folder, auto-numbered:

```
your-project/
└── proof/
    ├── 01.png
    ├── 02.png
    └── 03.png
```

**4.** When you're done:
```bash
unshoot
```
> On Windows, closing the terminal window also stops the listener.

---

## 👋 About

Built by **Elad Cohen**, a second-year CS student at Bar-Ilan University.

This started as a personal fix for a very specific pain: every exercise in Advanced System Programming requires submitting screenshot proof of your work. After manually cropping and renaming the hundredth image, I just built the thing that should have existed already.

If it saves you the same headache, great.

---

<div align="center">
  <sub>Made for the people who just want to get their work done.</sub>
</div>
