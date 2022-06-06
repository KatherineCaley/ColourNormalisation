from colour_norm.luminosity import get_Lref_mu_sigma, correct_lum
import cv2


def test_luminosity_percentile():
    lum, mu, sigma = get_Lref_mu_sigma(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/reference.jpg",
        95,
    )
    print(lum, mu, sigma)


def test_correct_lum():
    lref, mu, sigma = get_Lref_mu_sigma(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/reference.jpg",
        95,
    )

    im_normalised = correct_lum(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/tile_00005_00102_00637_016.png",
        lref,
        mu,
        sigma,
    )

    cv2.imwrite(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/normalised.jpg",
        im_normalised,
    )
