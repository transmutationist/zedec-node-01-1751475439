#!/bin/bash
set -e
URL="https://api.pcloud.com/getpubzip?code=kZJNRf5ZJG08Ck9uIKXLjqtmUDNU9BqsECi7"
TARGET_DIR="pcloud_autodeploy"
ZIP_FILE="pcloud_autodeploy.zip"

# Create clean workspace
rm -rf "$TARGET_DIR" "$ZIP_FILE"
mkdir -p "$TARGET_DIR"

# Download archive
curl -L "$URL" -o "$ZIP_FILE"

# Extract
unzip "$ZIP_FILE" -d "$TARGET_DIR"

# Search for deploy scripts
SCRIPT=""
if [ -f "$TARGET_DIR/install.sh" ]; then
  SCRIPT="$TARGET_DIR/install.sh"
elif [ -f "$TARGET_DIR/setup.sh" ]; then
  SCRIPT="$TARGET_DIR/setup.sh"
else
  # Try to find scripts deeper
  SCRIPT=$(find "$TARGET_DIR" -maxdepth 2 -name 'install.sh' -o -name 'setup.sh' | head -n 1)
fi

if [ -n "$SCRIPT" ]; then
  echo "Running $SCRIPT"
  chmod +x "$SCRIPT"
  "$SCRIPT"
elif [ -f "$TARGET_DIR/Makefile" ]; then
  (cd "$TARGET_DIR" && make)
else
  echo "No deployment script found in archive." >&2
fi

