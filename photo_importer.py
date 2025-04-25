import psutil
import os
import shutil
import time
import hashlib
from exif_utils import get_exif_data, is_good_photo


DEST_DIR = os.path.expanduser("~/PycharmProjects/lightroom_Plugin/data/incoming")
IMPORT_LOG = os.path.expanduser("~/PycharmProjects/lightroom_Plugin/data/imported_hashes.txt")

os.makedirs(DEST_DIR, exist_ok = True)
if not os.path.exists(IMPORT_LOG):
    with open(IMPORT_LOG,"w") as f:
        pass

def file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
def load_imported_hashes():
    if os.path.exists(IMPORT_LOG):
        with open(IMPORT_LOG, "r") as f:
         return set(line.strip() for line in f.readlines())
    return set()

def save_imported_hash(hash_val):
    with open(IMPORT_LOG, "a") as f:
        f.write(f"{hash_val}\n")

def import_photos_from_dcim(mountpoint):
    dcim_path = os.path.join(mountpoint, "DCIM")
    print(f"Checking path: {dcim_path}")  # Debugging line to check path

    if not os.path.exists(dcim_path):
        print(f"DCIM folder not found at {dcim_path}")  # Debugging line

        return
    imported_hashes = load_imported_hashes()
    print(f"Imported hashes: {imported_hashes}")  # Check what hashes are loaded

    for root, _, files in os.walk(dcim_path):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".nef")) and not file.startswith("._"):
                print(f"Found file: {file}")  # Confirm the file is found

                src = os.path.join(root, file)
                hash_val = file_hash(src)
                print(f"Hash of {file}: {hash_val}")  # Print the hash to see it's being calculated

                if hash_val in imported_hashes:
                    print(f"Skipping {file}, already imported.")  # File is skipped if its hash is found
                    continue

                exif_data = get_exif_data(src)
                if not is_good_photo(exif_data):
                    print(f"Skipping {file}, low quality based on EXIF.")
                    continue
                dest = os.path.join(DEST_DIR, file)
                shutil.copy2(src, dest)
                save_imported_hash(hash_val)
                print(f"Imported: {file} to {dest}")

def get_mountpoints():
    return [part.mountpoint for part in psutil.disk_partitions(all=False)]

print("Watching for SD cards...")

already_seen = set(get_mountpoints())

while True:
    current = set(get_mountpoints())
    new_drives = current - already_seen
    for drive in new_drives:
        print(f"New drive detected: {drive}")
        import_photos_from_dcim(drive)
    already_seen = current
    time.sleep(1)