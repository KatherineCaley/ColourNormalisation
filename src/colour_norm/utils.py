import os, random
import cv2

from math import sqrt


def get_dimensions(n):
    currentDiv = 1
    divisors = [
        currentDiv + 1 for currentDiv in range(n) if n % float(currentDiv + 1) == 0
    ]

    # print divisors this is to ensure that we're choosing well
    hIndex = min(range(len(divisors)), key=lambda i: abs(divisors[i] - sqrt(n)))
    if divisors[hIndex] * divisors[hIndex] == n:
        return divisors[hIndex], divisors[hIndex]

    wIndex = hIndex + 1
    return divisors[hIndex], divisors[wIndex]


def concat_vh(list_2d):

    # return final image
    return cv2.vconcat([cv2.hconcat(list_h) for list_h in list_2d])


def sample_tiles(slide_path: str, n: int, seed=None):

    # assert that there are at least the number of tiles in the slide that we wish to sample
    _, _, files = next(os.walk(slide_path))
    file_count = len(files)
    assert file_count >= n, "There are fewer tiles that requested to sample"

    if seed:
        random.seed(seed)

    chosen_tiles = random.sample(os.listdir(slide_path), n)

    loaded_tiles = [cv2.imread(slide_path + "/" + x) for x in chosen_tiles]

    # find the two largest numbers that multiply to get to n
    x, y = get_dimensions(n)

    list_2D = []
    for i in range(y):
        list_2D.append(loaded_tiles[i * x : i * x + x])

    # concatenate tiles into an image
    img_tile = concat_vh(list_2D)

    # show the output image
    cv2.imshow("concat_vh.jpg", img_tile)

    return img_tile
