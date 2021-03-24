"""
Created on Jan 19, 2020

@Author: Tae-Geun Ji and Soojong PAK
"""

from parameters import *
import output
import numpy as np
import math


def single_sn(r_mode, t_exp, n_exp, mag, sky, mag_wave):

    if r_mode == "LR":

        B_sky_LR = np.zeros(5)
        signal = np.zeros(5)
        noise = np.zeros(5)
        result = np.zeros(5)

        n = 5
        if mag_wave == 0:
            n = 4

        for i in range(0, n):
            B_sky_LR[i] = (t_exp * n_exp) * A_telescope * TAU_atmosphere_LR[i] * \
                          TAU_opt_LR[i] * TAU_IE_LR[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * LR[i])

        for i in range(0, n):
            signal[i] = (t_exp * n_exp) * A_telescope * TAU_atmosphere_LR[i] * \
                        TAU_opt_LR[i] * TAU_IE_LR[i] * S_ZM * 10.0 ** (-0.4 * mag[i]) / (h * LR[i])
            noise[i] = math.sqrt(signal[i] + B_sky_LR[i] + N_res * (t_exp * n_dark[i] + n_read[i] ** 2))
            result[i] = signal[i] / noise[i]

        output.display_single(r_mode, t_exp, n_exp, mag, sky, result, mag_wave)


def plot_sn_mag(r_mode, t_exp, n_exp, tmag, emag, sky):

    mag_index = np.arange(tmag, emag+0.5, 0.5)
    nlen = len(mag_index)

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

    if r_mode == "LR":
        B_sky_LR = np.zeros(4)

        for i in range(0, 4):
            B_sky_LR[i] = (t_exp*n_exp)*A_telescope*TAU_atmosphere_LR[i] * \
                          TAU_opt_LR[i]*TAU_IE_LR[i]*S_ZM*10.0**(-0.4*sky[i])/(h*LR[i])

        for i in range(0, nlen):
            signal_blue[i] = (t_exp*n_exp)*A_telescope*TAU_atmosphere_LR[0] * \
                             TAU_opt_LR[0]*TAU_IE_LR[0]*S_ZM*10.0**(-0.4*mag_index[i])/(h*LR[0])
            signal_green[i] = (t_exp*n_exp)*A_telescope*TAU_atmosphere_LR[1] * \
                             TAU_opt_LR[1]*TAU_IE_LR[1]*S_ZM*10.0**(-0.4*mag_index[i])/(h*LR[1])
            signal_red[i] = (t_exp*n_exp)*A_telescope*TAU_atmosphere_LR[2] * \
                             TAU_opt_LR[2]*TAU_IE_LR[2]*S_ZM*10.0**(-0.4*mag_index[i])/(h*LR[2])
            signal_nir[i] = (t_exp*n_exp)*A_telescope*TAU_atmosphere_LR[3] * \
                             TAU_opt_LR[3]*TAU_IE_LR[3]*S_ZM*10.0**(-0.4*mag_index[i])/(h*LR[3])

            noise_blue[i] = math.sqrt(signal_blue[i]+B_sky_LR[0]+N_res*(t_exp*n_dark[0]+n_read[0]**2))
            noise_green[i] = math.sqrt(signal_green[i]+B_sky_LR[1]+N_res*(t_exp*n_dark[1]+n_read[1]**2))
            noise_red[i] = math.sqrt(signal_red[i]+B_sky_LR[2]+N_res*(t_exp*n_dark[2]+n_read[2]**2))
            noise_nir[i] = math.sqrt(signal_nir[i]+B_sky_LR[3]+N_res*(t_exp*n_dark[3]+n_read[3]**2))

            result_blue[i] = signal_blue[i] / noise_blue[i]
            result_green[i] = signal_green[i] / noise_green[i]
            result_red[i] = signal_red[i] / noise_red[i]
            result_nir[i] = signal_nir[i] / noise_nir[i]

        arr_result = [result_blue, result_green, result_red, result_nir]
        output.display_sn_mag(r_mode, t_exp, n_exp, tmag, emag, mag_index, sky, arr_result)
'''
def plot_sn_wave(r_mode, t_exp, n_exp, mag, sky, twave, ewave, wave_mode):
    wave_index = np.arange(twave, ewave, 10)
    nlen = len(wave_index)

    signal = np.zeros(nlen)
    noise = np.zeros(nlen)
    result_wave = np.zeros(nlen)
    
    i = 4
    if r_mode == "LR":
        B_sky_LR= (t_exp * n_exp) * A_telescope * TAU_atmosphere_LR[i] * \
                      TAU_opt_LR[i] * TAU_IE_LR[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * LR[i])
        
        
        
        n = 5
        if mag_wave == 0:
            n = 4

        for i in range(0, n):
            B_sky_LR[i] = (t_exp * n_exp) * A_telescope * TAU_atmosphere_LR[i] * \
                          TAU_opt_LR[i] * TAU_IE_LR[i] * S_ZM * 10.0 ** (-0.4 * sky[i]) / (h * LR[i])

        for i in range(0, nlen):
            signal[i] = (t_exp * n_exp) * A_telescope * TAU_atmosphere_LR[i] * \
                        TAU_opt_LR[i] * TAU_IE_LR[i] * S_ZM * 10.0 ** (-0.4 * mag[i]) / (h * LR[i])
            noise[i] = math.sqrt(signal[i] + B_sky_LR[i] + N_res * (t_exp * n_dark[i] + n_read[i] ** 2))
            result[i] = signal[i] / noise[i]

        output.display_single(r_mode, t_exp, n_exp, mag, sky, result, mag_wave)
  '''
