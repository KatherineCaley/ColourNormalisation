
from colour_norm.luminosity import luminosity_percentile

def test_luminosity_percentile():
    lum = luminosity_percentile("/Users/katherine/repos/ColourNormalisation/tests/data/images_raw/00027/reference.jpg", 95)

    print(lum)
