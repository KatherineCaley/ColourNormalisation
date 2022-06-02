import pathlib
import cv2

import pytest

from colour_norm.utils import sample_tiles


def test_sample_tiles():

    img = sample_tiles(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027", 12
    )

    cv2.imwrite(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/reference.jpg",
        img,
    )
