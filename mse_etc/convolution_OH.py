"""OH line data convolution of MSE ETC.

Modification Log:
    * 2021.09.06 - Updated by Changgon Kim
"""

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from astropy.convolution import Box1DKernel, Gaussian1DKernel, convolve
from astropy.io import fits
from astropy.table import Table
from scipy import interpolate

"""

input : KIM_IGRINS_OH_H_40000.dat

output : MSE_AM1_box_OH_data_LR.fits

"""

class TelluricData:
    
    def __init__(self):
        
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        RES_before = 40000
        RES = 3000

        # part making skymodel .fits file from .dat
        p = np.genfromtxt('data/Kim_IGRINS_OH_H_40000.dat', encoding='ascii', names=('wavelength', 'emission'), dtype=None)

        c1 = fits.Column(name='wavelength', array=p['wavelength'], format='D')
        c2 = fits.Column(name='emission', array=p['emission'], format='D')

        cols = fits.ColDefs([c1, c2])
        table_hdu = fits.BinTableHDU.from_columns(cols)
        primary_hdu = fits.PrimaryHDU()
        primary_hdu.header['DATE'] = f'{day} {month} {year}'
        table_hdu.header['DATE'] = f'{day} {month} {year}'
        hdul = fits.HDUList([primary_hdu, table_hdu])

        hdul.writeto(f'data/Kim_IGRINS_OH_H_40000.fits', overwrite=True)

        # open FITS file
        fits_image_filename = f'data/Kim_IGRINS_OH_H_40000.fits'
        hdu_index = fits.open(fits_image_filename)

        # Read FITS file
        data1 = hdu_index[1].data
        hdu_index.close()

        row_nir = data1[0:]

        nlen1 = len(row_nir)

        self.data_wave = np.zeros(nlen1)
        self.data_atmo = np.zeros(nlen1)

        for i in range(0, nlen1):
            self.data_wave[i] = row_nir[i][0]*1000
            self.data_atmo[i] = row_nir[i][1]

        # Convolution
        k=1800

        bin1 = float(k) / 40000.0
        bin2 = float(k)/ 3000.0

        binning = bin2 / bin1

        #g1 = Box1DKernel(binning)
        g1 = Gaussian1DKernel(binning)
        z1 = convolve(self.data_atmo, g1)

        # interpolate
        self.func = interpolate.interp1d(self.data_wave, z1, kind='linear')
        self.result = np.zeros(nlen1)
        for i in range(0, nlen1):
            self.result[i] = self.func(self.data_wave[i])

    def save_file(self):
        #save result data to fits file

        c1 = fits.Column(name='wavelength', array=self.data_wave, format='D')
        c2 = fits.Column(name='result', array=self.result, format='D')

        cols = fits.ColDefs([c1,c2])
        table_hdu = fits.BinTableHDU.from_columns(cols)

        primary_hdu = fits.PrimaryHDU()
        primary_hdu.header['DATE'] = f'{day} {month} {year}'
        table_hdu.header['DATE'] = f'{day} {month} {year}'


        hdul = fits.HDUList([primary_hdu, table_hdu])

        hdul.writeto('data/result_MSE_OH_data_LR.fits', overwrite=True)

    def plot_data(self):        
        # plot
        plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

        ax = plt.subplot(111)
        ax.plot(self.data_wave, self.data_atmo, 'red', linewidth=1, label='red')
        ax.plot(self.data_wave, self.result, 'blue', linewidth=1, label='blue')

        plt.xlim([1400,1800])
        plt.legend(["R=40000(data)", f"R=3000(Gauissian)"], fontsize=15)

        plt.xlabel('Wavelength (nm)', fontsize=15)
        plt.ylabel('Transmission', fontsize=15)

        plt.show()