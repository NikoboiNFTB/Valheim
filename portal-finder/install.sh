#!/usr/bin/env bash

set -e

echo "sudo is needed to install into /usr/local/bin/"

sudo install -m 755 <(wget -qO- https://valheim.nikoboi.dev/portal-finder/script.sh) /usr/local/bin/valheim_portal_finder
sudo install -m 755 <(wget -qO- https://valheim.nikoboi.dev/portal-finder/script.py) /usr/local/bin/valheim_portal_finder.py

echo "Successfully installed script.sh and script.py as valheim_portal_finder and valheim_portal_finder.py, respectively."
