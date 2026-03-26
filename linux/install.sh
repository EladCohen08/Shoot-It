#!/bin/bash

echo "========================================="
echo " Installing Shoot-It (Linux Edition)"
echo "========================================="

# 1. Install system dependencies
# gnome-screenshot: The engine
# xclip: To pipe the image to the clipboard
# python3-tk: For the GUI
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y gnome-screenshot xclip python3-tk

# 2. Get the absolute path of this folder
# This ensures 'shoot' works no matter where you call it from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 3. Make sure the scripts are executable
chmod +x "$SCRIPT_DIR/shoot"
chmod +x "$SCRIPT_DIR/shoot_it.py"

# 4. Add the alias to the user's bash configuration
# We use a comment tag so the user knows where this came from
echo "" >> ~/.bashrc
echo "# Shoot-It Tool" >> ~/.bashrc
echo "alias shoot='\"$SCRIPT_DIR/shoot\"'" >> ~/.bashrc

echo "========================================="
echo " ✅ Setup Complete!"
echo "========================================="
echo "👉 Step 1: Run 'source ~/.bashrc' to activate the 'shoot' command."
echo "👉 Step 2: Open System Settings > Keyboard > Shortcuts."
echo "👉 Step 3: Create a Custom Shortcut (e.g., Ctrl+Alt+S) with this command:"
echo "   python3 $SCRIPT_DIR/shoot_it.py"
echo "========================================="
