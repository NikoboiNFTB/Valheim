# Valheim

Valheim stuff.

Stuff will be compatible with Valheim 1.0, not older.

## [Portal Finder](/portal_finder.py)

Script for finding all your portals in a world save.

### Usage

Run [`portal_finder.py`](/portal_finder.py) in the Valheim world save folder located here:

```
~/.config/unity3d/IronGate/Valheim/worlds_local/$WORLD_NAME
```

### Example usage and output:

```
$USER@$PC:~/.config/unity3d/IronGate/Valheim/worlds_local/$WORLD_NAME$ python3 portal_finder.py

--- Portal Tags Found in Save ---
Tag: 'Castle'  (Found in 2 file/chunk[s])
Tag: 'N Island'  (Found in 2 file/chunk[s])
Tag: 'NE Outpost'  (Found in 2 file/chunk[s])
Tag: 'NW Outpost'  (Found in 2 file/chunk[s])
Tag: 'Peninsula'  (Found in 1 file/chunk[s]) # NOTE: This is an example of a portal without a partner, i.e. only found once.
Tag: 'SE Outpost'  (Found in 2 file/chunk[s])
Tag: 'SW Outpost'  (Found in 2 file/chunk[s])
$USER@$PC:~/.config/unity3d/IronGate/Valheim/worlds_local/$WORLD_NAME$
```

### Automated Script (Coming Soon)

You do not need to download and move the script, you can also just run this automated script:

```
COMING SOON
```

## Contributing

Feel free to fork this repository and submit issues or pull requests if you have any suggestions or improvements. If you encounter any bugs or have feature requests, please open an issue.

## Credits

Created by [**Nikoboi**](https://github.com/NikoboiNFTB/)

## License

This project is licensed under the GNU General Public License V3. See [LICENSE](/LICENSE) for details.
