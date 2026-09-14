# Valheim

Valheim stuff.

The stuff in question will be compatible with Valheim 1.0, not older, possibly later.

## Portal Finder

Script for finding all your portals in a world, also highlighting unlinked/inactive portals.

> [!NOTE]
> Your world will need to be a local save, Valheim defaults to Cloud save. Fix it in "Manage saves" in the main menu.

### Usage

Run [`portal_finder.py`](/portal_finder.py) in the world save folder. They're located here (on Linux):

```
~/.config/unity3d/IronGate/Valheim/worlds_local/
```

Just put the script in a world folder located there and cd to it and run it like this:

```
python3 portal_finder.py
```

### Fully Automated Script

If you're lazy like me you can use open a terminal and paste this and it'll do everything for you.

```
bash <(wget -qO- https://valheim.nikoboi.dev/portal_finder.sh)
```

> [!NOTE]
> [`valheim.nikoboi.dev`](https://valheim.nikoboi.dev/) resolves to this repository.

This script will find all your worlds and then prompt you if you have multiple, and then run the Python script remotely. It will leave no files behind and won't modify anything.

### Example Output

Running the script directly:

```
user@pc:~/.config/unity3d/IronGate/Valheim/worlds_local/World_Name$ python3 portal_finder.py
Portal Tags Found in World_Name:
Tag: 'Coast'      (Found in 2 file/chunk[s])
Tag: 'NW Outpost' (Found in 2 file/chunk[s])
Tag: 'Peninsula'  (Found in 1 file/chunk[s])
Tag: 'SW Outpost' (Found in 2 file/chunk[s])

Warning[s]:
Tag: 'Peninsula' only found once, missing linked portal.
user@pc:~/.config/unity3d/IronGate/Valheim/worlds_local/World_Name$
```

Running the script remotely:

```
user@pc:~$ bash <(wget -qO- https://valheim.nikoboi.dev/portal_finder.sh)
Using world: World_Name
Directory:  /home/user/.config/unity3d/IronGate/Valheim/worlds_local/World_Name

Portal Tags Found in World_Name:
Tag: 'Coast'      (Found in 2 file/chunk[s])
Tag: 'NW Outpost' (Found in 2 file/chunk[s])
Tag: 'Peninsula'  (Found in 1 file/chunk[s])
Tag: 'SW Outpost' (Found in 2 file/chunk[s])

Warning[s]:
Tag: 'Peninsula' only found once, missing linked portal.
user@pc:~$
```

## Contributing

Feel free to fork this repository and submit issues or pull requests if you have any suggestions or improvements. If you encounter any bugs or have feature requests, please open an issue.

## Credits

Created by [**Nikoboi**](https://github.com/NikoboiNFTB/)

## License

This project is licensed under the GNU General Public License V3. See [LICENSE](/LICENSE) for details.
