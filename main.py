from photo_importer import watch_for_sd_cards
from face_sorter import sort_faces
# from editor import auto_edit

def main():
    print("Photo Organizer is running...")

    # 1. Import new photos
    watch_for_sd_cards()

    # 2. Once photos are in, run face sorting
    sort_faces()

    # 3. Optional: Run auto-edit on selected photos
    # auto_edit()

if __name__ == "__main__":
    main()