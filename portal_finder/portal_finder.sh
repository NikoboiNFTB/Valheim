#!/usr/bin/env bash

set -euo pipefail

WORLDS_DIR="$HOME/.config/unity3d/IronGate/Valheim/worlds_local"
COMMAND="/usr/local/bin/valheim_portal_finder"

# Find all world directories and remove backup suffixes.
mapfile -t worlds < <(
	find "$WORLDS_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' |
		sed -E 's/_backup_.*$//' |
		sort -u
)

if ((${#worlds[@]} == 0)); then
	echo "No Valheim worlds found."
	exit 1
fi

# Select the world.
if ((${#worlds[@]} == 1)); then
	world="${worlds[0]}"
else
	echo "Select a Valheim world:"
	echo

	for i in "${!worlds[@]}"; do
		printf '%d) %s\n' "$((i + 1))" "${worlds[i]}"
	done

	echo
	read -rp "Enter number: " selection
	echo

	if ! [[ "$selection" =~ ^[0-9]+$ ]] ||
		((selection < 1 || selection > ${#worlds[@]})); then
		echo "Invalid selection."
		exit 1
	fi

	world="${worlds[$((selection - 1))]}"
fi

WORLD_DIR="$WORLDS_DIR/$world"

echo "Using world: $world"
echo "Directory:  $WORLD_DIR"
echo

cd "$WORLD_DIR"

if [[ -f $COMMAND.py ]]; then
	echo "Local script found, using it." && echo
	python3 $COMMAND.py
else
	echo "Local script not found, using remote." && echo
	python3 <(wget -qO- https://valheim.nikoboi.dev/portal_finder/script.py)
fi
