"""Function module of MSE ETC.

Modification Log:
    * 2021.01.19 - The first MSE-ETC version was created by Tae-Geun Ji & Soojong Pak
    * 2021.03.24 - Updated by Tae-Geun Ji
    * 2021.03.29 - Updated by Tae-Geun Ji
    * 2021.04.09 - Updated by Hojae Ahn
    * 2021.04.21 - Updated by Mingyoeng Yang
    * 2021.04.26 - Updated by Mingyeong Yang
    * 2021.05.18 - Updated by Changgon Kim
    * 2021.06.03 - Updated by Hojae Ahn
    * 2021.06.17 - Updated by Tae-Geun Ji
    * 2021.08.04 - Updated by Changgon Kim
    * 2021.09.06 - Updated by Changgon Kim
    * 2023.06.13 - Updated by Tae-Geun Ji
"""

from math import sqrt

import numpy as np
import time
import interpolate
import output
from parameters import *
from copy import deepcopy


class Functions:

    def __init__(self):

        self.snr_arr = [[], []]
        self.res = []
        self.wave = []
        self.n_read = []

        self.wave_grid = []
        self.sky_bg = np.array([])
        self.signal = []
        self.noise = []
        self.snr = []

        self.sn_table = []
        self.exp_table = []

        self.snr_blue = []
        self.snr_green = []
        self.snr_red = []
        self.snr_nir = []

        self.wave_blue = []
        self.wave_green = []
        self.wave_red = []
        self.wave_nir = []

        self.tau_atmo = []
        self.tau_opt = []
        self.tau_ie = []
        self.tau = []

        self.tel_data = []

        self.wave_order1 = []
        self.wave_order2 = []
        self.snr_order1 = []
        self.snr_order2 = []

        self.find = False
        self.overlap = False

        self.tau_func = interpolate.Throughput()

    def cal_signal_to_noise(self, res_mode, airmass, pwv, exp_t, exp_n, mag, sky, input_wave, print_text):
        self.tau_func.set_data(res_mode)

        n = 0
        index = 6
        self.overlap = False

        self.res = np.zeros(index)
        self.wave = np.zeros(index)
        self.n_read = np.zeros(index)

        self.sky_bg = np.zeros(index)
        self.sky_bg_te = np.zeros(index)
        self.tel_data = np.zeros(index)
        self.signal = np.zeros(index)
        self.noise = np.zeros(index)
        self.snr = np.zeros(index)

        self.tau_atmo = np.zeros(index)
        self.tau_opt = np.zeros(index)
        self.tau_ie = np.zeros(index)
        self.tau = np.zeros(index)

        if res_mode == "LR":

            n = len(CTR_LR)
            num = len(WAVE_OVLP_LR)

            for i in range(index):
                if i < n:
                    self.res[i] = RES_LR[i]
                    self.wave[i] = CTR_LR[i]
                    self.n_read[i] = N_READ_LR[i]
                else:
                    self.wave[i] = input_wave

            for i in range(num):
                if WAVE_OVLP_LR[i][0] <= input_wave <= WAVE_OVLP_LR[i][1]:
                    self.res[n] = RES_LR[i]
                    self.res[n + 1] = RES_LR[i + 1]
                    self.n_read[n] = N_READ_LR[i]
                    self.n_read[n + 1] = N_READ_LR[i + 1]
                    BAND_LR[n] = BAND_LR[i]
                    BAND_LR[n + 1] = BAND_LR[i + 1]

                    self.overlap = True

            if self.overlap is False:
                for i in range(n):
                    if WAVE_BAND_LR[i][0] <= input_wave <= WAVE_BAND_LR[i][1]:
                        self.res[n] = RES_LR[i]
                        self.res[n + 1] = RES_LR[i]
                        self.n_read[n] = N_READ_LR[i]
                        self.n_read[n + 1] = N_READ_LR[i]
                        BAND_LR[n] = BAND_LR[i]
                        BAND_LR[n + 1] = BAND_LR[i]

        elif res_mode == "MR":

            n = len(CTR_MR)

            for i in range(index):
                if i < n:
                    self.res[i] = RES_MR[i]
                    self.wave[i] = CTR_MR[i]
                    self.n_read[i] = N_READ_MR[i]
                else:
                    self.wave[i] = input_wave

            for i in range(n):
                if WAVE_BAND_MR[i][0] <= input_wave <= WAVE_BAND_MR[i][1]:
                    self.res[n] = RES_MR[i]
                    self.res[n + 1] = RES_MR[i]
                    self.res[n + 2] = RES_MR[i]
                    self.n_read[n] = N_READ_MR[i]
                    self.n_read[n + 1] = N_READ_MR[i]
                    self.n_read[n + 2] = N_READ_MR[i]
                    BAND_MR[n] = BAND_MR[i]
                    BAND_MR[n + 1] = BAND_MR[i]
                    BAND_MR[n + 2] = BAND_MR[i]

        elif res_mode == "HR":

            n = len(CTR_HR)
            num = len(WAVE_OVLP_HR)

            for i in range(index):
                if i < n:
                    self.res[i] = RES_HR[i]
                    self.wave[i] = CTR_HR[i]
                    self.n_read[i] = N_READ_HR[i]
                else:
                    self.wave[i] = input_wave

            for i in range(num):
                if WAVE_OVLP_HR[i][0] <= input_wave <= WAVE_OVLP_HR[i][1]:
                    self.res[n] = RES_HR[i]
                    self.res[n + 1] = RES_HR[i + 1]
                    self.res[n + 1] = RES_HR[i + 2]
                    self.n_read[n] = N_READ_HR[i]
                    self.n_read[n + 1] = N_READ_HR[i + 1]
                    self.n_read[n + 2] = N_READ_HR[i + 2]
                    BAND_HR[n] = BAND_HR[i]
                    BAND_HR[n + 1] = BAND_HR[i + 1]
                    BAND_HR[n + 2] = BAND_HR[i + 2]

                    self.overlap = True

            if self.overlap is False:
                for i in range(n):
                    if WAVE_BAND_HR[i][0] <= input_wave <= WAVE_BAND_HR[i][1]:
                        self.res[n] = RES_HR[i]
                        self.res[n + 1] = RES_HR[i]
                        self.res[n + 2] = RES_HR[i]
                        self.n_read[n] = N_READ_HR[i]
                        self.n_read[n + 1] = N_READ_HR[i]
                        self.n_read[n + 2] = N_READ_HR[i]
                        BAND_HR[n] = BAND_HR[i]
                        BAND_HR[n + 1] = BAND_HR[i]
                        BAND_HR[n + 2] = BAND_HR[i]

        for i in range(index):
            if res_mode == "LR":
                if BAND_LR[i] == "NIR":
                    self.tel_data[i] = self.tau_func.telluric_emission(self.wave[i])
                self.tau_atmo[i] = self.tau_func.get_tau_atmo_LR(BAND_LR[i], airmass, pwv, self.wave[i])
            elif res_mode == "MR":
                self.tau_atmo[i] = self.tau_func.get_tau_atmo_MR(BAND_MR[i], airmass, pwv, self.wave[i])
            elif res_mode == "HR":
                self.tau_atmo[i] = self.tau_func.get_tau_atmo_HR(BAND_HR[i], airmass, pwv, self.wave[i])

            self.tau_opt[i] = self.tau_func.tau_opt_res(self.wave[i], False)
            self.tau_ie[i] = self.tau_func.tau_ie_res(self.wave[i])
            self.tau[i] = self.tau_atmo[i] * self.tau_opt[i] * self.tau_ie[i]

        for i in range(index):
            self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM * 10.0 ** (-0.4 * mag[i]) / (h * self.res[i])
            self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau_opt[i] * self.tau_atmo[i] * OMEGA \
                             * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * self.res[i])
            if res_mode == "LR":
                if BAND_LR[i] == "NIR":
                    self.sky_bg_te[i] = (exp_t * exp_n) * A_TEL * self.tau_opt[i] * self.tau_atmo[i] * OMEGA * self.tel_data[i]
                else:
                    self.sky_bg_te[i] = 0.0
            self.noise[i] = sqrt(self.signal[i] + self.sky_bg[i] + self.sky_bg_te[i] + N_RES * exp_n * (exp_t * N_DARK + self.n_read[i] ** 2))
            self.snr[i] = self.signal[i] / self.noise[i]

        if print_text is True:
            output.display_single(res_mode, airmass, pwv, exp_t, exp_n, mag, sky, self.snr, input_wave, self.overlap)

        return self.snr  # add 210408 hojae

    def cal_exp_time(self, res_mode, airmass, pwv, target_sn, mag, sky, input_wave):  # add 210408 hojae

        self.exp_table = np.zeros(len(mag))
        self.sn_table = []

        if res_mode == "LR":
            for idx in range(1, 5):  # from 10 to 10,000
                self.sn_table.append(self.cal_signal_to_noise(res_mode, airmass, pwv, 10 ** idx, 1, mag, sky, input_wave, False))
            sn_table = np.array(self.sn_table)

            # for B
            for band in range(len(mag) - 1):
                if sn_table[0, band] > target_sn:
                    output.display_simple_text(
                        "Required exposure time of band %d single frame is shorter than 10 seconds." % band)
                    return None
                elif (sn_table[0, band] <= target_sn) & (target_sn <= sn_table[1, band]):
                    self.exp_table[band] = self.solve_bisection(band, target_sn, 10, 100, res_mode, airmass, pwv, mag, sky,
                                                                input_wave)
                elif (sn_table[1, band] <= target_sn) & (target_sn <= sn_table[2, band]):
                    self.exp_table[band] = self.solve_bisection(band, target_sn, 100, 1000, res_mode, airmass, pwv, mag, sky,
                                                                input_wave)
                elif (sn_table[2, band] <= target_sn) & (target_sn <= sn_table[3, band]):
                    self.exp_table[band] = self.solve_bisection(band, target_sn, 1000, 10000, res_mode, airmass, pwv, mag, sky,
                                                                input_wave)
                else:
                    output.display_simple_text(
                        "Required exposure time of band %d single frame is longer than 10,000 seconds(~3 hours)." % band)
                    return None

        elif res_mode == "HR" or res_mode == "MR":
            for idx in range(1, 5):  # from 10 to 10,000
                self.sn_table.append(self.cal_signal_to_noise(res_mode, airmass, pwv, 10 ** idx, 1, mag, sky, input_wave, False))
            sn_table = np.array(self.sn_table)

            # for B
            for band in range(len(mag) - 1):
                if sn_table[0, band] > target_sn:
                    output.display_simple_text(
                        "Required exposure time of band %d single frame is shorter than 10 seconds." % band)
                    return None
                elif (sn_table[0, band] <= target_sn) & (target_sn <= sn_table[1, band]):
                    self.exp_table[band] = self.solve_bisection(band, target_sn, 10, 100, res_mode, airmass, pwv, mag, sky,
                                                                input_wave)
                elif (sn_table[1, band] <= target_sn) & (target_sn <= sn_table[2, band]):
                    self.exp_table[band] = self.solve_bisection(band, target_sn, 100, 1000, res_mode, airmass, pwv, mag, sky,
                                                                input_wave)
                elif (sn_table[2, band] <= target_sn) & (target_sn <= sn_table[3, band]):
                    self.exp_table[band] = self.solve_bisection(band, target_sn, 1000, 10000, res_mode, pwv, airmass, mag, sky,
                                                                input_wave)
                elif sn_table[0, band] * sn_table[1, band] * sn_table[2, band] * sn_table[3, band] == 0:
                    continue
                else:
                    output.display_simple_text(
                        "Required exposure time of band %d single frame is longer than 10,000 seconds(~3 hours)." % band)
                    return None

        output.display_exp_time(res_mode, airmass, pwv, target_sn, mag, sky, self.exp_table, input_wave, self.overlap)
        return self.exp_table

    def solve_bisection(self, band, target_sn, x_min, x_max, res_mode, airmass, pwv, mag, sky, input_wave,):
        func_min = self.cal_signal_to_noise(res_mode, airmass, pwv, x_min, 1, mag, sky, input_wave, False)[band] - target_sn
        func_max = self.cal_signal_to_noise(res_mode, airmass, pwv, x_max, 1, mag, sky, input_wave, False)[band] - target_sn

        if func_min * func_max > 0:
            return -1  # input error

        for idx in range(30):  # maximum iteration=30
            func_min = self.cal_signal_to_noise(res_mode, airmass, pwv, x_min, 1, mag, sky, input_wave, False)[band] - target_sn
            func_max = self.cal_signal_to_noise(res_mode, airmass, pwv, x_max, 1, mag, sky, input_wave, False)[band] - target_sn

            x_iter = (x_min + x_max) * 0.5
            func_iter = self.cal_signal_to_noise(res_mode, airmass, pwv, x_iter, 1, mag, sky, input_wave, False)[band] - target_sn

            if np.abs(func_min - func_max) < 0.005 * target_sn:  # convergence tolerance = 0.5% of SN
                return x_iter

            if func_min * func_iter < 0:
                x_max = x_iter

            elif func_iter * func_max < 0:
                x_min = x_iter

            else:
                return x_iter
        return -999  # Solution does not converge

    def plot_sn_mag(self, res_mode, airmass, pwv, exp_t, exp_n, min_mag, max_mag, sky):
        self.tau_func.set_data(res_mode)

        mag_grid = np.arange(min_mag, max_mag+0.1, 0.1)
        nlen = len(mag_grid)

        signal_blue = np.zeros(nlen)
        noise_blue = np.zeros(nlen)
        result_blue = np.zeros(nlen)

        signal_blue_grating = np.zeros(nlen)
        noise_blue_grating = np.zeros(nlen)
        result_blue_grating = np.zeros(nlen)

        signal_green = np.zeros(nlen)
        noise_green = np.zeros(nlen)
        result_green = np.zeros(nlen)

        signal_green_grating = np.zeros(nlen)
        noise_green_grating = np.zeros(nlen)
        result_green_grating = np.zeros(nlen)

        signal_red = np.zeros(nlen)
        noise_red = np.zeros(nlen)
        result_red = np.zeros(nlen)

        signal_red_grating = np.zeros(nlen)
        noise_red_grating = np.zeros(nlen)
        result_red_grating = np.zeros(nlen)

        signal_nir = np.zeros(nlen)
        noise_nir = np.zeros(nlen)
        result_nir = np.zeros(nlen)

        index = 4
        self.num = 0

        self.res = np.zeros(index)
        self.wave = np.zeros(index)
        self.n_read = np.zeros(index)

        self.sky_bg = np.zeros(index)
        self.sky_bg_grating = np.zeros(index)
        self.sky_bg_te = np.zeros(index)
        self.signal = np.zeros(index)
        self.noise = np.zeros(index)
        self.snr = np.zeros(index)

        self.tel_data = np.zeros(index)
        self.tau_atmo = np.zeros(index)
        self.tau_opt = np.zeros(index)
        self.tau_opt_grating = np.zeros(index)
        self.tau_ie = np.zeros(index)
        self.tau = np.zeros(index)
        self.tau_grating = np.zeros(index)

        if res_mode == "LR":
            self.num = len(CTR_LR)

            for i in range(self.num):

                band = "0"
                if i == 0:
                    band = "Blue"
                elif i == 1:
                    band = "Green"
                elif i == 2:
                    band = "Red"
                elif i == 3:
                    band = "NIR"
                else:
                    pass

                self.res[i] = RES_LR[i]
                self.wave[i] = CTR_LR[i]
                self.n_read[i] = N_READ_LR[i]
                self.tau_atmo[i] = self.tau_func.get_tau_atmo_LR(band, airmass, pwv, self.wave[i])
                self.tel_data[i] = self.tau_func.telluric_emission(self.wave[i])

        elif res_mode == "MR":
            self.num = len(CTR_MR)

            for i in range(self.num):
                self.res[i] = RES_MR[i]
                self.wave[i] = CTR_MR[i]
                self.n_read[i] = N_READ_MR[i]

                band = "0"
                if i == 0:
                    band = "Blue"
                elif i == 1:
                    band = "Green"
                elif i == 2:
                    band = "Red"
                else:
                    pass

                self.tau_atmo[i] = self.tau_func.get_tau_atmo_MR(band, airmass, pwv, self.wave[i])

        elif res_mode == "HR":
            self.num = len(CTR_HR)

            for i in range(self.num):
                self.res[i] = RES_HR[i]
                self.wave[i] = CTR_HR[i]
                self.n_read[i] = N_READ_HR[i]

                band = "0"
                if i == 0:
                    band = "Blue"
                elif i == 1:
                    band = "Green"
                elif i == 2:
                    band = "Red"
                else:
                    pass

                self.tau_atmo[i] = self.tau_func.get_tau_atmo_HR(band, airmass, pwv, self.wave[i])

        for i in range(self.num):
            self.tau_opt[i] = self.tau_func.tau_opt_res(self.wave[i], False)
            self.tau_ie[i] = self.tau_func.tau_ie_res(self.wave[i])
            self.tau[i] = self.tau_atmo[i] * self.tau_opt[i] * self.tau_ie[i]

            if res_mode == "MR" or res_mode == "HR":
                self.tau_opt_grating[i] = self.tau_func.tau_opt_res(self.wave[i], True)
                self.tau_grating[i] = self.tau_atmo[i] * self.tau_opt_grating[i] * self.tau_ie[i]

        for i in range(self.num):
            self.sky_bg[i] = (exp_t * exp_n) * A_TEL * OMEGA * self.tau_opt[i] * self.tau_atmo[i] \
                             * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * self.res[i])
            if res_mode == "MR" or res_mode == "HR":
                self.sky_bg_grating[i] = (exp_t * exp_n) * A_TEL * OMEGA * self.tau_opt_grating[i] * self.tau_atmo[i] \
                                         * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * self.res[i])
            if res_mode == "LR":
                self.sky_bg_te[i] = (exp_t * exp_n) * A_TEL * self.tau_opt[i] * self.tau_atmo[i] * OMEGA * self.tel_data[i]

        for i in range(nlen):
            signal_blue[i] = (exp_t * exp_n) * A_TEL * self.tau[0] * S_ZM \
                             * 10.0 ** (-0.4 * mag_grid[i]) / (h * self.res[0])
            signal_green[i] = (exp_t * exp_n) * A_TEL * self.tau[1] * S_ZM \
                              * 10.0 ** (-0.4 * mag_grid[i]) / (h * self.res[1])
            signal_red[i] = (exp_t * exp_n) * A_TEL * self.tau[2] * S_ZM \
                            * 10.0 ** (-0.4 * mag_grid[i]) / (h * self.res[2])

            if res_mode == "MR" or res_mode == "HR":
                signal_blue_grating[i] = (exp_t * exp_n) * A_TEL * self.tau_grating[0] * S_ZM \
                                         * 10.0 ** (-0.4 * mag_grid[i]) / (h * self.res[0])
                signal_green_grating[i] = (exp_t * exp_n) * A_TEL * self.tau_grating[1] * S_ZM \
                                          * 10.0 ** (-0.4 * mag_grid[i]) / (h * self.res[1])
                signal_red_grating[i] = (exp_t * exp_n) * A_TEL * self.tau_grating[2] * S_ZM \
                                        * 10.0 ** (-0.4 * mag_grid[i]) / (h * self.res[2])

            if res_mode == "LR":
                signal_nir[i] = (exp_t * exp_n) * A_TEL * self.tau[3] * S_ZM \
                                * 10.0 ** (-0.4 * mag_grid[i]) / (h * self.res[3])

            noise_blue[i] = sqrt(signal_blue[i] + self.sky_bg[0] + N_RES * exp_n * (exp_t * N_DARK + self.n_read[0]**2))
            noise_green[i] = sqrt(signal_green[i] + self.sky_bg[1] + N_RES * exp_n * (exp_t * N_DARK + self.n_read[1]**2))
            noise_red[i] = sqrt(signal_red[i] + self.sky_bg[2] + N_RES * exp_n * (exp_t * N_DARK + self.n_read[2]**2))

            if res_mode == "MR" or res_mode == "HR":
                noise_blue_grating[i] = sqrt(signal_blue_grating[i] + self.sky_bg_grating[0]
                                             + N_RES * exp_n * (exp_t * N_DARK + self.n_read[0] ** 2))
                noise_green_grating[i] = sqrt(signal_green_grating[i] + self.sky_bg_grating[1]
                                              + N_RES * exp_n * (exp_t * N_DARK + self.n_read[1] ** 2))
                noise_red_grating[i] = sqrt(signal_red_grating[i] + self.sky_bg_grating[2]
                                            + N_RES * exp_n * (exp_t * N_DARK + self.n_read[2] ** 2))

            if res_mode == "LR":
                noise_nir[i] = sqrt(signal_nir[i] + self.sky_bg[3] + self.sky_bg_te[3] + N_RES * exp_n * (exp_t * N_DARK + self.n_read[3]**2))

            result_blue[i] = signal_blue[i] / noise_blue[i]
            result_green[i] = signal_green[i] / noise_green[i]
            result_red[i] = signal_red[i] / noise_red[i]

            if res_mode == "MR" or res_mode == "HR":
                result_blue_grating[i] = signal_blue_grating[i] / noise_blue_grating[i]
                result_green_grating[i] = signal_green_grating[i] / noise_green_grating[i]
                result_red_grating[i] = signal_red_grating[i] / noise_red_grating[i]

            if res_mode == "LR":
                result_nir[i] = signal_nir[i] / noise_nir[i]

        if res_mode == "LR":
            arr_result = [result_blue, result_green, result_red, result_nir]
        else:
            arr_result = [result_blue, result_green, result_red,
                          result_blue_grating, result_green_grating, result_red_grating]

        output.display_sn_mag(res_mode, airmass, pwv, exp_t, exp_n, min_mag, max_mag, mag_grid, sky, arr_result)

    def plot_sn_wave(self, res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave):
        self.tau_func.set_data(res_mode)

        self.wave_grid = np.arange(min_wave, max_wave + 0.1, 0.1)
        num = len(self.wave_grid)

        self.sky_bg = np.zeros(num)
        self.signal = np.zeros(num)
        self.noise = np.zeros(num)
        self.snr = np.zeros(shape=(2, num))
        self.tau_atmo = np.zeros(num)
        self.tau_opt = np.zeros(num)
        self.tau_ie = np.zeros(num)
        self.tau = np.zeros(num)
        
        #added by CK 20210903
        self.sky_bg_te = np.zeros(num)
        
        k = 0  # band index

        if res_mode == "LR":
            start = time.time()
            if wave_mode != "Input Wave":
                for i in range(num):
                    self.tau_atmo[i] = self.tau_func.get_tau_atmo_LR(wave_mode, airmass, pwv, self.wave_grid[i])
                    self.tau_opt[i] = self.tau_func.tau_opt_res(self.wave_grid[i], False)
                    self.tau_ie[i] = self.tau_func.tau_ie_res(self.wave_grid[i])
                    self.tau[i] = self.tau_atmo[i] * self.tau_opt[i] * self.tau_ie[i]

                #added by CK 20210903
                for i in range(num):
                    tel_data = self.tau_func.telluric_emission(self.wave_grid[i])
                    self.sky_bg_te[i] = (exp_t * exp_n) * A_TEL * self.tau_opt[i] * self.tau_atmo[i] * OMEGA * tel_data
                
                for i in range(num):
                    self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM * 10.0 ** (-0.4 * mag) \
                                     / (h * RES_LR[k])
                    # remove tau ie for the background -> 
                    self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau_opt[i] * self.tau_atmo[i] * OMEGA \
                                     * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[k])

                    self.noise[i] = sqrt(self.signal[i] + self.sky_bg[i] + self.sky_bg_te[i] + N_RES * exp_n * (exp_t * N_DARK + N_READ_LR[k] ** 2))
                    self.snr[0][i] = self.signal[i] / self.noise[i]

                end = time.time()
                print(f"Processing time = {end - start:.2f} sec.")

                output.display_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky,
                                       min_wave, max_wave, self.snr, self.wave_grid)

            else:
                index = [0, 0, 0, 0]

                for k in range(4):
                    count = 0
                    for i in range(num):
                        if WAVE_BAND_LR[k][0] <= self.wave_grid[i] <= WAVE_BAND_LR[k][1]:
                            count += 1
                        else:
                            continue

                    index[k] = count

                self.snr_blue = np.zeros(index[0])
                self.snr_green = np.zeros(index[1])
                self.snr_red = np.zeros(index[2])
                self.snr_nir = np.zeros(index[3])

                self.wave_blue = np.zeros(index[0])
                self.wave_green = np.zeros(index[1])
                self.wave_red = np.zeros(index[2])
                self.wave_nir = np.zeros(index[3])

                for k in range(4):
                    count = 0
                    for i in range(num):
                        if WAVE_BAND_LR[k][0] <= self.wave_grid[i] <= WAVE_BAND_LR[k][1]:

                            band = "0"
                            if k == 0:
                                band = "Blue"
                            elif k == 1:
                                band = "Green"
                            elif k == 2:
                                band = "Red"
                            elif k == 3:
                                band = "NIR"
                            else:
                                pass

                            self.tau_atmo[i] = self.tau_func.get_tau_atmo_LR(band, airmass, pwv, self.wave_grid[i])

                            self.tau_opt[i] = self.tau_func.tau_opt_res(self.wave_grid[i], False)
                            self.tau_ie[i] = self.tau_func.tau_ie_res(self.wave_grid[i])
                            self.tau[i] = self.tau_atmo[i] * self.tau_opt[i] * self.tau_ie[i]

                            tel_data = self.tau_func.telluric_emission(self.wave_grid[i])
                            self.sky_bg_te[i] = exp_t * exp_n * A_TEL * self.tau_atmo[i] * self.tau_opt[i] * OMEGA * tel_data

                            self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau_atmo[i] * self.tau_opt[i] * OMEGA * S_ZM \
                                             * 10.0 ** (-0.4 * sky) / (h * RES_LR[k])
                            self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                             * 10.0 ** (-0.4 * mag) / (h * RES_LR[k])
                            self.noise[i] = sqrt(self.signal[i] + self.sky_bg[i] + self.sky_bg_te[i] + N_RES * exp_n
                                                 * (exp_t * N_DARK + N_READ_LR[k] ** 2))

                            if k == 0:
                                self.snr_blue[count] = self.signal[i] / self.noise[i]
                                self.wave_blue[count] = self.wave_grid[i]
                            elif k == 1:
                                self.snr_green[count] = self.signal[i] / self.noise[i]
                                self.wave_green[count] = self.wave_grid[i]
                            elif k == 2:
                                self.snr_red[count] = self.signal[i] / self.noise[i]
                                self.wave_red[count] = self.wave_grid[i]
                            else:
                                self.snr_nir[count] = self.signal[i] / self.noise[i]
                                self.wave_nir[count] = self.wave_grid[i]

                            count += 1
                
                wave_arr = [self.wave_blue, self.wave_green, self.wave_red, self.wave_nir]
                snr_arr = [self.snr_blue, self.snr_green, self.snr_red, self.snr_nir]

                end = time.time()
                print(f"Processing time = {end - start:.2f} sec.")

                output.display_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky,
                                       min_wave, max_wave, snr_arr, wave_arr)

        elif res_mode == "MR":
            if wave_mode != "Input Wave":
                with_grating = 0
                while with_grating <= 1:
                    for i in range(num):
                        self.tau_atmo[i] = self.tau_func.get_tau_atmo_MR(wave_mode, airmass, pwv, self.wave_grid[i])
                        self.tau_opt[i] = self.tau_func.tau_opt_res(self.wave_grid[i], with_grating)
                        self.tau_ie[i] = self.tau_func.tau_ie_res(self.wave_grid[i])
                        self.tau[i] = self.tau_atmo[i] * self.tau_opt[i] * self.tau_ie[i]

                    for i in range(num):
                        self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                         * 10.0 ** (-0.4 * sky) / (h * RES_MR[k])
                        self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                         * 10.0 ** (-0.4 * mag) / (h * RES_MR[k])
                        self.noise[i] = sqrt(
                            self.signal[i] + self.sky_bg[i] + N_RES * exp_n * (exp_t * N_DARK + N_READ_MR[k] ** 2))
                        self.snr[with_grating][i] = self.signal[i] / self.noise[i]

                    with_grating += 1

                output.display_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky,
                                       min_wave, max_wave, self.snr, self.wave_grid)

            else:
                index = [0, 0, 0]

                for k in range(3):
                    count = 0
                    for i in range(num):
                        if WAVE_BAND_MR[k][0] <= self.wave_grid[i] <= WAVE_BAND_MR[k][1]:
                            count += 1
                        else:
                            continue

                    index[k] = count


                self.snr_blue = np.zeros(index[0])
                self.snr_green = np.zeros(index[1])
                self.snr_red = np.zeros(index[2])
                #self.snr_nir = np.zeros(index[3])

                self.wave_blue = np.zeros(index[0])
                self.wave_green = np.zeros(index[1])
                self.wave_red = np.zeros(index[2])
                #self.wave_nir = np.zeros(index[3])

                with_grating = 0
                while with_grating <= 1:
                    for k in range(3):
                        count = 0
                        for i in range(num):
                            if WAVE_BAND_MR[k][0] <= self.wave_grid[i] <= WAVE_BAND_MR[k][1]:

                                band = "0"
                                if k == 0:
                                    band = "Blue"
                                elif k == 1:
                                    band = "Green"
                                elif k == 2:
                                    band = "Red"
                                elif k == 3:
                                    band = "NIR"
                                else:
                                    pass

                                self.tau_atmo[i] = self.tau_func.get_tau_atmo_MR(band, airmass, pwv, self.wave_grid[i])
                                self.tau_opt[i] = self.tau_func.tau_opt_res(self.wave_grid[i], with_grating)
                                self.tau_ie[i] = self.tau_func.tau_ie_res(self.wave_grid[i])
                                self.tau[i] = self.tau_atmo[i] * self.tau_opt[i] * self.tau_ie[i]

                                self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                                 * 10.0 ** (-0.4 * sky) / (h * RES_MR[k])
                                self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                                 * 10.0 ** (-0.4 * mag) / (h * RES_MR[k])
                                self.noise[i] = sqrt(self.signal[i] + self.sky_bg[i] + N_RES * exp_n
                                                     * (exp_t * N_DARK + N_READ_MR[k] ** 2))

                                if k == 0:
                                    self.snr_blue[count] = self.signal[i] / self.noise[i]
                                    self.wave_blue[count] = self.wave_grid[i]
                                elif k == 1:
                                    self.snr_green[count] = self.signal[i] / self.noise[i]
                                    self.wave_green[count] = self.wave_grid[i]
                                elif k == 2:
                                    self.snr_red[count] = self.signal[i] / self.noise[i]
                                    self.wave_red[count] = self.wave_grid[i]
                                else:
                                    self.snr_nir[count] = self.signal[i] / self.noise[i]
                                    self.wave_nir[count] = self.wave_grid[i]

                                count += 1

                    wave_arr = [self.wave_blue, self.wave_green, self.wave_red]
                    snr_arr = [self.snr_blue, self.snr_green, self.snr_red]
                    self.snr_arr[with_grating] = deepcopy(snr_arr)
                    with_grating += 1

                output.display_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky,
                                       min_wave, max_wave, self.snr_arr, wave_arr)

        elif res_mode == "HR":
            if wave_mode == "Blue":
                k = 0
            elif wave_mode == "Green":
                k = 1
            elif wave_mode == "Red":
                k = 2
            else:
                pass

            if wave_mode != "Input Wave":
                pass
            else:
                index = [0, 0, 0]

                for k in range(3):
                    count = 0
                    for i in range(num):
                        if WAVE_BAND_HR[k][0] <= self.wave_grid[i] <= WAVE_BAND_HR[k][1]:
                            count += 1
                        else:
                            continue

                    index[k] = count

                self.snr_blue = np.zeros(index[0])
                self.snr_green = np.zeros(index[1])
                self.snr_red = np.zeros(index[2])

                self.wave_blue = np.zeros(index[0])
                self.wave_green = np.zeros(index[1])
                self.wave_red = np.zeros(index[2])

                with_grating = 0
                while with_grating <= 1:
                    for k in range(3):
                        if (with_grating == 1) and (k == 0 or k == 2):
                            continue
                        count = 0
                        for i in range(num):
                            if WAVE_BAND_HR[k][0] <= self.wave_grid[i] <= WAVE_BAND_HR[k][1]:

                                band = "0"
                                if k == 0:
                                    band = "Blue"
                                elif k == 1:
                                    band = "Green"
                                elif k == 2:
                                    band = "Red"
                                elif k == 3:
                                    band = "NIR"
                                else:
                                    pass

                                self.tau_atmo[i] = self.tau_func.get_tau_atmo_HR(band, airmass, pwv, self.wave_grid[i])
                                self.tau_opt[i] = self.tau_func.tau_opt_res(self.wave_grid[i], with_grating)
                                self.tau_ie[i] = self.tau_func.tau_ie_res(self.wave_grid[i])
                                self.tau[i] = self.tau_atmo[i] * self.tau_opt[i] * self.tau_ie[i]

                                self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                                 * 10.0 ** (-0.4 * sky) / (h * RES_HR[k])
                                self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                                 * 10.0 ** (-0.4 * mag) / (h * RES_HR[k])
                                self.noise[i] = sqrt(self.signal[i] + self.sky_bg[i] + N_RES * exp_n
                                                     * (exp_t * N_DARK + N_READ_HR[k] ** 2))

                                if k == 0:
                                    self.snr_blue[count] = self.signal[i] / self.noise[i]
                                    self.wave_blue[count] = self.wave_grid[i]
                                elif k == 1:
                                    self.snr_green[count] = self.signal[i] / self.noise[i]
                                    self.wave_green[count] = self.wave_grid[i]
                                else:
                                    self.snr_red[count] = self.signal[i] / self.noise[i]
                                    self.wave_red[count] = self.wave_grid[i]

                                count += 1

                    wave_arr = [self.wave_blue, self.wave_green, self.wave_red]
                    snr_arr = [self.snr_blue, self.snr_green, self.snr_red]
                    self.snr_arr[with_grating] = deepcopy(snr_arr)
                    with_grating += 1

                output.display_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky,
                                       min_wave, max_wave, self.snr_arr, wave_arr)

    def plot_sn_wave_order(self, res_mode, wave_mode, order, airmass, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave):
        self.tau_func.set_data(res_mode)

        self.wave_order1 = np.arange(min_wave[0], max_wave[0] + 0.1, 0.1)
        self.wave_order2 = np.arange(min_wave[1], max_wave[1] + 0.1, 0.1)

        len1 = len(self.wave_order1)
        len2 = len(self.wave_order2)

        k = 0  # band index

        if res_mode == "HR":

            if wave_mode.startswith('B'):
                k = 0
            elif wave_mode.startswith('G'):
                k = 1
            elif wave_mode.startswith('R'):
                k = 2
            else:
                return None

            # Calculate first order
            self.tau_func.set_data_order(res_mode, order)
            self.sky_bg = np.zeros(len1)
            self.signal = np.zeros(len1)
            self.noise = np.zeros(len1)
            self.snr_order1 = np.zeros(len1)

            self.tau_atmo = np.zeros(len1)
            self.tau_opt = np.zeros(len1)
            self.tau_ie = np.zeros(len1)
            self.tau = np.zeros(len1)

            for i in range(len1):
                self.tau_atmo[i] = self.tau_func.get_tau_atmo_HR(k, airmass, pwv, self.wave_order1[i])
                self.tau[i] = self.tau_atmo[i] * self.tau_func.get_tau_order(self.wave_order1[i])

                self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                 * 10.0 ** (-0.4 * sky) / (h * RES_HR[k])
                self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                 * 10.0 ** (-0.4 * mag) / (h * RES_HR[k])
                self.noise[i] = sqrt(self.signal[i] + self.sky_bg[i] + N_RES * exp_n
                                     * (exp_t * N_DARK + N_READ_HR[k] ** 2))

                self.snr_order1[i] = self.signal[i] / self.noise[i]

            # Calculate second order
            order = order - 1
            self.tau_func.set_data_order(res_mode, order)

            self.sky_bg = np.zeros(len2)
            self.signal = np.zeros(len2)
            self.noise = np.zeros(len2)
            self.snr_order2 = np.zeros(len2)

            self.tau_atmo = np.zeros(len2)
            self.tau_opt = np.zeros(len2)
            self.tau_ie = np.zeros(len2)
            self.tau = np.zeros(len2)

            for i in range(len2):
                self.tau_atmo[i] = self.tau_func.get_tau_atmo_HR(k, airmass, pwv, self.wave_order2[i])
                self.tau[i] = self.tau_atmo[i] * self.tau_func.get_tau_order(self.wave_order2[i])

                self.sky_bg[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                 * 10.0 ** (-0.4 * sky) / (h * RES_HR[k])
                self.signal[i] = (exp_t * exp_n) * A_TEL * self.tau[i] * S_ZM \
                                 * 10.0 ** (-0.4 * mag) / (h * RES_HR[k])
                self.noise[i] = sqrt(self.signal[i] + self.sky_bg[i] + N_RES * exp_n
                                     * (exp_t * N_DARK + N_READ_HR[k] ** 2))

                self.snr_order2[i] = self.signal[i] / self.noise[i]

            wave_arr = [self.wave_order1, self.wave_order2]
            snr_arr = [self.snr_order1, self.snr_order2]

            output.display_sn_wave_order(res_mode, wave_mode, order, airmass, pwv, exp_t, exp_n, mag, sky,
                                         min_wave, max_wave, snr_arr, wave_arr)
