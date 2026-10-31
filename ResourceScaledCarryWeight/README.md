> [!NOTE]
> [/ResourceScaledCarryWeight](/ResourceScaledCarryWeight/) and this [README.md](/ResourceScaledCarryWeight/README.md) are completely ChatGPT.

# Resource Scaled Carry Weight

A client-side BepInEx 5 plugin for Valheim. It scales the complete carry-weight result (base capacity plus status-effect bonuses) to the world's `Resources` rate.

Examples:

- Resources 1.0x: base 300, Megingjord +150, Moder +300, Troll Endurance +250, Corpse Run +150
- Resources 1.5x: base 450, Megingjord +225, Moder +450, Troll Endurance +375, Corpse Run +225
- Resources 3.0x: base 900, Megingjord +450, Moder +900, Troll Endurance +750, Corpse Run +450

The plugin discovers status effects by their `SE_Stats.m_addMaxCarryWeight` value, rather than maintaining a hard-coded list. It updates the descriptions of every status effect with a positive carry-weight bonus and the Megingjord item description.

## Build on Linux

Install the .NET SDK, then build from the repository root. This project needs two separate directories because r2modman keeps the active BepInEx files in its profile, while the Valheim game assemblies live in the Steam installation.

For the r2modman Default profile and the paths supplied in the project setup:

```bash
dotnet build -c Release \
  -p:BepInExDir="/home/$USER/.var/app/io.github.ebkr.r2modman/config/r2modmanPlus-local/Valheim/profiles/Default/BepInEx/core" \
  -p:GameManagedDir="/media/$USER/2 TB Volume/SteamLibrary/steamapps/common/Valheim/valheim_Data/Managed"
```

The compiled plugin is:

`bin/Release/netstandard2.1/ResourceScaledCarryWeight.dll`

If you use another r2modman profile, change `BepInExDir` to that profile's `BepInEx/core` directory. Do not use r2modman's `cache/denikson-BepInExPack_Valheim/...` directory as the build reference: it is the cached package source, not the active profile installation.

The project references game and BepInEx assemblies but does not copy them into the plugin output.

## Install with r2modman

1. Select the Valheim profile in r2modman.
2. Choose **Settings > Browse profile folder**.
3. Open `BepInEx/plugins`.
4. Create `ResourceScaledCarryWeight`.
5. Copy `ResourceScaledCarryWeight.dll` into that folder.
6. Launch using **Start modded**.

Expected layout:

```text
<r2modman profile>/
└── BepInEx/
    └── plugins/
        └── ResourceScaledCarryWeight/
            └── ResourceScaledCarryWeight.dll
```

Do not copy BepInEx, Harmony, Unity or Valheim assemblies into the plugin folder.

## Open-source repository contents

Commit the source project files, for example:

```text
.gitignore
LICENSE
README.md
ResourceScaledCarryWeight.csproj
src/Plugin.cs
```

Choose a license for your own code and add its corresponding `LICENSE` file. Do not commit or redistribute `BepInEx.dll`, `0Harmony.dll`, `assembly_valheim.dll`, `UnityEngine.CoreModule.dll`, or other proprietary game assemblies. They are local build references, not project source. The `.gitignore` excludes DLLs and build output.

## Important testing notes

- Version 0.2.0 source has not been compiled against your local Valheim installation or tested in-game.
- It expects the installed Valheim assembly to expose the fields and methods used in the source. If Iron Gate changes these APIs, compilation or the BepInEx log will identify the failed lookup or patch.
- Effects implemented through a different carry-weight mechanism will not be discovered by the generic status-effect scan.
- If another mod changes carry capacity or the same tooltip fields, patch/load order can matter.
- Install it on each client that should receive the behaviour. It does not alter the world save or install anything on a dedicated server.
