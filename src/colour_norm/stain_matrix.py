import numpy as np
import cv2
from matplotlib import pyplot as plt


##################### CONSTANTS ######################

HE_REF = np.array([[0.5626, 0.2159],
                  [0.7201, 0.8012],
                  [0.4062, 0.5581]])

I = 240 # Transmitted light intensity, Normalizing factor for image intensities
ALPHA = 1  #As recommend in the paper. tolerance for the pseudo-min and pseudo-max (default: 1)
BETA = 0.15 #As recommended in the paper. OD threshold for transparent pixels (default: 0.15)
MAX_C_REF = np.array([1.9705, 1.0308])  ### reference maximum stain concentrations for H&E


def stain_matix_macenko(im_src, HERef=None):

    im = cv2.imread(im_src, 1)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    ## use reference H&E OD matrix if not provided
    if not HERef:
        HERef = HE_REF

    ######## Step 1: Convert RGB to OD ###################

    # extract the height, width and num of channels of image
    h, w, c = im.shape

    # reshape image to multiple rows and 3 columns.
    im = im.reshape((-1,3))

    OD = -np.log10((im.astype(np.float)+1) / I)
    #Add 1 in case any pixels in the image have a value of 0 (log 0 is indeterminate)

    ############ Step 2: Remove data with OD intensity less than β ############
    # remove transparent pixels (clear region with no tissue)
    ODhat = OD[~np.any(OD < BETA, axis=1)] #Returns an array where OD values are above beta

    ############# Step 3: Calculate SVD on the OD tuples ######################
    #Estimate covariance matrix of ODhat (transposed)
    # and then compute eigen values & eigenvectors.
    eigvals, eigvecs = np.linalg.eigh(np.cov(ODhat.T))


    ######## Step 4: Create plane from the SVD directions with two largest values ######
    #project on the plane spanned by the eigenvectors corresponding to the two
    # largest eigenvalues
    That = ODhat.dot(eigvecs[:,1:3]) #Dot product

    ############### Step 5: Project data onto the plane, and normalize to unit length ###########
    ############## Step 6: Calculate angle of each point wrt the first SVD direction ########
    #find the min and max vectors and project back to OD space
    phi = np.arctan2(That[:,1],That[:,0])

    minPhi = np.percentile(phi, ALPHA)
    maxPhi = np.percentile(phi, 100 - ALPHA)

    vMin = eigvecs[:,1:3].dot(np.array([(np.cos(minPhi), np.sin(minPhi))]).T)
    vMax = eigvecs[:,1:3].dot(np.array([(np.cos(maxPhi), np.sin(maxPhi))]).T)

    # a heuristic to make the vector corresponding to hematoxylin first and the
    # one corresponding to eosin second
    if vMin[0] > vMax[0]:
        HE = np.array((vMin[:,0], vMax[:,0])).T

    else:
        HE = np.array((vMax[:,0], vMin[:,0])).T

    # rows correspond to channels (RGB), columns to OD values
    Y = np.reshape(OD, (-1, 3)).T

    # determine concentrations of the individual stains
    C = np.linalg.lstsq(HE,Y, rcond=None)[0]

    # normalize stain concentrations
    maxC = np.array([np.percentile(C[0,:], 99), np.percentile(C[1,:],99)])
    tmp = np.divide(maxC, MAX_C_REF)
    C2 = np.divide(C,tmp[:, np.newaxis])

    ###### Step 8: Convert extreme values back to OD space
    # recreate the normalized image using reference mixing matrix

    Inorm = np.multiply(I, np.exp(-HERef.dot(C2)))
    Inorm[Inorm>255] = 254
    Inorm = np.reshape(Inorm.T, (h, w, 3)).astype(np.uint8)


    # Separating H and E components

    H = np.multiply(I, np.exp(np.expand_dims(-HERef[:, 0], axis=1).dot(np.expand_dims(C2[0, :], axis=0))))
    H[H>255] = 254
    H = np.reshape(H.T, (h, w, 3)).astype(np.uint8)

    E = np.multiply(I, np.exp(np.expand_dims(-HERef[:, 1], axis=1).dot(np.expand_dims(C2[1, :], axis=0))))
    E[E>255] = 254
    E = np.reshape(E.T, (h, w, 3)).astype(np.uint8)

    plt.imsave("test_outputs/test_stain_matrix/HnE_normalized.jpg", Inorm)
    plt.imsave("test_outputs/test_stain_matrix/HnE_separated_H.jpg", H)
    plt.imsave("test_outputs/test_stain_matrix/HnE_separated_E.jpg", E)

    return HE


def seperate_h_e():
    return None
