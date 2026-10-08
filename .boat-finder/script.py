import ctypes
import math
import os
import struct
from pathlib import Path

# Try importing zstandard for compressed Valheim 1.0 chunk files
try:
    import zstandard as zstd
except ImportError:
    zstd = None

VESSELS = {
    "Raft": "Raft",
    "Karve": "Karve",
    "Longship": "VikingShip",
    "Drakkar": "VikingShip_Ashlands",
}


def c_int32(val: int) -> int:
    return ctypes.c_int32(val).value


def get_stable_hash_code(s: str) -> int:
    """Replicates C# String.GetStableHashCode used by Valheim."""
    hash1 = 5381
    hash2 = 5381
    for i in range(0, len(s), 2):
        hash1 = c_int32(c_int32((hash1 << 5) + hash1) ^ ord(s[i]))
        if i + 1 < len(s):
            hash2 = c_int32(c_int32((hash2 << 5) + hash2) ^ ord(s[i + 1]))
    return c_int32(hash1 + c_int32(hash2 * 1566083941))


def is_valid_vessel_coord(x: float, y: float, z: float) -> bool:
    """Validates real-world game coordinates and filters out origin dummy values (0,0,0)."""
    if any(math.isnan(c) or math.isinf(c) for c in (x, y, z)):
        return False
    # Exclude dummy/uninitialized zero coordinates
    if abs(x) < 0.1 and abs(y) < 0.1 and abs(z) < 0.1:
        return False
    # Map boundaries: ~10,500m radius horizontally, altitude between -100m and 5000m
    return (
        (-10500.0 <= x <= 10500.0)
        and (-100.0 <= y <= 5000.0)
        and (-10500.0 <= z <= 10500.0)
    )


def decompress_data(data: bytes) -> bytes:
    """Decompresses Zstandard binary data if compressed."""
    if zstd and data.startswith(b"\x28\xb5\x2f\xfd"):  # ZSTD magic header
        try:
            dctx = zstd.ZstdDecompressor()
            return dctx.decompress(data, max_output_size=500000000)
        except Exception:
            pass
    return data


def scan_valheim_world(save_dir: str):
    path = Path(save_dir).expanduser()

    if not path.exists():
        print(f"Error: Target path '{path}' does not exist.")
        return

    ship_hashes = {}
    for name, prefab in VESSELS.items():
        h = get_stable_hash_code(prefab)
        ship_hashes[h] = (name, struct.pack("<i", h))

    files_to_scan = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".chunk", ".db2", ".db", ".fw")):
                files_to_scan.append(Path(root) / file)

    print(f"Scanning {len(files_to_scan)} save file(s) in: {path}\n")

    found_ships = set()

    for file_path in files_to_scan:
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()

            data = decompress_data(raw_data)

            for hash_val, (ship_name, pattern) in ship_hashes.items():
                start = 0
                while True:
                    idx = data.find(pattern, start)
                    if idx == -1:
                        break

                    # Check offset patterns preceding m_prefab:
                    # -28 bytes: Vector3 position (12b) + Quaternion rotation (16b)
                    # -24 bytes: Vector3 position (12b) + Vector3 rotation (12b)
                    for offset in (28, 24):
                        if idx >= offset:
                            pos_bytes = data[idx - offset : idx - offset + 12]
                            x, y, z = struct.unpack("<fff", pos_bytes)

                            if is_valid_vessel_coord(x, y, z):
                                coord_key = (
                                    ship_name,
                                    round(x, 1),
                                    round(y, 1),
                                    round(z, 1),
                                )
                                found_ships.add(coord_key)
                                break

                    start = idx + 1

        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")

    # Output
    print("=" * 60)
    print(f"{'SHIP TYPE':<15} | {'X COORD':<10} | {'Y (ALT)':<10} | {'Z COORD':<10}")
    print("=" * 60)

    if not found_ships:
        print("No seafaring vessels were detected in this world save.")
    else:
        for ship_name, x, y, z in sorted(found_ships):
            print(f"{ship_name:<15} | {x:<10.1f} | {y:<10.1f} | {z:<10.1f}")

    print("=" * 60)
    print(f"Total unique ships found: {len(found_ships)}")


if __name__ == "__main__":
    WORLD_SAVE_PATH = "~/.config/unity3d/IronGate/Valheim/worlds_local/Nikoboi"
    scan_valheim_world(WORLD_SAVE_PATH)
