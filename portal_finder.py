import glob
import mmap
import os

# Hash for portal prefab tag in Valheim ZDO data
PORTAL_HASH = b"\xea\x91|)"


def scan_world_files():
    found_tags = {}

    # Matches both newer .chunk / .db2 files and older .db files
    files = glob.glob("*.chunk") + glob.glob("*.db2") + glob.glob("*.db")

    for filename in files:
        if os.path.getsize(filename) == 0:
            continue

        with open(filename, "rb") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            i = 0
            while True:
                i = mm.find(PORTAL_HASH, i)
                if i == -1:
                    break

                try:
                    # Next byte is length of the tag string
                    tag_len = mm[i + 4]
                    if 0 < tag_len <= 32:  # Sanity check on tag length
                        tag = mm[i + 5 : i + 5 + tag_len].decode(
                            "utf-8", errors="ignore"
                        )
                        if tag and tag.isprintable():
                            if tag not in found_tags:
                                found_tags[tag] = []
                            found_tags[tag].append(filename)
                except Exception:
                    pass

                i += 5

    print("\n--- Portal Tags Found in Save ---")
    for tag, files_list in sorted(found_tags.items()):
        print(f"Tag: '{tag}'  (Found in {len(files_list)} file/chunk[s])")


if __name__ == "__main__":
    scan_world_files()
