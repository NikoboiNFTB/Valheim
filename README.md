# Valheim

Valheim stuff.

> [!NOTE]
> Stuff will be compatible with Valheim 1.0, not older, possibly later.

## Portal Finder

Script for finding all your portals in a world, also highlighting unlinked/inactive portals.

### Usage

Run [`portal_finder.py`](/portal_finder.py) in the Valheim world save folder located here:

```
~/.config/unity3d/IronGate/Valheim/worlds_local/
```

### Example usage and output:

```
user@pc:~/.config/unity3d/IronGate/Valheim/worlds_local/World_Name$ python3 portal_finder.py
Portal Tags Found in World_Name:

Tag: 'Castle'     (Found in 2 file/chunk[s])
Tag: 'NE Outpost' (Found in 2 file/chunk[s])
Tag: 'NW Outpost' (Found in 2 file/chunk[s])
Tag: 'Peninsula'  (Found in 2 file/chunk[s])
user@pc:~/.config/unity3d/IronGate/Valheim/worlds_local/World_Name$
```

> [!NOTE]
> Script must be in the directory for this exact command to work. Just place it there, It's Easy, Mmm'kay.

### Remote Execution

Cool for running without adding any extra files on your PC.

> [!WARNING]
> This only works if you only have one world. Otherwise I think it errors because `cd` has too many args?

```
cd $HOME/.config/unity3d/IronGate/Valheim/worlds_local/
cd $(find . -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sed -E 's/_backup_.*$//' | sort -u)
python3 <(wget -qO- https://valheim.nikoboi.dev/portal_finder.py)
```

> [!NOTE]
> If HTTPS doesn't work yet, try HTTP.

### Fully Automated Script

This is a one tap script. No need to change directories or download or move any files. Just open a terminal and paste this:

```
bash <(wget -qO- https://valheim.nikoboi.dev/portal_finder.sh)
```

> [!NOTE]
> If HTTPS doesn't work yet, try HTTP. Although the script also uses HTTPS to get the Python script, so you might have to do it manually for now. It should work by tomorrow morning, September 15th 2026.

This script will find the worlds for you, and prompt you if you have multiple.

## Contributing

Feel free to fork this repository and submit issues or pull requests if you have any suggestions or improvements. If you encounter any bugs or have feature requests, please open an issue.

## Credits

Created by [**Nikoboi**](https://github.com/NikoboiNFTB/)

## License

This project is licensed under the GNU General Public License V3. See [LICENSE](/LICENSE) for details.
