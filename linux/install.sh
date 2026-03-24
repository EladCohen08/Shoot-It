#!/bin/bash

echo "========================================="
echo " Installing Shoot-It (Linux Edition)"
echo "========================================="

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y gnome-screenshot xclip python3-tk

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
chmod +x "$SCRIPT_DIR/shoot"
chmod +x "$SCRIPT_DIR/shoot_it.py"

# Clean old aliases
sed -i '/# Shoot-It/d' ~/.bashrc
sed -i '/alias shoot=/d' ~/.bashrc
sed -i '/alias unshoot=/d' ~/.bashrc

# Add clean alias pointing to the live wrapper
echo "" >> ~/.bashrc
echo "# Shoot-It Alias" >> ~/.bashrc
echo "alias shoot='\"$SCRIPT_DIR/shoot\"'" >> ~/.bashrc

echo ""
echo "[Success] Setup complete!"
echo "👉 Step 1: Run 'source ~/.bashrc' to activate the command."
echo "👉 Step 2: Go to Settings > Keyboard > Shortcuts."
echo "👉 Step 3: Add a custom shortcut (e.g. Ctrl+Alt+S) with this exact command:"
echo "python3 $SCRIPT_DIR/shoot_it.py"