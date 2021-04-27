"""
Created on Jan 19, 2020

@Author: Tae-Geun Ji and Soojong PAK
"""

import math
import numpy as np


# ==== Physical Constants
C = 299792500       # Speed of light [m s-1]
h = 6.67259E-34     # Plank constant [J s]
PI = math.pi        # Circular constant
MAX_LINE = 4096

# ==== Instruments Parameters
D_TEL = 10.14           # Telescope aperture [m]
S_ZM = 10**(-56.1/2.5)  # Definition of AB mag [W m-2 Hz-2]
N_RES = 16              # Pixel
N_DARK = 0.02           # Dark current [e s-1 pix-1]
RES_LR = [2550, 3650, 3600, 3600, 1, -1]  # B, G, R, NIR, and Input band in LR: spectral resolution [nm]
WAVE_LR = [482, 626, 900, 1235, 0, 0]     # B, G, R, NIR, and Input band in LR: wavelength [nm]
N_READ_LR = [13.4/math.sqrt(7.2), 13.4/math.sqrt(7.2), 13.4/math.sqrt(7.2), 21.4/math.sqrt(7.2), 0, 0]

# ==== Throughput Parameters: B, G, R, and NIR band of LR
ENCL_LR = 1.000
TEL_MSTR_LR = 0.960
TEL_M1_ZECOAT_LR = [0.937, 0.954, 0.970, 0.966]
TEL_PFHS_LR = 0.987
TEL_WFC_ADC_LR = [0.856, 0.803, 0.849, 0.812]
SIP_POSS_LR = 0.970
SIP_FITS_LMR = [0.784, 0.849, 0.871, 0.809]
SIP_LR = [0.496, 0.534, 0.543, 0.478]
TAU_IE_LR = [0.604, 0.607, 0.648, 0.689]         # Injection efficiency
TAU_ATMO_LR = [1.000, 1.000, 1.000, 1.000]       # Atmospheric transmission (TBD)

# ==== Text Paramters
BAND_LR = ['Blue', 'Green', 'Red', 'NIR', '', '']