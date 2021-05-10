"""Function module of MSE ETC.

Modification Log:
    * 2021.01.19 - The first MSE-ETC version was created by Tae-Geun Ji & Soojong Pak
    * 2021.03.24 - Updated by Tae-Geun Ji
    * 2021.03.29 - Updated by Tae-Geun Ji
    * 2021.04.09 - Updated by Hojae Ahn
    * 2021.04.21 - Updated by Mingyoeng Yang
    * 2021.04.26 - Updated by Mingyeong Yang
"""

from parameters import *
import interpolate
import output
import numpy as np
import math
import time

# change 20210422 by MY
class Functions:

    def __init__(self):
        self.a_tel = PI*(D_TEL/2)**2
        self.band_n = 6

        self.wave_arr = []
        self.sky_bg_arr = []
        self.signal_arr = []
        self.noise_arr = []
        self.signal_to_noise_arr = []

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

        self.tau_atmo_arr = []
        self.tau_opt_arr = []
        self.tau_ie_arr = []
        self.find = False

        self.tau_func = interpolate.Throughput()

    def signal_to_noise_low(self, res_mode, pwv, exp_t, exp_n, mag, sky, wave, print_text):
        self.tau_func.set_data(res_mode)

        self.sky_bg_arr = np.zeros(self.band_n)
        self.signal_arr = np.zeros(self.band_n)
        self.noise_arr = np.zeros(self.band_n)
        self.signal_to_noise_arr = np.zeros(self.band_n)
        self.tau_atmo_arr = np.zeros(self.band_n)
        self.tau_opt_arr = np.zeros(self.band_n)
        self.tau_ie_arr = np.zeros(self.band_n)

        if res_mode == "LR":

            WAVE_LR[4] = wave
            WAVE_LR[5] = wave

            self.tau_atmo_arr[0] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[0])
            self.tau_atmo_arr[1] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[1])
            self.tau_atmo_arr[2] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[2])
            self.tau_atmo_arr[3] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[3])

            if 360 <= wave < 540:
                RES_LR[4] = RES_LR[0]
                BAND_LR[4] = BAND_LR[0]
                N_READ_LR[4] = N_READ_LR[0]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[4])
            elif 560 < wave < 715:
                RES_LR[4] = RES_LR[1]
                BAND_LR[4] = BAND_LR[1]
                N_READ_LR[4] = N_READ_LR[1]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[4])
            elif 740 < wave < 960:
                RES_LR[4] = RES_LR[2]
                BAND_LR[4] = BAND_LR[1]
                N_READ_LR[4] = N_READ_LR[2]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[4])
            elif 985 < wave < 1320:
                RES_LR[4] = RES_LR[3]
                BAND_LR[4] = BAND_LR[3]
                N_READ_LR[4] = N_READ_LR[3]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[4])

            if 540 <= wave <= 560:
                RES_LR[4] = RES_LR[0]
                RES_LR[5] = RES_LR[1]
                BAND_LR[4] = BAND_LR[0]
                BAND_LR[5] = BAND_LR[1]
                N_READ_LR[4] = N_READ_LR[0]
                N_READ_LR[5] = N_READ_LR[1]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[5])
            elif 715 <= wave <= 740:
                RES_LR[4] = RES_LR[1]
                RES_LR[5] = RES_LR[2]
                BAND_LR[4] = BAND_LR[1]
                BAND_LR[5] = BAND_LR[2]
                N_READ_LR[4] = N_READ_LR[1]
                N_READ_LR[5] = N_READ_LR[2]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[5])
            elif 960 <= wave <= 985:
                RES_LR[4] = RES_LR[2]
                RES_LR[5] = RES_LR[3]
                BAND_LR[4] = BAND_LR[2]
                BAND_LR[5] = BAND_LR[3]
                N_READ_LR[4] = N_READ_LR[2]
                N_READ_LR[5] = N_READ_LR[3]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[5])

            for i in range(0, self.band_n):
                self.tau_opt_arr[i] = self.tau_func.tau_opt_res(WAVE_LR[i])
                self.tau_ie_arr[i] = self.tau_func.tau_ie_res(WAVE_LR[i])

            for i in range(0, self.band_n):
                self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                     * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * RES_LR[i])

                self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                     * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag[i]) / (h * RES_LR[i])

                self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                              * (exp_t * N_DARK + N_READ_LR[i] ** 2))

                self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

        elif res_mode == "MR":

            WAVE_MR[4] = wave
            WAVE_MR[5] = wave

            self.tau_atmo_arr[0] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[0])
            self.tau_atmo_arr[1] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[1])
            self.tau_atmo_arr[2] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[2])
            self.tau_atmo_arr[3] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[3])

            if 391 <= wave < 510:
                RES_MR[4] = RES_MR[0]
                BAND_MR[4] = BAND_MR[0]
                N_READ_MR[4] = N_READ_MR[0]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[4])
            elif 576 < wave < 700:
                RES_MR[4] = RES_MR[1]
                BAND_MR[4] = BAND_MR[1]
                N_READ_MR[4] = N_READ_MR[1]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[4])
            elif 737 < wave < 900:
                RES_MR[4] = RES_MR[2]
                BAND_MR[4] = BAND_MR[2]
                N_READ_MR[4] = N_READ_MR[2]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[4])
            elif 1457 < wave < 1780:
                RES_MR[4] = RES_MR[3]
                BAND_MR[4] = BAND_MR[3]
                N_READ_MR[4] = N_READ_MR[3]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[4])

            if 510 <= wave <= 576:
                RES_MR[4] = RES_MR[0]
                RES_MR[5] = RES_MR[1]
                BAND_MR[4] = BAND_MR[0]
                BAND_MR[5] = BAND_MR[1]
                N_READ_MR[4] = N_READ_MR[0]
                N_READ_MR[5] = N_READ_MR[1]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[5])
            elif 700 <= wave <= 737:
                RES_MR[4] = RES_MR[1]
                RES_MR[5] = RES_MR[2]
                BAND_MR[4] = BAND_MR[1]
                BAND_MR[5] = BAND_MR[2]
                N_READ_MR[4] = N_READ_MR[1]
                N_READ_MR[5] = N_READ_MR[2]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[5])
            elif 900 <= wave <= 1457:
                RES_MR[4] = RES_MR[2]
                RES_MR[5] = RES_MR[3]
                BAND_MR[4] = BAND_MR[2]
                BAND_MR[5] = BAND_MR[3]
                N_READ_MR[4] = N_READ_MR[2]
                N_READ_MR[5] = N_READ_MR[3]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[5])

            for i in range(0, self.band_n):
                self.tau_opt_arr[i] = self.tau_func.tau_opt_res(WAVE_MR[i])
                self.tau_ie_arr[i] = self.tau_func.tau_ie_res(WAVE_MR[i])

            for i in range(0, self.band_n):
                self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                     * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * RES_MR[i])

                self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                     * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag[i]) / (h * RES_MR[i])

                self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                              * (exp_t * N_DARK + N_READ_MR[i] ** 2))

                self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

        elif res_mode == "HR":

            WAVE_HR[3] = wave
            WAVE_HR[4] = wave
            WAVE_HR[5] = wave

            self.tau_atmo_arr[0] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[0])
            self.tau_atmo_arr[1] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[1])
            self.tau_atmo_arr[2] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[2])
            #self.tau_atmo_arr[3] = self.tau_func.Get_tau_atmo(pwv, WAVE_MR[3])

            if 360 <= wave < 440:
                RES_HR[4] = RES_HR[0]
                BAND_HR[4] = BAND_HR[0]
                N_READ_HR[4] = N_READ_HR[0]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[4])
            elif 460 < wave < 600:
                RES_HR[4] = RES_HR[1]
                BAND_HR[4] = BAND_HR[1]
                N_READ_HR[4] = N_READ_HR[1]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[4])
            elif 620 < wave < 900:
                RES_HR[4] = RES_HR[2]
                BAND_HR[4] = BAND_HR[2]
                N_READ_HR[4] = N_READ_HR[2]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[4])

            if 440 <= wave <= 460:
                RES_HR[4] = RES_HR[0]
                RES_HR[5] = RES_HR[1]
                BAND_HR[4] = BAND_HR[0]
                BAND_HR[5] = BAND_HR[1]
                N_READ_HR[4] = N_READ_HR[0]
                N_READ_HR[5] = N_READ_HR[1]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[5])
            elif 600 <= wave <= 620:
                RES_HR[4] = RES_HR[1]
                RES_HR[5] = RES_HR[2]
                BAND_HR[4] = BAND_HR[1]
                BAND_HR[5] = BAND_HR[2]
                N_READ_HR[4] = N_READ_HR[1]
                N_READ_HR[5] = N_READ_HR[2]
                self.tau_atmo_arr[4] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[4])
                self.tau_atmo_arr[5] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[5])

            for i in range(0, self.band_n):
                self.tau_opt_arr[i] = self.tau_func.tau_opt_res(WAVE_HR[i])
                self.tau_ie_arr[i] = self.tau_func.tau_ie_res(WAVE_HR[i])

            for i in range(0, self.band_n):
                self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                     * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * RES_HR[i])

                self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                     * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag[i]) / (h * RES_HR[i])

                self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                              * (exp_t * N_DARK + N_READ_HR[i] ** 2))

                self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]


        if print_text is True:
            output.display_single(res_mode, pwv, exp_t, exp_n, mag, sky, self.signal_to_noise_arr, wave)

        return self.signal_to_noise_arr  # add 210408 hojae

    def exp_time_cal(self, res_mode, pwv, target_sn, mag, sky, wave):  # add 210408 hojae
        self.exp_table = np.zeros(len(mag))

        for idx in range(1, 5):  # from 10 to 10,000
            self.sn_table.append(self.signal_to_noise_low(res_mode, pwv, 10**idx, 1, mag, sky, wave, False))
        sn_table = np.array(self.sn_table)

        # for B
        for band in range(len(mag)-1):
            if sn_table[0, band] > target_sn:
                output.display_simple_text("Required exposure time of band %d single frame is shorter than 10 seconds." % band)
                return None
            elif (sn_table[0, band] <= target_sn) & (target_sn <= sn_table[1, band]):
                self.exp_table[band] = self.solve_bisection(band, target_sn, 10, 100, res_mode, pwv, mag, sky, wave, False)
            elif (sn_table[1, band] <= target_sn) & (target_sn <= sn_table[2, band]):
                self.exp_table[band] = self.solve_bisection(band, target_sn, 100, 1000, res_mode, pwv, mag, sky, wave, False)
            elif (sn_table[2, band] <= target_sn) & (target_sn <= sn_table[3, band]):
                self.exp_table[band] = self.solve_bisection(band, target_sn, 1000, 10000, res_mode, pwv, mag, sky, wave, False)
            else:
                output.display_simple_text("Required exposure time of band %d single frame is longer than 10,000 seconds(~3 hours)." % band)
                return None
        output.display_exp_time(res_mode, pwv, target_sn, mag, sky, self.exp_table, wave)
        return self.exp_table

    def solve_bisection(self, band, target_sn, x_min, x_max, res_mode, pwv, mag, sky, wave, print_text):  # add 210408 hojae bisection equation solver
        func_min = self.signal_to_noise_low(res_mode, pwv, x_min, 1, mag, sky, wave, False)[band] - target_sn
        func_max = self.signal_to_noise_low(res_mode, pwv, x_max, 1, mag, sky, wave, False)[band] - target_sn

        if func_min * func_max > 0:
            return -1  # input error

        for idx in range(30):  # maximum iteration=30
            func_min = self.signal_to_noise_low(res_mode, pwv, x_min, 1, mag, sky, wave, False)[band] - target_sn
            func_max = self.signal_to_noise_low(res_mode, pwv, x_max, 1, mag, sky, wave, False)[band] - target_sn

            x_iter = (x_min + x_max) * 0.5
            func_iter = self.signal_to_noise_low(res_mode, pwv, x_iter, 1, mag, sky, wave, False)[band] - target_sn

            if np.abs(func_min - func_max) < 0.005 * target_sn:  # convergence tolerance = 0.5% of SN
                return x_iter

            if func_min * func_iter < 0:
                x_max = x_iter

            elif func_iter * func_max < 0:
                x_min = x_iter

            else:
                return x_iter
        return -11  # Solution does not converge

    def plot_sn_mag(self, res_mode, pwv, exp_t, exp_n, min_mag, max_mag, sky):
        self.tau_func.set_data(res_mode)

        mag_arr = np.arange(min_mag, max_mag+0.1, 0.1)
        nlen = len(mag_arr)

        signal_blue = np.zeros(nlen)
        noise_blue = np.zeros(nlen)
        result_blue = np.zeros(nlen)

        signal_green = np.zeros(nlen)
        noise_green = np.zeros(nlen)
        result_green = np.zeros(nlen)

        signal_red = np.zeros(nlen)
        noise_red = np.zeros(nlen)
        result_red = np.zeros(nlen)

        signal_nir = np.zeros(nlen)
        noise_nir = np.zeros(nlen)
        result_nir = np.zeros(nlen)

        self.tau_atmo_arr = np.zeros(4)
        self.tau_opt_arr = np.zeros(4)
        self.tau_ie_arr = np.zeros(4)

        if res_mode == "LR":
            sky_bg_arr = np.zeros(4)

            self.tau_atmo_arr[0] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[0])
            self.tau_atmo_arr[1] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[1])
            self.tau_atmo_arr[2] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[2])
            self.tau_atmo_arr[3] = self.tau_func.Get_tau_atmo(pwv, WAVE_LR[3])

            for i in range(0, 4):
                self.tau_opt_arr[i] = self.tau_func.tau_opt_res(WAVE_LR[i])
                self.tau_ie_arr[i] = self.tau_func.tau_ie_res(WAVE_LR[i])

            for i in range(0, 4):
                sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h*WAVE_LR[i])

            for i in range(0, nlen):
                signal_blue[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[0] * self.tau_opt_arr[0] \
                                 * self.tau_ie_arr[0] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_LR[0])
                signal_green[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[1] * self.tau_opt_arr[1] \
                                 * self.tau_ie_arr[1] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_LR[1])
                signal_red[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[2] * self.tau_opt_arr[2] \
                                 * self.tau_ie_arr[2] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_LR[2])
                signal_nir[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[3] * self.tau_opt_arr[3] \
                                 * self.tau_ie_arr[3] * S_ZM * 10.0 **(-0.4 * mag_arr[i]) / (h * WAVE_LR[3])

                noise_blue[i] = math.sqrt(signal_blue[i]+sky_bg_arr[0]+N_RES*(exp_t*N_DARK+N_READ_LR[0]**2))
                noise_green[i] = math.sqrt(signal_green[i]+sky_bg_arr[1]+N_RES*(exp_t*N_DARK+N_READ_LR[1]**2))
                noise_red[i] = math.sqrt(signal_red[i]+sky_bg_arr[2]+N_RES*(exp_t*N_DARK+N_READ_LR[2]**2))
                noise_nir[i] = math.sqrt(signal_nir[i]+sky_bg_arr[3]+N_RES*(exp_t*N_DARK+N_READ_LR[3]**2))

                result_blue[i] = signal_blue[i] / noise_blue[i]
                result_green[i] = signal_green[i] / noise_green[i]
                result_red[i] = signal_red[i] / noise_red[i]
                result_nir[i] = signal_nir[i] / noise_nir[i]

            arr_result = [result_blue, result_green, result_red, result_nir]
            output.display_sn_mag(res_mode, pwv, exp_t, exp_n, min_mag, max_mag, mag_arr, sky, arr_result)

        elif res_mode == "MR":
            sky_bg_arr = np.zeros(4)

            self.tau_atmo_arr[0] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[0])
            self.tau_atmo_arr[1] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[1])
            self.tau_atmo_arr[2] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[2])
            self.tau_atmo_arr[3] = self.tau_func.Get_tau_atmo_MR(pwv, WAVE_MR[3])

            for i in range(0, 4):
                self.tau_opt_arr[i] = self.tau_func.tau_opt_res(WAVE_MR[i])
                self.tau_ie_arr[i] = self.tau_func.tau_ie_res(WAVE_MR[i])

            for i in range(0, 4):
                sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * WAVE_MR[i])

            for i in range(0, nlen):
                signal_blue[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[0] * self.tau_opt_arr[0] \
                                 * self.tau_ie_arr[0] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_MR[0])
                signal_green[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[1] * self.tau_opt_arr[1] \
                                  * self.tau_ie_arr[1] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_MR[1])
                signal_red[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[2] * self.tau_opt_arr[2] \
                                * self.tau_ie_arr[2] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_MR[2])
                signal_nir[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[3] * self.tau_opt_arr[3] \
                                * self.tau_ie_arr[3] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_MR[3])

                noise_blue[i] = math.sqrt(signal_blue[i] + sky_bg_arr[0] + N_RES * (exp_t * N_DARK + N_READ_MR[0] ** 2))
                noise_green[i] = math.sqrt(
                    signal_green[i] + sky_bg_arr[1] + N_RES * (exp_t * N_DARK + N_READ_MR[1] ** 2))
                noise_red[i] = math.sqrt(signal_red[i] + sky_bg_arr[2] + N_RES * (exp_t * N_DARK + N_READ_MR[2] ** 2))
                noise_nir[i] = math.sqrt(signal_nir[i] + sky_bg_arr[3] + N_RES * (exp_t * N_DARK + N_READ_MR[3] ** 2))

                result_blue[i] = signal_blue[i] / noise_blue[i]
                result_green[i] = signal_green[i] / noise_green[i]
                result_red[i] = signal_red[i] / noise_red[i]
                result_nir[i] = signal_nir[i] / noise_nir[i]

            arr_result = [result_blue, result_green, result_red, result_nir]
            output.display_sn_mag(res_mode, pwv, exp_t, exp_n, min_mag, max_mag, mag_arr, sky, arr_result)

        elif res_mode == "HR":

            sky_bg_arr = np.zeros(4)

            self.tau_atmo_arr[0] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[0])
            self.tau_atmo_arr[1] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[1])
            self.tau_atmo_arr[2] = self.tau_func.Get_tau_atmo_HR(pwv, WAVE_HR[2])
            #self.tau_atmo_arr[3] = self.tau_func.Get_tau_atmo(pwv, WAVE_HR[3])

            for i in range(0, 4):
                self.tau_opt_arr[i] = self.tau_func.tau_opt_res(WAVE_HR[i])
                self.tau_ie_arr[i] = self.tau_func.tau_ie_res(WAVE_HR[i])

            for i in range(0, 4):
                sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * WAVE_HR[i])

            for i in range(0, nlen):
                signal_blue[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[0] * self.tau_opt_arr[0] \
                                 * self.tau_ie_arr[0] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_HR[0])
                signal_green[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[1] * self.tau_opt_arr[1] \
                                  * self.tau_ie_arr[1] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_HR[1])
                signal_red[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[2] * self.tau_opt_arr[2] \
                                * self.tau_ie_arr[2] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_HR[2])
                #signal_nir[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[3] * self.tau_opt_arr[3] \
                #                * self.tau_ie_arr[3] * S_ZM * 10.0 ** (-0.4 * mag_arr[i]) / (h * WAVE_HR[3])

                noise_blue[i] = math.sqrt(signal_blue[i] + sky_bg_arr[0] + N_RES * (exp_t * N_DARK + N_READ_HR[0] ** 2))
                noise_green[i] = math.sqrt(
                    signal_green[i] + sky_bg_arr[1] + N_RES * (exp_t * N_DARK + N_READ_HR[1] ** 2))
                noise_red[i] = math.sqrt(signal_red[i] + sky_bg_arr[2] + N_RES * (exp_t * N_DARK + N_READ_HR[2] ** 2))
                #noise_nir[i] = math.sqrt(signal_nir[i] + sky_bg_arr[3] + N_RES * (exp_t * N_DARK + N_READ_HR[3] ** 2))

                result_blue[i] = signal_blue[i] / noise_blue[i]
                result_green[i] = signal_green[i] / noise_green[i]
                result_red[i] = signal_red[i] / noise_red[i]
                #result_nir[i] = signal_nir[i] / noise_nir[i]

            arr_result = [result_blue, result_green, result_red, result_nir]
            output.display_sn_mag(res_mode, pwv, exp_t, exp_n, min_mag, max_mag, mag_arr, sky, arr_result)

    def plot_sn_wave(self, res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave):
        self.tau_func.set_data(res_mode)

        self.wave_arr = np.arange(min_wave, max_wave + 0.1, 0.1)
        nlen = len(self.wave_arr)

        self.sky_bg_arr = np.zeros(nlen)
        self.signal_arr = np.zeros(nlen)
        self.noise_arr = np.zeros(nlen)
        self.signal_to_noise_arr = np.zeros(nlen)
        self.tau_atmo_arr = np.zeros(nlen)
        self.tau_opt_arr = np.zeros(nlen)
        self.tau_ie_arr = np.zeros(nlen)

        if res_mode == "LR":
            if wave_mode == "Blue":
                for i in range(0, nlen):
                    t1 = time.time()
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[0])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[0])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_LR[0] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "Green":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[1])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[1])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_LR[1] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "Red":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[2])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[2])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_LR[2] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "NIR":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[3])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[3])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_LR[3] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            else:
                self.snr_blue = np.zeros(nlen)
                self.snr_green = np.zeros(nlen)
                self.snr_red = np.zeros(nlen)
                self.snr_nir = np.zeros(nlen)

                self.wave_blue = np.zeros(nlen)
                self.wave_green = np.zeros(nlen)
                self.wave_red = np.zeros(nlen)
                self.wave_nir = np.zeros(nlen)

                count = 0
                for i in range(0, nlen):
                    if 360 <= self.wave_arr[i] <= 560:
                        count += 1

                self.snr_blue = np.zeros(count)
                self.wave_blue = np.zeros(count)

                count = 0
                for i in range (0, nlen):

                    if 360 <= self.wave_arr[i] <= 560:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[0])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[0])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_LR[0] ** 2))

                        self.snr_blue[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_blue[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 540 <= self.wave_arr[i] <= 740:
                        count += 1

                self.snr_green = np.zeros(count)
                self.wave_green = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 540 <= self.wave_arr[i] <= 740:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[1])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[1])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_LR[1] ** 2))

                        self.snr_green[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_green[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 715 <= self.wave_arr[i] <= 985:
                        count += 1

                self.snr_red = np.zeros(count)
                self.wave_red = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 715 <= self.wave_arr[i] <= 985:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[2])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[2])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_LR[2] ** 2))

                        self.snr_red[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_red[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 960 <= self.wave_arr[i] <= 1320:
                        count += 1

                self.snr_nir = np.zeros(count)
                self.wave_nir = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 960 <= self.wave_arr[i] <= 1320:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_LR[3])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_LR[3])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_LR[3] ** 2))

                        self.snr_nir[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_nir[count] = self.wave_arr[i]
                        count += 1

                wave_arr = [self.wave_blue, self.wave_green, self.wave_red, self.wave_nir]
                result_arr = [self.snr_blue, self.snr_green, self.snr_red, self.snr_nir]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       result_arr, wave_arr)

        elif res_mode == "MR":

            if wave_mode == "Blue":
                for i in range(0, nlen):
                    t1 = time.time()
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[0])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[0])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_MR[0] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "Green":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[1])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[1])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_MR[1] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "Red":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[2])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[2])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_MR[2] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "NIR":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[3])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[3])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_MR[3] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            else:
                self.snr_blue = np.zeros(nlen)
                self.snr_green = np.zeros(nlen)
                self.snr_red = np.zeros(nlen)
                self.snr_nir = np.zeros(nlen)

                self.wave_blue = np.zeros(nlen)
                self.wave_green = np.zeros(nlen)
                self.wave_red = np.zeros(nlen)
                self.wave_nir = np.zeros(nlen)

                count = 0
                for i in range(0, nlen):
                    if 391 <= self.wave_arr[i] <= 510:
                        count += 1

                self.snr_blue = np.zeros(count)
                self.wave_blue = np.zeros(count)

                count = 0
                for i in range (0, nlen):

                    if 391 <= self.wave_arr[i] <= 510:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[0])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[0])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_MR[0] ** 2))

                        self.snr_blue[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_blue[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 576 <= self.wave_arr[i] <= 700:
                        count += 1

                self.snr_green = np.zeros(count)
                self.wave_green = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 576 <= self.wave_arr[i] <= 700:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[1])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[1])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_MR[1] ** 2))

                        self.snr_green[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_green[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 737 <= self.wave_arr[i] <= 900:
                        count += 1

                self.snr_red = np.zeros(count)
                self.wave_red = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 737 <= self.wave_arr[i] <= 900:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[2])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[2])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_MR[2] ** 2))

                        self.snr_red[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_red[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 1457 <= self.wave_arr[i] <= 1780:
                        count += 1

                self.snr_nir = np.zeros(count)
                self.wave_nir = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 1457 <= self.wave_arr[i] <= 1780:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_MR(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[3])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[3])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_MR[3] ** 2))

                        self.snr_nir[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_nir[count] = self.wave_arr[i]
                        count += 1

                wave_arr = [self.wave_blue, self.wave_green, self.wave_red, self.wave_nir]
                result_arr = [self.snr_blue, self.snr_green, self.snr_red, self.snr_nir]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       result_arr, wave_arr)

        elif res_mode == "HR":

            if wave_mode == "Blue":
                for i in range(0, nlen):
                    t1 = time.time()
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_HR(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_HR[0])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_HR[0])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_HR[0] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "Green":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_HR(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_HR[1])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_HR[1])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_HR[1] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "Red":
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_HR(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_HR[2])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_HR[2])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_HR[2] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)

            elif wave_mode == "NIR":
                """
                for i in range(0, nlen):
                    self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                    self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                    self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                for i in range(0, nlen):
                    self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_MR[3])

                    self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                         * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_MR[3])

                    self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                  * (exp_t * N_DARK + N_READ_MR[3] ** 2))

                    self.signal_to_noise_arr[i] = self.signal_arr[i] / self.noise_arr[i]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       self.signal_to_noise_arr, self.wave_arr)
                """

            else:
                self.snr_blue = np.zeros(nlen)
                self.snr_green = np.zeros(nlen)
                self.snr_red = np.zeros(nlen)
                #self.snr_nir = np.zeros(nlen)

                self.wave_blue = np.zeros(nlen)
                self.wave_green = np.zeros(nlen)
                self.wave_red = np.zeros(nlen)
                #self.wave_nir = np.zeros(nlen)

                count = 0
                for i in range(0, nlen):
                    if 360 <= self.wave_arr[i] <= 460:
                        count += 1

                self.snr_blue = np.zeros(count)
                self.wave_blue = np.zeros(count)

                count = 0
                for i in range(0, nlen):

                    if 360 <= self.wave_arr[i] <= 460:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo_HR(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_HR[0])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_HR[0])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_HR[0] ** 2))

                        self.snr_blue[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_blue[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 440 <= self.wave_arr[i] <= 620:
                        count += 1

                self.snr_green = np.zeros(count)
                self.wave_green = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 440 <= self.wave_arr[i] <= 620:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_HR[1])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_HR[1])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_HR[1] ** 2))

                        self.snr_green[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_green[count] = self.wave_arr[i]
                        count += 1

                count = 0
                for i in range(0, nlen):
                    if 600 <= self.wave_arr[i] <= 900:
                        count += 1

                self.snr_red = np.zeros(count)
                self.wave_red = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 600 <= self.wave_arr[i] <= 900:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_HR[2])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_HR[2])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_HR[2] ** 2))

                        self.snr_red[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_red[count] = self.wave_arr[i]
                        count += 1

                """
                count = 0
                for i in range(0, nlen):
                    if 960 <= self.wave_arr[i] <= 1320:
                        count += 1

                self.snr_nir = np.zeros(count)
                self.wave_nir = np.zeros(count)

                count = 0
                for i in range(0, nlen):
                    if 960 <= self.wave_arr[i] <= 1320:
                        self.tau_atmo_arr[i] = self.tau_func.Get_tau_atmo(pwv, self.wave_arr[i])
                        self.tau_opt_arr[i] = self.tau_func.tau_opt_res(self.wave_arr[i])
                        self.tau_ie_arr[i] = self.tau_func.tau_ie_res(self.wave_arr[i])

                        self.sky_bg_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * sky) / (h * RES_HR[3])

                        self.signal_arr[i] = (exp_t * exp_n) * self.a_tel * self.tau_atmo_arr[i] * self.tau_opt_arr[i] \
                                             * self.tau_ie_arr[i] * S_ZM * 10.0 ** (-0.4 * mag) / (h * RES_HR[3])

                        self.noise_arr[i] = math.sqrt(self.signal_arr[i] + self.sky_bg_arr[i] + N_RES
                                                      * (exp_t * N_DARK + N_READ_HR[3] ** 2))

                        self.snr_nir[count] = self.signal_arr[i] / self.noise_arr[i]
                        self.wave_nir[count] = self.wave_arr[i]
                        count += 1
                        
                """

                wave_arr = [self.wave_blue, self.wave_green, self.wave_red]
                result_arr = [self.snr_blue, self.snr_green, self.snr_red]

                output.display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave,
                                       result_arr, wave_arr)