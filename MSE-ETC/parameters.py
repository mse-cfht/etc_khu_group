"""
Created on Jan 19, 2020

@Author: Tae-Geun Ji and Soojong PAK
"""

import math
import numpy as np


# Constants

C = 299792500       # velocity          [m s-1]
h = 6.67259E-34     # Plank constant    [J s]
PI = math.pi

# Parameters

D_telescope = 10.14                     # Aperture of the telescope [m]
A_telescope = PI*(D_telescope/2)**2     # Light-collecting area [m2]
S_ZM = 10**(-56.1/2.5)                  # Definition of AB mag [W m-2 Hz-2]
N_res = 16
LR = [2550, 3650, 3600, 3600, 0.]           # Low spectral resolution (Blue, Green, Red, NIR) [nm]

n_dark = [0.02, 0.02, 0.02, 0.02, 0.02]
n_read = [13.4/math.sqrt(7.2), 13.4/math.sqrt(7.2), 13.4/math.sqrt(7.2), 21.4/math.sqrt(7.2), 0.]

# Parameters: MSE Throughput Budgets
# ===== Low resolution mode (Blue, Green, Red, NIR)

ENCL = [1.000, 1.000, 1.000, 1.000, 1.000]
TEL_MSTR = [0.960, 0.960, 0.960, 0.960, 0.960]
TEL_M1_ZeCoat = [0.937, 0.954, 0.970, 0.966, 0.]
TEL_PFHS = [0.987, 0.987, 0.987, 0.987, 0.987]
TEL_WFC_ADC = [0.856, 0.803, 0.849, 0.812, 0.]
SIP_PosS = [0.970, 0.970, 0.970, 0.970, 0.970]
SIP_FiTS_LMR = [0.784, 0.849, 0.871, 0.809, 0.]
SIP_LR = [0.496, 0.534, 0.543, 0.478, 0.]

TAU_opt_LR = np.zeros(5)                            # TAU_optics
for i in range(0, 4):
    TAU_opt_LR[i] = ENCL[i]*TEL_MSTR[i]*TEL_M1_ZeCoat[i]*TEL_PFHS[i] * \
                    TEL_WFC_ADC[i]*SIP_PosS[i]*SIP_FiTS_LMR[i]*SIP_LR[i]

TAU_IE_LR = [0.604, 0.607, 0.648, 0.689, 0.]            # Injection Efficiency
TAU_atmosphere_LR = [1.000, 1.000, 1.000, 1.000, 1.000]    # Atmospheric transmission (TBD)