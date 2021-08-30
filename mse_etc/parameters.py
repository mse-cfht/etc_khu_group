"""
Created on Jan 19, 2020

@Author: Tae-Geun Ji and Soojong PAK
"""

from math import pi
from math import sqrt


# ==== Physical Constants
C = 299792500            # Speed of light [m s-1]
h = 6.67259E-34          # Plank constant [J s]

# ==== Instruments Parameters
D_TEL = 10.14            # Telescope diameter [m]
A_TEL = pi*(D_TEL/2)**2  # Light collecting area [m2]
S_ZM = 10**(-56.1/2.5)   # Definition of AB mag [W m-2 Hz-2]
N_RES = 16               # Pixel
N_DARK = 0.02            # Dark current [e s-1 pix-1]

# ==== LR
RES_LR = [2550, 3650, 3600, 3600]  # B, G, R, NIR on LR: Spectral resolution [nm]
CTR_LR = [482, 626, 900, 1235]     # B, G, R, NIR on LR: Central wavelength [nm]
WAVE_BAND_LR = [[360, 560], [540, 740], [715, 985], [960, 1320]]  # B, G, R, NIR on LR: Wavelength range [nm]
WAVE_OVLP_LR = [[540, 560], [715, 740], [960, 985]]               # Overlap range [nm]
N_READ_LR = [13.4/sqrt(7.2), 13.4/sqrt(7.2), 13.4/sqrt(7.2), 21.4/sqrt(7.2)]

# ==== MR
RES_MR = [4400, 6200, 6100, 6000]   # B, G, R, NIR, and Input band in MR: spectral resolution [nm]
CTR_MR = [482, 626, 767]#, 1662]      # B, G, R, NIR, and Input band in MR: wavelength [nm]
WAVE_BAND_MR = [[350, 510], [576, 700], [737, 900], [1457, 1800]]
N_READ_MR = [13.4/sqrt(7.2), 13.4/sqrt(7.2), 13.4/sqrt(7.2), 21.4/sqrt(7.2)]

# ==== HR
RES_HR = [40000, 40000, 20000]  # B, G, R and Input band in LR: spectral resolution [nm]
CTR_HR = [400, 482, 767]        # B, G, R and Input band in LR: wavelength [nm]
WAVE_BAND_HR = [[359, 440], [460, 600], [620, 900]]
WAVE_OVLP_HR = [[440, 460], [600, 620]]
N_READ_HR = [13.4/sqrt(7.2), 13.4/sqrt(7.2), 13.4/sqrt(7.2)]

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

# ==== Throughput Parameters: B, G, R, and NIR band of MR (added by CK)
ENCL_MR = 1.000
TEL_MSTR_MR = 0.960
TEL_M1_ZECOAT_MR = [0.937, 0.954, 0.954, 0.963]
TEL_PFHS_MR = 0.987
TEL_WFC_ADC_MR = [0.856, 0.803, 0.824, 0.675]
SIP_POSS_MR = 0.970
SIP_FITS_MR = [0.784, 0.849, 0.865, 0.810]
SIP_MR_WG = [0.405, 0.483, 0.448, 0]
SIP_MR_WoG = [0.560, 0.608, 0.628, 0]
TAU_IE_MR = [0.606, 0.612, 0.633, 0.574]         # Injection efficiency
TAU_ATMO_MR = [1.000, 1.000, 1.000, 1.000]       # Atmospheric transmission (TBD)

# ==== Throughput Parameters: B, G, R, and NIR band of MR (added by CK)
ENCL_HR = 1.000
TEL_MSTR_HR = 0.960
TEL_M1_ZECOAT_HR = [0.959, 0.937, 0.954, 0]
TEL_PFHS_HR = 0.987
TEL_WFC_ADC_HR = [0.767, 0.856, 0.824, 0]
SIP_POSS_HR = 0.970
SIP_FITS_HR = [0.596, 0.742, 0.875, 0]
SIP_HR_WG = [0.405, 0.354, 0.435, 0]
SIP_HR_WoG = [0.405, 0.415, 0.435, 0]
TAU_IE_HR = [0.426, 0.430, 0.449, 0]         # Injection efficiency
TAU_ATMO_HR = [1.000, 1.000, 1.000, 1.000]       # Atmospheric transmission (TBD)

# ==== Text Parameters: Filter Band
BAND_LR = ['Blue', 'Green', 'Red', 'NIR', '', '']
BAND_MR = ['Blue', 'Green', 'Red', '', '', '']
BAND_HR = ['Blue', 'Green', 'Red', '', '', '']