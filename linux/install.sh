#!/bin/bash

# Get the absolute path of the autoshot script
SCRIPT_PATH="$(pwd)/linux/autoshot.sh"
chmod +x "$SCRIPT_PATH"

# Add aliases to .bashrc if they don't exist
if ! grep -q "alias setshot=" ~/.bashrc; then
    echo "alias setshot='pwd > ~/.autoshot_dir && echo \"📸 Target set to: \$(pwd)\"'" >> ~/.bashrc
    echo "alias unsetshot='rm -f ~/.autoshot_dir && echo \"🚫 Autoshot disabled.\"'" >> ~/.bashrc
    echo "Done! Please run 'source ~/.bashrc' to activate."
else
    echo "Aliases already exist in .bashrc"
fi

echo "Configuration complete. Point your Global Shortcut to: $SCRIPT_PATH"
