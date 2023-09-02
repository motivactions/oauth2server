import uuid
import os
from io import BytesIO

from PIL import Image


def path_and_rename_prefix(instance, filename, upload_to):
    filename_structure = filename.split(".")
    ext = filename_structure.pop(-1)
    filename_base = "-".join(filename_structure)
    filename = "{}_{}.{}".format(filename_base, uuid.uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def create_image(
    filename="example.png", size=(100, 100), image_mode="RGB", image_format="PNG"
):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    image = BytesIO()
    Image.new(image_mode, size).save(image, image_format)
    image.seek(0)
    image.name = filename
    return image
