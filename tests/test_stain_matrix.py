from colour_norm.stain_matrix import stain_matix_macenko
import numpy as np


##################### CONSTANTS ######################

HE_REF = np.array([[0.5626, 0.2159],
                  [0.7201, 0.8012],
                  [0.4062, 0.5581]])

I = 240 # Transmitted light intensity, Normalizing factor for image intensities
ALPHA = 1  #As recommend in the paper. tolerance for the pseudo-min and pseudo-max (default: 1)
BETA = 0.15 #As recommended in the paper. OD threshold for transparent pixels (default: 0.15)
MAX_C_REF = np.array([1.9705, 1.0308])  ### reference maximum stain concentrations for H&E


def test_stain_matix_macenko():
    HE = stain_matix_macenko(
        "/Users/katherine/repos/ColourNormalisation/tests/test_outputs/test_sample/global_reference.jpg",)
    print(HE)
