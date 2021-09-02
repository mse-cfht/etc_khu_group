"""Interpolation module of MSE ETC.

This module determines the atmospheric transmission depending on pwv 
and wavelength. This specifies transmission values affected by various 
variables using data preprocessed using convolution and interpolation.

Todo:
    * calculate the atmospheric throughput

Modification Log:
    * 2020.02.25 - First created by Taeeun Kim
    * 2020.03.24 - Updated by Tae-Geun Ji
    * 2020.03.29 - Updated by Tae-Geun Ji
    * 2021.04.21 - Updated by Mingyoeng Yang
    * 2021.04.26 - Updated by Mingyeong Yang
"""

from parameters import *
from scipy import interpolate
from astropy.io import fits
import numpy as np


# change 20210421 by MY
class Throughput:
    """ Determines the atmospheric throughput."""

    def __init__(self):

        print('...... Reading skytable for atmospheric throughput calculation.')

        # Atmospheric transmission data for low resolution
        blue_low_box_path = 'SKY/MSE_AM1_box_blue.fits'
        green_low_box_path = 'SKY/MSE_AM1_box_green.fits'
        red_low_box_path = 'SKY/MSE_AM1_box_red.fits'
        nir_low_box_path = 'SKY/MSE_AM1_box_nir.fits'

        # Atmospheric transmission data for moderate resolution
        blue_moderate_box_path = 'SKY/MSE_AM1_box_blue_MR.fits'
        green_moderate_box_path = 'SKY/MSE_AM1_box_green_MR.fits'
        red_moderate_box_path = 'SKY/MSE_AM1_box_red_MR.fits'
        nir_moderate_box_path = 'SKY/MSE_AM1_box_NIR_MR.fits'

        # Atmospheric transmission data for high resolution
        blue_high_box_path = 'SKY/MSE_AM1_box_blue_HR.fits'
        green_high_box_path = 'SKY/MSE_AM1_box_green_HR.fits'
        red_high_box_path = 'SKY/MSE_AM1_box_red_HR.fits'

        # read fits files and set data (LR)
        self.file_blue_low = fits.open(blue_low_box_path)
        self.file_green_low = fits.open(green_low_box_path)
        self.file_red_low = fits.open(red_low_box_path)
        self.file_nir_low = fits.open(nir_low_box_path)

        # read fits files and set data (MR)
        self.file_blue_moderate = fits.open(blue_moderate_box_path)
        self.file_green_moderate = fits.open(green_moderate_box_path)
        self.file_red_moderate = fits.open(red_moderate_box_path)
        self.file_nir_moderate = fits.open(nir_moderate_box_path)

        # read fits files and set data (HR)
        self.file_blue_high = fits.open(blue_high_box_path)
        self.file_green_high = fits.open(green_high_box_path)
        self.file_red_high = fits.open(red_high_box_path)

        # read data (LR)
        self.data_blue_low = self.file_blue_low[1].data
        self.data_green_low = self.file_green_low[1].data
        self.data_red_low = self.file_red_low[1].data
        self.data_nir_low = self.file_nir_low[1].data

        # read data (MR)
        self.data_blue_moderate = self.file_blue_moderate[1].data
        self.data_green_moderate = self.file_green_moderate[1].data
        self.data_red_moderate = self.file_red_moderate[1].data
        self.data_nir_moderate = self.file_nir_moderate[1].data

        # read data (HR)
        self.data_blue_high = self.file_blue_high[1].data
        self.data_green_high = self.file_green_high[1].data
        self.data_red_high = self.file_red_high[1].data

        # close files
        self.file_blue_low.close()
        self.file_green_low.close()
        self.file_red_low.close()
        self.file_nir_low.close()

        # close files
        self.file_blue_moderate.close()
        self.file_green_moderate.close()
        self.file_red_moderate.close()
        self.file_nir_moderate.close()

        # close files
        self.file_blue_high.close()
        self.file_green_high.close()
        self.file_red_high.close()

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

        self.index_order = []
        self.tau_wave_order = []
        self.data_tau_order = []

        self.data_wave = []
        self.data_tau = []

    def set_data(self, res_mode):
        """Sets the data array suitable for each resolution mode.

        params:
            res_mode (str): The resolution mode.
                * Low resolution
                * Moderate resolution
                * High resolution

        Raises:
        """

        if res_mode == "LR":

            self.wave_blue = self.data_blue_low.field(0)
            self.wave_green = self.data_green_low.field(0)
            self.wave_red = self.data_red_low.field(0)
            self.wave_nir = self.data_nir_low.field(0)

            self.atmo_blue = []
            self.atmo_blue = np.array([self.data_blue_low.field(1),
                                     self.data_blue_low.field(2),
                                     self.data_blue_low.field(3)])

            self.atmo_green = []
            self.atmo_green = np.array([self.data_green_low.field(1),
                                      self.data_green_low.field(2),
                                      self.data_green_low.field(3)])

            self.atmo_red = []
            self.atmo_red = np.array([self.data_red_low.field(1),
                                    self.data_red_low.field(2),
                                    self.data_red_low.field(3)])

            self.atmo_nir = []
            self.atmo_nir = np.array([self.data_nir_low.field(1),
                                    self.data_nir_low.field(2),
                                    self.data_nir_low.field(3)])


            data = np.loadtxt("Throughput_LR.dat")

            self.tau_wave = data[:, 0]
            self.tel_m1_zecoat_arr = data[:, 1]
            self.tel_wfc_adc_arr = data[:, 2]
            self.sip_fits_arr = data[:, 3]
            self.sip_arr = data[:, 4]
            self.data_tau_ie = data[:, 5]

        elif res_mode == "MR":

            self.wave_blue = self.data_blue_moderate.field(0)
            self.wave_green = self.data_green_moderate.field(0)
            self.wave_red = self.data_red_moderate.field(0)
            self.wave_nir = self.data_nir_moderate.field(0)

            self.atmo_blue = []
            self.atmo_blue = np.array([self.data_blue_moderate.field(1),
                                       self.data_blue_moderate.field(2),
                                       self.data_blue_moderate.field(3)])

            self.atmo_green = []
            self.atmo_green = np.array([self.data_green_moderate.field(1),
                                        self.data_green_moderate.field(2),
                                        self.data_green_moderate.field(3)])

            self.atmo_red = []
            self.atmo_red = np.array([self.data_red_moderate.field(1),
                                      self.data_red_moderate.field(2),
                                      self.data_red_moderate.field(3)])

            self.atmo_nir = []
            self.atmo_nir = np.array([self.data_nir_moderate.field(1),
                                      self.data_nir_moderate.field(1),
                                      self.data_nir_moderate.field(1)])


            data = np.loadtxt("Throughput_MR.dat")

            self.tau_wave = data[2:-2, 0]
            self.tel_m1_zecoat_arr = data[2:-2, 1]
            self.tel_wfc_adc_arr = data[2:-2, 2]
            self.sip_fits_arr = data[2:-2, 3]
            self.sip_arr = data[2:-2, 4]
            self.data_tau_ie = data[2:-2, 5]


        elif res_mode == "HR":

            self.wave_blue = self.data_blue_high.field(0)
            self.wave_green = self.data_green_high.field(0)
            self.wave_red = self.data_red_high.field(0)

            self.atmo_blue = []
            self.atmo_blue = np.array([self.data_blue_high.field(1),
                                       self.data_blue_high.field(2),
                                       self.data_blue_high.field(3)])

            self.atmo_green = []
            self.atmo_green = np.array([self.data_green_high.field(1),
                                        self.data_green_high.field(2),
                                        self.data_green_high.field(3)])

            self.atmo_red = []
            self.atmo_red = np.array([self.data_red_high.field(1),
                                      self.data_red_high.field(2),
                                      self.data_red_high.field(3)])

            self.atmo_nir = []
            self.atmo_nir = np.array([self.data_nir_low.field(1),
                                      self.data_nir_low.field(1),
                                      self.data_nir_low.field(1)])


            data = np.loadtxt("Throughput_HR.dat")

            self.tau_wave = data[2:-1, 0]
            self.tel_m1_zecoat_arr = data[2:-1, 1]
            self.tel_wfc_adc_arr = data[2:-1, 2]
            self.sip_fits_arr = data[2:-1, 3]
            self.sip_arr = data[2:-1, 4]
            self.data_tau_ie = data[2:-1, 5]


            data_order = np.loadtxt("Throughput_Order_HR.dat")
            self.index_order = data_order[:, 0]
            self.tau_wave_order = data_order[:, 1]
            self.data_tau_order = data_order[:, 2]

    def set_data_order(self, res_mode, order):
        if res_mode == "HR":
            num = len(self.index_order)

            count = 0
            for i in range(num):
                if self.index_order[i] == order:
                    count += 1

            self.data_wave = np.zeros(count)
            self.data_tau = np.zeros(count)

            k = 0
            for i in range(num):
                if self.index_order[i] == order:
                    self.data_wave[k] = self.tau_wave_order[i]
                    self.data_tau[k] = self.data_tau_order[i]
                    k += 1

    def tau_atmo_blue(self, pwv):
        """Returns the atmospheric throughput in blue wavelength.

        This fuction finds a specific atmospheric throughput suitable 
        for pwv. It uses 1-D inpolation of data array in the blue wavelength band.

        params:
            pwv (float): Precipitable Water Vapor.

        Returns:
            tau_atmo (float): The atmospheric throughput.

        """

        if pwv == 1.0:
            func = interpolate.interp1d(self.wave_blue, self.atmo_blue[0, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_blue)

        if pwv == 2.5:
            func = interpolate.interp1d(self.wave_blue, self.atmo_blue[1, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_blue)

        if pwv == 7.5:
            func = interpolate.interp1d(self.wave_blue, self.atmo_blue[2, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_blue)

        return self.tau_atmo

    def tau_atmo_green(self, pwv):
        """Returns the atmospheric throughput in green wavelength. """

        if pwv == 1.0:
            func = interpolate.interp1d(self.wave_green, self.atmo_green[0, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_green)

        if pwv == 2.5:
            func = interpolate.interp1d(self.wave_green, self.atmo_green[1, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_green)

        if pwv == 7.5:
            func = interpolate.interp1d(self.wave_green, self.atmo_green[2, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_green)

        return self.tau_atmo

    def tau_atmo_red(self, pwv):
        """Returns the atmospheric throughput in red wavelength. """


        if pwv == 1.0:
            func = interpolate.interp1d(self.wave_red, self.atmo_red[0, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_red)

        if pwv == 2.5:
            func = interpolate.interp1d(self.wave_red, self.atmo_red[1, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_red)

        if pwv == 7.5:
            func = interpolate.interp1d(self.wave_red, self.atmo_red[2, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_red)

        return self.tau_atmo

    def tau_atmo_nir(self, pwv):
        """Returns the atmospheric throughput in nir-infrared wavelength. """


        if pwv == 1.0:
            func = interpolate.interp1d(self.wave_nir, self.atmo_nir[0, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_nir)

        if pwv == 2.5:
            func = interpolate.interp1d(self.wave_nir, self.atmo_nir[1, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_nir)

        if pwv == 7.5:
            func = interpolate.interp1d(self.wave_nir, self.atmo_nir[2, :], kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(self.wave_nir)

        return self.tau_atmo

    def cal_tau_atmo(self, wave, transmission1, transmission2, transmission7, pwv):
        """Calculates the atmospheric throughput with parameters.

        This function estimates the transmission value corresponding to a specific pwv 
        by calculating transmission data with different pwv.

        params:
            wave (float): The wavelength band.
                * Blue 360- 560 nm
                * Green 540 - 740 nm
                * Red 715 - 985 nm
                * Nir 960 - x nm
            transmission1 (float): The atmospheric transmission extracted under pwv = 1.0.
            transmission2 (float): The atmospheric transmission extracted under pwv = 2.5.
            transmission7 (float): The atmospheric transmission extracted under pwv = 7.5.
            pwv (float): Precipitable Water Vapor.

        Returns: 
            y (float): The atmospheric transmission.

        Raises:

        """

        N_data = len(wave)
        y = np.zeros(N_data)

        if pwv >= 1 and pwv <= 2.5:
            for i in np.arange(0, N_data):
                y[i] = transmission1[i] + (pwv - 1) * (transmission2[i] - transmission1[i])
        elif pwv > 2.5 and pwv <= 7.5:
            for i in np.arange(0, N_data):
                y[i] = transmission2[i] + (pwv - 2.5) * (transmission7[i] - transmission2[i]) / (7.5 - 2.5)
        else:
            return print("tau_atmo calculation error occurred.")

        return y

    def get_tau_atmo_LR(self, band, input_airmass, input_pwv, input_wavelength):
        """Return the result value for input parameters.

        This function returns the atmospheric throughput according to the wavelength band and pwv
        inputed by the user, using the calculation defined in the middle level functions above. 

        params:
            input_pwv (float): pwv set by the user
            input_wavelength (float): wavelength band set by the user

        Returns: 
            tau_atmo (float): The atmospheric transmission

        Raises:

        """

        if band == 0:
            transmission1 = self.tau_atmo_blue(self.data_pwv[0])
            transmission2 = self.tau_atmo_blue(self.data_pwv[1])
            transmission7 = self.tau_atmo_blue(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_blue, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_blue, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(input_wavelength)

        if band == 1:
            transmission1 = self.tau_atmo_green(self.data_pwv[0])
            transmission2 = self.tau_atmo_green(self.data_pwv[1])
            transmission7 = self.tau_atmo_green(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_green, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_green, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(input_wavelength)

        if band == 2:
            transmission1 = self.tau_atmo_red(self.data_pwv[0])
            transmission2 = self.tau_atmo_red(self.data_pwv[1])
            transmission7 = self.tau_atmo_red(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_red, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_red, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(input_wavelength)

        if band == 3:
            transmission1 = self.tau_atmo_nir(self.data_pwv[0])
            transmission2 = self.tau_atmo_nir(self.data_pwv[1])
            transmission7 = self.tau_atmo_nir(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_nir, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_nir, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(input_wavelength)
        self.tau_atmo = self.tau_atmo / input_airmass
        return self.tau_atmo

    def get_tau_atmo_MR(self, band, input_airmass, input_pwv, input_wavelength):

        """Return the result value for input parameters.

                This function returns the atmospheric throughput according to the wavelength band and pwv
                inputed by the user, using the calculation defined in the middle level functions above.

                params:
                    input_pwv (float): pwv set by the user
                    input_wavelength (float): wavelength band set by the user

                Returns:
                    tau_atmo (float): The atmospheric transmission

                Raises:

                This part is implemented by Changgon Kim
                The reason using the wavelength end range of 543, 718, 1457 for each wavelength is because the interpolation fails when there are blank between other wavelengths.
                """

        if band == 0:
            transmission1_m = self.tau_atmo_blue(self.data_pwv[0])
            transmission2_m = self.tau_atmo_blue(self.data_pwv[1])
            transmission7_m = self.tau_atmo_blue(self.data_pwv[2])

            throughput_m = self.cal_tau_atmo(self.wave_blue, transmission1_m, transmission2_m, transmission7_m, input_pwv)
            func = interpolate.interp1d(self.wave_blue, throughput_m, kind='linear', fill_value="extrapolate")
            self.tau_atmo_m = func(input_wavelength)

        if band == 1:
            transmission1 = self.tau_atmo_green(self.data_pwv[0])
            transmission2 = self.tau_atmo_green(self.data_pwv[1])
            transmission7 = self.tau_atmo_green(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_green, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_green, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo_m = func(input_wavelength)

        if band == 2:
            transmission1 = self.tau_atmo_red(self.data_pwv[0])
            transmission2 = self.tau_atmo_red(self.data_pwv[1])
            transmission7 = self.tau_atmo_red(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_red, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_red, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo_m = func(input_wavelength)

        if band == 3:
            transmission1 = self.tau_atmo_nir(self.data_pwv[0])
            transmission2 = self.tau_atmo_nir(self.data_pwv[1])
            transmission7 = self.tau_atmo_nir(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_nir, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_nir, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo_m = func(input_wavelength)
        self.tau_atmo_m = self.tau_atmo_m / input_airmass
        return self.tau_atmo_m

    def get_tau_atmo_HR(self, band, input_airmass, input_pwv, input_wavelength):

        """Return the result value for input parameters.

                This function returns the atmospheric throughput according to the wavelength band and pwv
                inputed by the user, using the calculation defined in the middle level functions above.

                params:
                    input_pwv (float): pwv set by the user
                    input_wavelength (float): wavelength band set by the user

                Returns:
                    tau_atmo (float): The atmospheric transmission

                Raises:

                """

        if band == 0:
            transmission1 = self.tau_atmo_blue(self.data_pwv[0])
            transmission2 = self.tau_atmo_blue(self.data_pwv[1])
            transmission7 = self.tau_atmo_blue(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_blue, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_blue, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(input_wavelength)

        if band == 1:
            transmission1 = self.tau_atmo_green(self.data_pwv[0])
            transmission2 = self.tau_atmo_green(self.data_pwv[1])
            transmission7 = self.tau_atmo_green(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_green, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_green, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(input_wavelength)

        if band == 2:
            transmission1 = self.tau_atmo_red(self.data_pwv[0])
            transmission2 = self.tau_atmo_red(self.data_pwv[1])
            transmission7 = self.tau_atmo_red(self.data_pwv[2])

            throughput = self.cal_tau_atmo(self.wave_red, transmission1, transmission2, transmission7, input_pwv)
            func = interpolate.interp1d(self.wave_red, throughput, kind='linear', fill_value="extrapolate")
            self.tau_atmo = func(input_wavelength)
        self.tau_atmo = self.tau_atmo / input_airmass
        return self.tau_atmo

    def get_tau_order(self, wave): # Only consider to index for HR
        """ Returns the throughput values. """

        func_tau_order = interpolate.interp1d(self.data_wave, self.data_tau, kind='cubic', fill_value="extrapolate")
        result = func_tau_order(wave)

        return result

    def tau_opt_res(self, wave):
        """ Returns the optical values. """

        func_tel_m1_zecoat = interpolate.interp1d(self.tau_wave, self.tel_m1_zecoat_arr,
                                                  kind='cubic', fill_value="extrapolate")
        func_tel_wfc_adc = interpolate.interp1d(self.tau_wave, self.tel_wfc_adc_arr,
                                                kind='cubic', fill_value="extrapolate")
        func_sip_fits = interpolate.interp1d(self.tau_wave, self.sip_fits_arr,
                                             kind='cubic', fill_value="extrapolate")
        func_sip = interpolate.interp1d(self.tau_wave, self.sip_arr,
                                        kind='cubic', fill_value="extrapolate")

        # LR, MR, HR has same value for ENCL, TEL_MSTR, TEL_PFHS, SIP_POSS
        self.tau_opt = ENCL_LR * TEL_MSTR_LR * func_tel_m1_zecoat(wave) * TEL_PFHS_LR \
                       * func_tel_wfc_adc(wave) * SIP_POSS_LR * func_sip_fits(wave) * func_sip(wave)

        return self.tau_opt

    def tau_ie_res(self, wave):
        """ Returns the injection efficiency. """

        func_tau_ie = interpolate.interp1d(self.tau_wave, self.data_tau_ie, kind='cubic', fill_value="extrapolate")
        self.tau_ie = func_tau_ie(wave)

        return self.tau_ie
