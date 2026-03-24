#!/bin/bash

# 1. Path Setup
STATE_FILE="$HOME/.autoshot_dir"

# CHECK: If the file doesn't exist, we notify the user and STOP
if [ ! -f "$STATE_FILE" ]; then
    notify-send "🚫 Autoshot Not Set" "Run 'setshot' in your project folder first!" --icon=dialog-error
    exit 1
fi

CURRENT_DIR=$(cat "$STATE_FILE")

# SAFETY CHECK: Does the project folder still exist on disk?
if [ ! -d "$CURRENT_DIR" ]; then
    notify-send "⚠️ Folder Missing" "The path was moved or deleted. Run 'setshot' again."
    rm -f "$STATE_FILE" # Clean up the dead link
    exit 1
fi

TARGET_DIR="$CURRENT_DIR/proof"
mkdir -p "$TARGET_DIR"

# 2. Sequencing (01, 02...)
COUNT=1
for file in "$TARGET_DIR"/[0-9][0-9].png; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .png)
        num=$((10#$basename + 1))
        [ "$num" -gt "$COUNT" ] && COUNT=$num
    fi
done
FILENAME=$(printf "%02d.png" $COUNT)
FILEPATH="$TARGET_DIR/$FILENAME"

# 3. Take Shot
sleep 0.5
gnome-screenshot -w -f "$FILEPATH"

# 4. Clickable Notification Logic
# Note: Some Ubuntu versions require the 'default' action to be explicitly caught
# We use a longer timeout (5s) to give you time to click
ACTION=$(notify-send "📸 Captured $FILENAME" \
    "Click here to preview" \
    --icon=camera-photo \
    --action="default=Open" \
    --expire-time=5000)

# 5. Handle the click
case "$ACTION" in
    "default")
        eog "$FILEPATH" >/dev/null 2>&1 &
        ;;
esac
