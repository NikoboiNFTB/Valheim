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

                    if 0 < tag_len <= 32:
                        tag = mm[i + 5 : i + 5 + tag_len].decode(
                            "utf-8", errors="ignore"
                        )

                        if tag and tag.isprintable():
                            if tag not in found_tags:
                                found_tags[tag] = {
                                    "occurrences": 0,
                                    "files": set(),
                                }

                            found_tags[tag]["occurrences"] += 1
                            found_tags[tag]["files"].add(filename)

                except Exception:
                    pass

                i += 5

            mm.close()

    world_save_name = os.path.basename(os.getcwd())

    print(f"Portal Tags Found in {world_save_name}:\n")

    if not found_tags:
        print("No portal tags found.")
        return

    # Align the "(Found in...)" column.
    tag_width = max(len(tag) for tag in found_tags)

    for tag, data in sorted(found_tags.items()):
        print(
            f"Tag: '{tag}'".ljust(tag_width + 8)
            + f"(Found in {data['occurrences']} file/chunk[s])"
        )

    # A portal should normally have two matching endpoints.
    missing = [
        tag for tag, data in sorted(found_tags.items()) if data["occurrences"] == 1
    ]

    if missing:
        print("\nWarning:")
        for tag in missing:
            print(f"Tag: '{tag}' only found once, missing linked portal.")


if __name__ == "__main__":
    scan_world_files()
