import cv2

import numpy as np
from skimage.io import imread
from skimage.color import rgb2lab, lab2rgb
import matplotlib.pylab as plt
from histomicstk.preprocessing.color_conversion import lab_mean_std
from histomicstk.preprocessing.color_conversion import lab_to_rgb, rgb_to_lab


def get_Lref_mu_sigma(im_scr, pctl: int):
    """
    im_src:
        path to image
    pctl:
        the desired percentile of luminosity you wish to compute.
    """

    im_rgb = cv2.imread(im_scr, 1)
    im_lab = rgb_to_lab(im_rgb)

    rows, cols, _ = im_lab.shape

    luminosities = []

    for i in range(rows):
        for j in range(cols):
            L, A, B = im_lab[i, j]
            luminosities.append(L)

    mean_lab = np.array([im_lab[..., i].mean() for i in range(3)])
    std_lab = np.array([im_lab[..., i].std() for i in range(3)])

    return np.percentile(luminosities, pctl), mean_lab, std_lab


def correct_lum(im_src, Lref95, target_mu, target_sigma):
    """

    im_src:
        path to image
    Lref95:
        the 95th percentile of luminosity from the distribution of pixels in the slide-level reference

    returns
        tile in RGB format rescaled based on global luminosity reference
    """

    im_rgb = cv2.imread(im_src, 1)

    cv2.imwrite(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/im_rgb.jpg",
        im_rgb,
    )

    im_lab = rgb_to_lab(im_rgb)

    # calculate src_mu and src_sigma

    src_mu = [im_lab[..., i].mean() for i in range(3)]
    print(src_mu)
    src_sigma = [im_lab[..., i].std() for i in range(3)]

    # scale to unit variance
    for i in range(3):
        im_lab[:, :, i] = (im_lab[:, :, i] - src_mu[i]) / src_sigma[i]

    # rescale and recenter to match target statistics
    for i in range(3):
        im_lab[:, :, i] = im_lab[:, :, i] * target_sigma[i] + target_mu[i]

    # convert back to RGB colorspace
    im_normalized = lab_to_rgb(im_lab)

    im_normalized[im_normalized > 255] = 255
    im_normalized[im_normalized < 0] = 0

    im_normalized = im_normalized.astype(np.uint8)

    cv2.imwrite(
        "/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/im_normalised.jpg",
        im_normalized,
    )

    return im_normalized
