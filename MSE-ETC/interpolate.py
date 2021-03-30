"""This is the interpolation module of MSE ETC.
This module executes....

Modification Log
2020.02.25 - First created by Taeeun Kim
2020.03.24 - Updated by Tae-Geun Ji
2020.03.29 - Updated by Tae-Geun Ji
"""

from parameters import *
from scipy import interpolate
import numpy as np
import time

# change 20210324 by T-G. Ji
class Throughput:

    def __init__(self):

        print('...... Reading skytable for Low Resolution')

        blue_low_path = 'SKY/MSE_AM1_BLUE_2550.dat'
        green_low_path = 'SKY/MSE_AM1_GREEN_3650.dat'
        red_low_path = 'SKY/MSE_AM1_RED_3600.dat'
        nir_low_path = 'SKY/MSE_AM1_NIR_3600.dat'

        self.data_blue_low = np.genfromtxt(blue_low_path, names=('wavelength', 'data1', 'data2', 'data3'))
        self.data_green_low = np.genfromtxt(green_low_path, names=('wavelength', 'data1', 'data2', 'data3'))
        self.data_red_low = np.genfromtxt(red_low_path, names=('wavelength', 'data1', 'data2', 'data3'))
        self.data_nir_low = np.genfromtxt(nir_low_path, names=('wavelength', 'data1', 'data2', 'data3'))

        self.wave_blue = []
        self.wave_green = []
        self.wave_red = []
        self.wave_nir = []

        self.atmo_blue = []
        self.atmo_green = []
        self.atmo_red = []
        self.atmo_nir = []

        self.tau_wave = []
        self.tel_m1_zecoat_arr = []
        self.tel_wfc_adc_arr = []
        self.sip_fits_arr = []
        self.sip_arr = []

        self.data_pwv = [1.0, 2.5, 7.5]
        self.data_atmo = []
        self.tau_atmo = 0
        self.tau_opt = 0
        self.tau_ie = 0

    def set_data(self, res_mode):
        if res_mode == "LR":
            self.wave_blue = self.data_blue_low['wavelength']
            self.wave_green = self.data_green_low['wavelength']
            self.wave_red = self.data_red_low['wavelength']
            self.wave_nir = self.data_nir_low['wavelength']

            nlen = len(self.data_blue_low)
            self.atmo_blue = [[0] * 3 for i in range(nlen)]

            for i in range(0, nlen):
                self.atmo_blue[i] = [self.data_blue_low['data1'][i],
                                     self.data_blue_low['data2'][i],
                                     self.data_blue_low['data3'][i]]

            self.wave_green = self.data_green_low['wavelength']

            nlen = len(self.data_green_low)
            self.atmo_green = [[0] * 3 for i in range(nlen)]

            for i in range(0, nlen):
                self.atmo_green[i] = [self.data_green_low['data1'][i],
                                      self.data_green_low['data2'][i],
                                      self.data_green_low['data3'][i]]

            nlen = len(self.data_red_low)
            self.atmo_red = [[0] * 3 for i in range(nlen)]

            for i in range(0, nlen):
                self.atmo_red[i] = [self.data_red_low['data1'][i],
                                    self.data_red_low['data2'][i],
                                    self.data_red_low['data3'][i]]

            nlen = len(self.data_nir_low)
            self.atmo_nir = [[0] * 3 for i in range(nlen)]

            for i in range(0, nlen):
                self.atmo_nir[i] = [self.data_nir_low['data1'][i],
                                    self.data_nir_low['data2'][i],
                                    self.data_nir_low['data3'][i]]

            data = np.loadtxt("Throughput_LR.dat")

            self.tau_wave = data[:, 0]
            self.tel_m1_zecoat_arr = data[:, 1]
            self.tel_wfc_adc_arr = data[:, 2]
            self.sip_fits_arr = data[:, 3]
            self.sip_arr = data[:, 4]
            self.data_tau_ie = data[:, 5]

    def tau_atmo_blue(self, pwv, wave):
        func = interpolate.interp2d(self.data_pwv, self.wave_blue, self.atmo_blue, kind='linear')
        self.tau_atmo = func(pwv, wave)

        return self.tau_atmo

    def tau_atmo_green(self, pwv, wave):
        func = interpolate.interp2d(self.data_pwv, self.wave_green, self.atmo_green, kind='linear')
        self.tau_atmo = func(pwv, wave)

        return self.tau_atmo

    def tau_atmo_red(self, pwv, wave):
        func = interpolate.interp2d(self.data_pwv, self.wave_red, self.atmo_red, kind='linear')
        self.tau_atmo = func(pwv, wave)

        return self.tau_atmo

    def tau_atmo_nir(self, pwv, wave):
        func = interpolate.interp2d(self.data_pwv, self.wave_nir, self.atmo_nir, kind='linear')
        self.tau_atmo = func(pwv, wave)

        return self.tau_atmo

    def tau_opt_res(self, wave):
        func_tel_m1_zecoat = interpolate.interp1d(self.tau_wave, self.tel_m1_zecoat_arr, kind='cubic')
        func_tel_wfc_adc = interpolate.interp1d(self.tau_wave, self.tel_wfc_adc_arr, kind='cubic')
        func_sip_fits = interpolate.interp1d(self.tau_wave, self.sip_fits_arr, kind='cubic')
        func_sip = interpolate.interp1d(self.tau_wave, self.sip_arr, kind='cubic')

        self.tau_opt = ENCL_LR * TEL_MSTR_LR * func_tel_m1_zecoat(wave) * TEL_PFHS_LR * func_tel_wfc_adc(wave) \
                         * SIP_POSS_LR * func_sip_fits(wave) * func_sip(wave)
        return self.tau_opt

    def tau_ie_res(self, wave):
        func_tau_ie = interpolate.interp1d(self.tau_wave, self.data_tau_ie, kind='cubic')
        self.tau_ie = func_tau_ie(wave)

        return self.tau_ie