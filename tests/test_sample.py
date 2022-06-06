import pathlib
import cv2

import pytest

from colour_norm.sample import sample_tiles_wsi, sample_tiles_dataset


def test_sample_tiles_WSI():

    im_concat = sample_tiles_wsi(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027", 12
    )

    cv2.imwrite(
        "/Users/katherine/repos/ColourNormalisation/tests/data/test_outputs/00027/reference.jpg",
        im_concat,
    )
def test_sample_tiles_dataset():

    im_concat = sample_tiles_dataset(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/", 30
    )

    cv2.imwrite(
        "/Users/katherine/repos/ColourNormalisation/tests/data/test_outputs/reference.jpg",
        im_concat,
    )

