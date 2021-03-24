from parameters import *
from scipy import interpolate
import numpy as np

Wave_Arr = np.array([360, 370, 400, 482, 626, 767, 900, 910, 950, 962, 1235, 1300, 1500, 1662, 1800])
TEL_M1_ZeCoat_Arr = np.array([0.936, 0.941, 0.959, 0.937, 0.954, 0.954, 0.970, 0.968, 0.958, 0.966, 0.966, 0.975, 0.974, 0.963, 0.963])
TEL_WFC_ADC_Arr = np.array([0.523, 0.594, 0.767, 0.856, 0.803, 0.824, 0.849, 0.849, 0.847, 0.846, 0.812, 0.794, 0.743, 0.675, 0.584])
SIP_FiTS_LMR_Arr = np.array([0.570, 0.605, 0.688, 0.784, 0.849, 0.865, 0.871, 0.871, 0.862, 0.868, 0.809, 0.807, 0.774, 0.810, 0.690])
SIP_LR_Arr = np.array([0.331, 0.396, 0.493, 0.496, 0.534, 0.530, 0.543, 0.511, 0.383, 0.457, 0.478, 0.392, 0.459, 0.438, 0.239])
TAU_IE_LR_Arr = np.array([0.549, 0.572, 0.604, 0.604, 0.607, 0.627, 0.648, 0.650, 0.657, 0.659, 0.689, 0.685, 0.663, 0.581, 0.518])

def ADD_PARAMETERS(wave):
    if wave < 360:
        wave = 360
    elif wave > 1320:
        wave = 1320

    INTERP_TEL_M1_ZeCoat(wave)
    INTERP_TEL_WFC_ADC(wave)
    INTERP_SIP_FiTS_LMR(wave)
    INTERP_SIP_LR(wave)
    INTERP_TAU_IE_LR(wave)
    SELECT_n_read(wave)
    SELECT_LR(wave)

    TAU_opt_LR[4] = ENCL[4] * TEL_MSTR[4] * TEL_M1_ZeCoat[4] * TEL_PFHS[4] * \
                    TEL_WFC_ADC[4] * SIP_PosS[4] * SIP_FiTS_LMR[4] * SIP_LR[4]

def INTERP_TEL_M1_ZeCoat(wave):
    func = interpolate.interp1d(Wave_Arr, TEL_M1_ZeCoat_Arr, kind='cubic')
    TEL_M1_ZeCoat[4] = func(wave)

def INTERP_TEL_WFC_ADC(wave):
    func = interpolate.interp1d(Wave_Arr, TEL_WFC_ADC_Arr, kind='cubic')
    TEL_WFC_ADC[4] = func(wave)

def INTERP_SIP_FiTS_LMR(wave):
    func = interpolate.interp1d(Wave_Arr, SIP_FiTS_LMR_Arr, kind='cubic')
    SIP_FiTS_LMR[4] = func(wave)

def INTERP_SIP_LR(wave):
    func = interpolate.interp1d(Wave_Arr, SIP_LR_Arr, kind='cubic')
    SIP_LR[4] = func(wave)

def INTERP_TAU_IE_LR(wave):
    func = interpolate.interp1d(Wave_Arr, TAU_IE_LR_Arr, kind='cubic')
    TAU_IE_LR[4] = func(wave)

def SELECT_n_read(wave):
    if 360 <= wave <= 900:
        n_read[4] = (13.4/math.sqrt(7.2))
    elif 950 < wave <= 1800:
        n_read[4] = (21.4/math.sqrt(7.2))

def SELECT_LR(wave):
    if 360 <= wave <= 560:
        LR[4] = 2550
    elif 560 < wave <= 740:
        LR[4] = 3650
    elif 715 < wave <= 985:
        LR[4] = 3600
    elif 960 < wave <= 1320:
        LR[4] = 3600

