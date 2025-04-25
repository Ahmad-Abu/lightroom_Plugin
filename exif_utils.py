from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = {}

    if not hasattr(image, '_getexif'):
        return exif_data

    exif_raw = image._getexif()
    if exif_raw is None:
        return exif_data

    for tag, value in exif_raw.items():
        decoded_tag = TAGS.get(tag, tag)
        exif_data[decoded_tag] = value

    return exif_data

def is_good_photo(exif_data):
    iso = exif_data.get('ISOSpeedRatings', 100)
    exposure = exif_data.get('ExposureTime', 1/60)
    aperture = exif_data.get('FNumber', 2.8)

    # Example filters (customize these as needed)
    if iso > 1600:
        return False  # Might be too grainy
    if isinstance(exposure, tuple) and (exposure[0] / exposure[1]) > 1/15:
        return False  # Might be too blurry
    return True
