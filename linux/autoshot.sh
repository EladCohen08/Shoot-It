#!/bin/bash

STATE_FILE="$HOME/.shoot_it_dir"

# Safety Check 1: Did they run 'shoot'?
if [ ! -f "$STATE_FILE" ]; then
    notify-send "🚫 Shoot-It Not Set" "Run 'shoot' in your terminal first!" --icon=dialog-error
    exit 1
fi

PROJECT_DIR=$(cat "$STATE_FILE")
TARGET_DIR="$PROJECT_DIR/proof"

# Safety Check 2: Does the project folder still exist?
if [ ! -d "$PROJECT_DIR" ]; then
    notify-send "⚠️ Folder Missing" "The project folder was moved or deleted. Run 'shoot' again." --icon=dialog-error
    rm -f "$STATE_FILE"
    exit 1
fi

# Create proof directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Sequential Naming (01.png, 02.png...)
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

# Take the screenshot (0.2s delay prevents shortcut keys from messing up the shot)
sleep 0.2
gnome-screenshot -w -f "$FILEPATH"

# Send clickable notification
ACTION=$(notify-send "📸 Captured $FILENAME" \
    "Click here to preview" \
    --icon=camera-photo \
    --action="default=Open" \
    --expire-time=4000)

# Open image if clicked
if [ "$ACTION" == "default" ]; then
    xdg-open "$FILEPATH" >/dev/null 2>&1 &
fi
