# ColourNormalisation

In this repository I attempt to replicate the colour normalisation method described in [Wang et al (2021)](https://aacrjournals.org/cancerres/article/81/19/5115/670326/Predicting-Molecular-Phenotypes-from). Wish me luck! 


## Overview of Their Method

#### STEP ONE: Correct Luminosity
- Create a reference image for **each** Whole Slide Image (WSI), this reference is 100 tiles randomly sampled from a WSI, concatenated to form a single image. 
- Transform reference image from RGB to LAB colour space.
- Determine L<sub>ref95</sub>: the 95th percentile of luminosity from the distribution of pixels in the global reference. 
- Rescale each WSI according to L<sub>ref95</sub>:

    1. RGB to LAB transformation
    2. Luminosity values of pixels exceeding L<sub>ref95</sub> were set to 255 (white)
    3. Luminosity values of all other pixels were linearly rescaled to a range from 0 to 255
    4. LAB to RGB transformation

#### STEP TWO: Find Global Stain Matrix and Saturation Reference
- Create global reference, this reference is 3,000 (luminosity corrected) tiles randomly sampled from across all data sets concatenated to form a single image. 
- Compute the HE stain matrix of the global reference image. 
- Determine S<sub>ref99</sub> for each stain: the 99th percentile of the saturation coefficient from the distribution of pixels in the global reference.

#### STEP THREE: Process each slide
- Create a reference for **each** Whole Slide Image (WSI), this reference is 100 luminosity-corrected tiles randomly sampled from a WSI. 
- Compute the slide specific stain matrices based on these tiles. 
- Each tile for a WSI was then normalised by the following method:
  - the pixel-wise saturation coefficients were extracted based on the slide level stain matrix and the tile’s pixel values in OD space
  - exclude the top 1st percentile of saturation values for each stain and linearly rescaled the remaining values as described by Macenko et al.(5) such that the maximum value matches S<sub>ref99</sub> 
  - apply the global reference stain matrix on the corrected saturation values to obtain normalised pixel values in OD space
