#!/bin/bash

# Get the absolute path of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/autoshot.sh"

# Make the screenshot script executable
chmod +x "$SCRIPT_PATH"

# Add aliases to .bashrc safely
if ! grep -q "alias shoot=" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Shoot-It Aliases" >> ~/.bashrc
    echo "alias shoot='pwd > ~/.shoot_it_dir && echo \"📸 Shoot-It target set to: \$(pwd)\"'" >> ~/.bashrc
    echo "alias unshoot='rm -f ~/.shoot_it_dir && echo \"🚫 Shoot-It disabled.\"'" >> ~/.bashrc
    echo "✅ Aliases added to ~/.bashrc"
else
    echo "⚡ Aliases already exist in ~/.bashrc"
fi

echo ""
echo "🎉 Linux setup complete!"
echo "👉 Step 1: Run 'source ~/.bashrc' to activate your aliases."
echo "👉 Step 2: Go to Settings > Keyboard > Shortcuts."
echo "👉 Step 3: Add a new shortcut (e.g. Ctrl+Alt+S) and paste this exact command:"
echo "$SCRIPT_PATH"
