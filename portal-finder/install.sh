#!/usr/bin/env bash

set -e

echo "sudo is needed to install into /usr/local/bin/"

wget -qO- https://valheim.nikoboi.dev/portal-finder/script.sh |
	sudo tee /usr/local/bin/valheim_portal_finder >/dev/null
sudo chmod 755 /usr/local/bin/valheim_portal_finder

wget -qO- https://valheim.nikoboi.dev/portal-finder/script.py |
	sudo tee /usr/local/bin/valheim_portal_finder.py >/dev/null
sudo chmod 755 /usr/local/bin/valheim_portal_finder.py

echo "Successfully installed script.sh and script.py as valheim_portal_finder and valheim_portal_finder.py, respectively."
