import os, random
import cv2

from math import sqrt


def get_dimensions(n):
    currentDiv = 1
    divisors = [
        currentDiv + 1 for currentDiv in range(n) if n % float(currentDiv + 1) == 0
    ]

    hIndex = min(range(len(divisors)), key=lambda i: abs(divisors[i] - sqrt(n)))
    if divisors[hIndex] * divisors[hIndex] == n:
        return divisors[hIndex], divisors[hIndex]

    wIndex = hIndex + 1
    return divisors[hIndex], divisors[wIndex]


def concat_vh(list_2d):

    return cv2.vconcat([cv2.hconcat(list_h) for list_h in list_2d])


def sample_tiles_wsi(wsi_src: str, n: int, seed=None):

    # assert that there are at least the number of tiles in the slide that we wish to sample
    _, _, files = next(os.walk(wsi_src))
    file_count = len(files)
    assert file_count >= n, "There are fewer tiles than requested to sample"

    if not seed:
        random.seed(seed)

    chosen_tiles = random.sample(os.listdir(wsi_src), n)

    loaded_tiles = [cv2.imread(wsi_src + "/" + x) for x in chosen_tiles]

    # find the two largest numbers that multiply to get to the number of tiles
    x, y = get_dimensions(n)

    list_2D = []
    for i in range(y):
        list_2D.append(loaded_tiles[i * x : i * x + x])

    # concatenate tiles into an image
    im_concat = concat_vh(list_2D)

    # show the output image
    cv2.imshow("concat_vh.jpg", im_concat)

    return im_concat


def sample_tiles_dataset(data_src: str, n: int, seed=None):

    # todo: assert that there are at least the number of tiles in the dataset that we wish to sample from

    if not seed:
        random.seed(seed)

    chosen_wsis = random.choices(os.listdir(data_src), k=n)

    chosen_tiles = [(random.choice(os.listdir(data_src + x)), x) for x in chosen_wsis]

    loaded_tiles = [cv2.imread(data_src + "/" + x[1] + "/" + x[0]) for x in chosen_tiles]

    x, y = get_dimensions(n)

    list_2D = []
    for i in range(y):
        list_2D.append(loaded_tiles[i * x : i * x + x])

    # concatenate tiles into an image
    im_concat = concat_vh(list_2D)

    return im_concat

