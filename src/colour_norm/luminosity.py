import cv2

import numpy as np


def luminosity_percentile(img, pctl: int):

    img = cv2.imread(img, 1)
    rows, cols, _ = img.shape

    luminosities = []

    for i in range(rows):
        for j in range(cols):
            R, G, B = img[i, j]
            luminosities.append(sum([R, G, B]) / 3)

    return np.percentile(luminosities, pctl)
