#!/bin/bash
# ZEDEC Codex Schema v3 - Full Sync and Broadcast Activation for Debian 12
# This script follows the high level schema to fetch data from public sources,
# distribute it across local volumes and object storage, and regenerate the
# manifest file.

set -euo pipefail

SCHEMA_VERSION="3.0.0-ZADAC-DEBIAN12"
NODE_ID="ZADAC"
GLYPH="36N9-PRIME"
BASE_DIR="/opt/zedec-v3"
SOURCE_DIR="$BASE_DIR/source"
DATA_DIR="$BASE_DIR/data"
MANIFEST="$BASE_DIR/manifest.v3.json"

GIT_REPO="https://github.com/transmutationist/zedec-post-quantum-os"
PCLOUD_URL="https://u.pcloud.link/publink/show?code=kZJNRf5ZJG08Ck9uIKXLjqtmUDNU9BqsECi7"

mkdir -p "$SOURCE_DIR" "$DATA_DIR"

# Fetch source from GitHub
if [ ! -d "$SOURCE_DIR/.git" ]; then
  echo "Cloning source repository..."
  git clone "$GIT_REPO" "$SOURCE_DIR"
else
  echo "Updating source repository..."
  git -C "$SOURCE_DIR" pull
fi

# Fetch data from pCloud and extract
TEMP_TAR="$BASE_DIR/data.tgz"
if wget -O "$TEMP_TAR" "$PCLOUD_URL"; then
  if [ -s "$TEMP_TAR" ]; then
    echo "Extracting data archive..."
    tar -C "$DATA_DIR" -xf "$TEMP_TAR"
  else
    echo "Downloaded archive is empty; skipping extraction." >&2
  fi
else
  echo "Failed to download data from pCloud." >&2
fi
rm -f "$TEMP_TAR"

# Distribute files to mounted volumes if they exist
for target in "/ZADAC/zedec-source" "/36N9/zedec-data" "/mnt/object-storage/zedec-sync"; do
  if [ -d "$target" ]; then
    echo "Syncing data to $target ..."
    rsync -a "$DATA_DIR/" "$target/"
  else
    echo "Target $target not found; skipping." >&2
  fi
done

# Push to object storage using rclone if configured
if command -v rclone >/dev/null 2>&1; then
  rclone copy "$DATA_DIR" remotebucket:zedec-data
  rclone copy "$SOURCE_DIR" remotebucket:zedec-source
else
  echo "rclone not installed; skipping object storage push." >&2
fi

# Regenerate manifest
cat > "$MANIFEST" <<JSON
{
  "node": "$NODE_ID",
  "glyph": "$GLYPH",
  "schema": "$SCHEMA_VERSION",
  "cid": "auto",
  "pulse": "http://178.156.185.180/pulse",
  "mirrors": {
    "github": "$GIT_REPO",
    "pcloud": "$PCLOUD_URL",
    "local": "$DATA_DIR"
  },
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON

# Optionally broadcast to codex endpoints (requires curl)
if [ "${ZEDEC_BROADCAST:-}" = "1" ]; then
  if command -v curl >/dev/null 2>&1; then
    echo "Broadcasting manifest to Codex..."
    curl -X POST -H 'Content-Type: application/json' \
      --data-binary "@$MANIFEST" "https://codex.mesh/ingest" || true
  else
    echo "curl not found; cannot broadcast." >&2
  fi
fi

echo "Sync complete. Manifest written to $MANIFEST"
