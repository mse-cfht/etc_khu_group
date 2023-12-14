"""Interpolation module"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

LR_wave = []
LR_tel_m1_zecoat_arr = []
LR_tel_wfc_adc_arr = []
LR_sip_fits_arr = []
LR_sip_arr = []
LR_sip_no_grating_arr = []

MR_wave = []
MR_sip_fits_arr = []
MR_sip_arr = []
MR_sip_no_grating_arr = []

HR_wave = []
HR_sip_fits_arr = []
HR_sip_arr = []
HR_sip_no_grating_arr = []

data = np.loadtxt("tau_opt/Throughput_LR.dat")

LR_wave = data[:, 0]
LR_tel_m1_zecoat_arr = data[:, 1]
LR_tel_wfc_adc_arr = data[:, 2]
LR_sip_fits_arr = data[:, 3]
LR_sip_arr = data[:, 4]

LR_func_tel_m1_zecoat = interpolate.interp1d(LR_wave, LR_tel_m1_zecoat_arr, kind='linear')
LR_func_tel_wfc_adc = interpolate.interp1d(LR_wave, LR_tel_wfc_adc_arr, kind='linear', fill_value="extrapolate")
LR_func_sip_fits = interpolate.interp1d(LR_wave, LR_sip_fits_arr, kind='linear', fill_value="extrapolate")
LR_func_sip_arr = interpolate.interp1d(LR_wave, LR_sip_arr, kind='linear')

LR_wave_arr = np.arange(360, 1800, 0.1)
tel_m1_zecoat_arr_new = LR_func_tel_m1_zecoat(LR_wave_arr)
tel_wfc_adc_new = LR_func_tel_wfc_adc(LR_wave_arr)
sip_fits_new = LR_func_sip_fits(LR_wave_arr)
sip_arr_new = LR_func_sip_arr(LR_wave_arr)

data = np.loadtxt("tau_opt/Throughput_MR.dat")

MR_wave = data[:, 0]
MR_sip_fits_arr = data[:, 3]
MR_sip_arr = data[:, 4]
HR_sip_no_grating_arr = data[:, 6]

MR_func_sip_fits = interpolate.interp1d(MR_wave, MR_sip_fits_arr, kind='linear', fill_value="extrapolate")
MR_func_sip_arr = interpolate.interp1d(MR_wave, MR_sip_arr, kind='linear', fill_value="extrapolate")
MR_func_sip_no_grating_arr = interpolate.interp1d(MR_wave, HR_sip_no_grating_arr, kind='linear', fill_value="extrapolate")

MR_wave_arr = np.arange(360, 950+0.1, 0.1)
MR_wave_arr2 = np.arange(400, 900+0.1, 0.1)
MR_sip_fits_new = MR_func_sip_fits(MR_wave_arr)
MR_sip_arr_new = MR_func_sip_arr(MR_wave_arr2)
MR_sip_no_grating_arr_new = MR_func_sip_no_grating_arr(MR_wave_arr)

data = np.loadtxt("tau_opt/Throughput_HR.dat")

HR_wave = data[:, 0]
HR_sip_fits_arr = data[:, 3]
HR_sip_arr = data[:, 4]
HR_sip_no_grating_arr = data[:, 6]

HR_func_sip_fits = interpolate.interp1d(HR_wave, HR_sip_fits_arr, kind='linear', fill_value="extrapolate")
HR_func_sip_arr = interpolate.interp1d(HR_wave, HR_sip_arr, kind='linear', fill_value="extrapolate")
HR_func_sip_no_grating_arr = interpolate.interp1d(HR_wave, HR_sip_no_grating_arr, kind='linear', fill_value="extrapolate")

HR_wave_arr = np.arange(360, 900+0.1, 0.1)
HR_sip_fits_new = HR_func_sip_fits(HR_wave_arr)
HR_sip_no_grating_arr_new = HR_func_sip_no_grating_arr(HR_wave_arr)

# plot
plt.figure(num=None, figsize=(15, 7), dpi=160, facecolor='w', edgecolor='k')
ax = plt.subplot(111)
ax.plot(LR_wave_arr, tel_m1_zecoat_arr_new, 'black', linewidth=2, label='black')
ax.plot(LR_wave_arr, tel_wfc_adc_new, 'orange', linewidth=2, label='orange')

ax.plot(LR_wave_arr, sip_fits_new, 'red', linewidth=2, label='red')
ax.plot(HR_wave_arr, HR_sip_fits_new, 'red', linewidth=2, label='red', linestyle='dotted')

ax.plot(LR_wave_arr, sip_arr_new, 'green', linewidth=2, label='green')
ax.plot(MR_wave_arr2, MR_sip_arr_new, 'blue', linewidth=2, label='blue', linestyle='dashed')
ax.plot(MR_wave_arr, MR_sip_no_grating_arr_new, 'blue', linewidth=2, label='blue')
ax.plot(HR_wave_arr, HR_sip_no_grating_arr_new, 'purple', linewidth=2, label='purple')

plt.xlim([360, 1800])
plt.ylim([0, 1.0])
plt.legend(['ZeCoat', 'WFC/ADC', 'FiTS (LR/MR)', 'FiTS (HR)', 'SIP (LR)', 'SIP (MR with Grating)', 'SIP (MR without Grating)', 'SIP (HR without Grating)'], fontsize=10)
plt.title('MSE Optical Throughput', fontsize=16)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel('Wavelength (nm)', fontsize=16)
plt.ylabel('Throughput', fontsize=16)

plt.show()

# ax.plot(data_wave2, data_atmo2, 'red', linewidth=1, label='red')
# ax.plot(data_wave2, result, 'blue', linewidth=1, label='blue')