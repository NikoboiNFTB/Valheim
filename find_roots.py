import glob
import mmap
import os
import struct

# Prefab identifier
PREFAB_NAME = "WrithanRoots"
PREFAB_BYTES = PREFAB_NAME.encode("utf-8")

# Valheim stable hash calculation (GetStableHashCode)
def get_stable_hashcode(text: str) -> int:
    hash_val = 0
    for char in text:
        hash_val = ((hash_val * 31) + ord(char)) & 0xFFFFFFFF
    if hash_val >= 0x80000000:
        hash_val -= 0x100000000
    return hash_val

# Convert hash to 4-byte little-endian binary signature
HASH_INT = get_stable_hashcode(PREFAB_NAME)
HASH_BYTES = struct.pack("<i", HASH_INT)

def scan_for_coordinates():
    files = glob.glob("*.chunk") + glob.glob("*.db2") + glob.glob("*.db")
    if not files:
        print("No chunk or db files found in the current directory.")
        return

    print(f"Target Prefab: {PREFAB_NAME}")
    print(f"Target Hash: {HASH_INT} (Bytes: {HASH_BYTES.hex()})\n")

    matches_found = 0

    for filename in files:
        if os.path.getsize(filename) == 0:
            continue

        with open(filename, "rb") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            
            # Scan for both literal string and binary hash pattern
            for target_pattern, pattern_type in [(HASH_BYTES, "Hash Match"), (PREFAB_BYTES, "String Match")]:
                pos = 0
                while True:
                    pos = mm.find(target_pattern, pos)
                    if pos == -1:
                        break

                    matches_found += 1
                    
                    # Read surrounding memory block to look for candidate float coordinates (x, y, z)
                    # ZDO positions are stored as 3 contiguous 32-bit floats (12 bytes)
                    coords = extract_nearby_floats(mm, pos)
                    
                    print(f"[{pattern_type}] File: {filename} @ Offset: {hex(pos)}")
                    if coords:
                        for idx, (x, y, z) in enumerate(coords):
                            print(f"  └─ Candidate Coords {idx+1}: X={x:.1f}, Y={y:.1f}, Z={z:.1f}")
                    else:
                        print("  └─ No valid coordinate vectors found nearby.")

                    pos += len(target_pattern)

            mm.close()

    if matches_found == 0:
        print("No instances of WrithanRoots were detected in the saved chunk files.")

def extract_nearby_floats(mm, offset, search_range=64):
    """Scans a window before and after the hit offset for plausible Valheim map coordinates."""
    candidates = []
    start_pos = max(0, offset - search_range)
    end_pos = min(len(mm) - 12, offset + search_range)

    for i in range(start_pos, end_pos, 4):
        try:
            x, y, z = struct.unpack("<fff", mm[i:i+12])
            # Valheim maps span roughly -10500 to +10500 on X/Z, and -100 to +1000 on Y
            if -10500.0 <= x <= 10500.0 and -100.0 <= y <= 1000.0 and -10500.0 <= z <= 10500.0:
                # Filter out pure zeros or low-precision garbage floats
                if not (x == 0.0 and y == 0.0 and z == 0.0):
                    candidates.append((round(x, 2), round(y, 2), round(z, 2)))
        except Exception:
            continue
            
    # Deduplicate candidate coordinates
    return list(set(candidates))

if __name__ == "__main__":
    scan_for_coordinates()
