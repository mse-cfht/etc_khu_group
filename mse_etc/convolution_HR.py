"""ESO sky model data convolution of MSE ETC.

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

input : skymodel_MSE_pwv{pwv_value}_{resolution}.dat

output : MSE_AM1_box_{resolution_wave_band}_MR.fits

"""


now = datetime.now()
year = now.year
month = now.month
day = now.day

pwv = [1.0, 2.5, 7.5]
res = [40000, 20000]
wave = {400, 482, 767}

# part making skymodel .fits file from .dat

for l in wave:
    p1 = np.genfromtxt(f'data/skymodel_MSE_pwv1.0_{l}.dat', encoding='ascii', names=('wavelength', 'tr'), dtype=None)
    p2 = np.genfromtxt(f'data/skymodel_MSE_pwv2.5_{l}.dat', encoding='ascii', names=('wavelength', 'tr'), dtype=None)
    p7 = np.genfromtxt(f'data/skymodel_MSE_pwv7.5_{l}.dat', encoding='ascii', names=('wavelength', 'tr'), dtype=None)

    c1 = fits.Column(name='wavelength', array = p1['wavelength'], format='D')
    c2 = fits.Column(name='pwv1.0', array=p1['tr'], format='D')
    c3 = fits.Column(name='pwv2.5', array=p2['tr'], format='D')
    c4 = fits.Column(name='pwv7.5', array=p7['tr'], format='D')

    c = [c1, c2, c3, c4]

    for r in range(1, 4):
        cols = fits.ColDefs([c1,c[r]])
        table_hdu = fits.BinTableHDU.from_columns(cols)
        primary_hdu = fits.PrimaryHDU()
        primary_hdu.header['DATE'] = f'{day} {month} {year}'
        table_hdu.header['DATE'] = f'{day} {month} {year}'
        hdul = fits.HDUList([primary_hdu, table_hdu])

        if r == 1:
            hdul.writeto(f'data/skymodel_MSE_pwv1.0_{l}.fits', overwrite=True)
        elif r == 2:
            hdul.writeto(f'data/skymodel_MSE_pwv2.5_{l}.fits', overwrite=True)
        elif r == 3:
            hdul.writeto(f'data/skymodel_MSE_pwv7.5_{l}.fits', overwrite=True)

#opening the .fits data
for l in pwv:
    # Open FITS file
    fits_image_filename = f'SKY/MSE_AM1_pwv{l}_50000.fits'
    hdu_index = fits.open(fits_image_filename)

    # Read FITS file
    data1 = hdu_index[1].data
    hdu_index.close()

    # distinguish wavelength Blue/Green/Red/NIR
    row_blue1 = data1[0:13665]                       #Blue 350-560nm
    row_green1 = data1[0:37463] #11443:28590
    row_red1 = data1[0:47224]

    nlen1 = len(row_red1)
    data_wave1 = np.zeros(nlen1)
    data_atmo1 = np.zeros(nlen1)
    for i in range(0, nlen1):
        data_wave1[i] = row_red1[i][0]
        data_atmo1[i] = row_red1[i][1]

    for k in wave:

        if k == 400.0:
            nlen1 = len(row_blue1)
            data_wave1 = np.zeros(nlen1)
            data_atmo1 = np.zeros(nlen1)
            for i in range(0, nlen1):
                data_wave1[i] = row_blue1[i][0]
                data_atmo1[i] = row_blue1[i][1]
        elif k == 482.0:
            nlen1 = len(row_green1)
            data_wave1 = np.zeros(nlen1)
            data_atmo1 = np.zeros(nlen1)
            for i in range(0, nlen1):
                data_wave1[i] = row_green1[i][0]
                data_atmo1[i] = row_green1[i][1]
        elif k == 767.0:
            nlen1 = len(row_red1)
            data_wave1 = np.zeros(nlen1)
            data_atmo1 = np.zeros(nlen1)
            for i in range(0, nlen1):
                data_wave1[i] = row_red1[i][0]
                data_atmo1[i] = row_red1[i][1]

        # Open FITS file for comparison
        fits_image_filename = f"data/skymodel_MSE_pwv{l}_{k}.fits"
        hdu_index = fits.open(fits_image_filename)
        
        # Read FITS file for comparison
        data2 = hdu_index[1].data
        hdu_index.close()

        index_start = 0
        index_end = len(data2)

        for t in range(0, len(data2)):

            if k == 400:
                if data2[t][0] <= 460:
                    index_end = t+1
                else:
                    break
            elif k == 482:
                if data2[t][0] <= 620:
                    index_end = t+1
                else:
                    break
            elif k == 767:
                break

        for s in range(0, len(data2)):

            if k == 400:
                break
            elif k == 482:
                if data2[s][0] >= 440:
                    index_start = s
                    break
            elif k == 767:
                if data2[s][0] >= 600:
                    index_start = s
                    break

        # print(data2[1][0], l, k, index_start, index_end)

        #distinguish wavelength Blue/Green/Red/NIR
        if k == 400:
            row_data = data2[index_start:index_end]
        elif k == 482:
            row_data = data2[index_start:index_end]
        elif k == 767:
            row_data = data2[index_start:index_end]

        """
        # distinguish wavelength Blue/Green/Red/NIR
        row_blue2 = data2[0:1199]                                 #350-510
        row_green2 = data2[1107:1910]                            #576-700
        row_red2 = data2[2609:3777]                               #737-900
        row_NIR2 = data2[3684:5978]                              #1457-1800
        """

        nlen2 = len(row_data)
        print(nlen1)
        print(nlen2)
        data_wave2 = np.zeros(nlen2)
        data_atmo2 = np.zeros(nlen2)

        for i in range(0, nlen2):
            data_wave2[i] = row_data[i][0]
            data_atmo2[i] = row_data[i][1]

        # Convolution
        bin1 = float(k) / 50000.0
        if k == 400:
            bin2 = float(k) / 40000.0
        elif k == 482:
            bin2 = float(k) / 40000.0
        elif k == 767:
            bin2 = float(k) / 20000.0
        binning = bin2 / bin1
        print(binning)

        #g1 = Box1DKernel(binning)
        g1 = Gaussian1DKernel(binning)
        z1 = convolve(data_atmo1, g1)

        # interpolate
        func = interpolate.interp1d(data_wave1, z1, kind='linear')
        result = np.zeros(nlen2)
        for i in range(0, nlen2):
            result[i] = func(data_wave2[i])

        #save result data to fits file

        c1 = fits.Column(name='wavelength', array=data_wave2, format='D')
        c2 = fits.Column(name='result', array=result, format='D')

        cols = fits.ColDefs([c1,c2])
        table_hdu = fits.BinTableHDU.from_columns(cols)

        primary_hdu = fits.PrimaryHDU()
        primary_hdu.header['DATE'] = f'{day} {month} {year}'
        table_hdu.header['DATE'] = f'{day} {month} {year}'
        
        name = ' '

        if k == 400:
            table_hdu.header['LAMDA'] = 'blue'
            name = 'blue'
        elif k == 482:
            table_hdu.header['LAMDA'] = 'green'
            name = 'green'
        elif k == 767:
            table_hdu.header['LAMDA'] = 'red'
            name = 'red'

        table_hdu.header['PWV'] = l
        if k == 400:
            table_hdu.header['R'] = 40000
        elif k ==482:
            table_hdu.header['R'] = 40000
        elif k == 767:
            table_hdu.header['R'] = 20000

        hdul = fits.HDUList([primary_hdu, table_hdu])
        hdul.writeto(f'data/result_MSE_pwv{l}_{name}_{k}.fits', overwrite=True)


        # plot
        plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

        ax = plt.subplot(111)
        ax.plot(data_wave1, data_atmo1, 'lightgreen', linewidth=1, label='lightgreen')
        ax.plot(data_wave2, data_atmo2, 'red', linewidth=1, label='red')
        ax.plot(data_wave2, result, 'blue', linewidth=1, label='blue')

        if k == 400:
            plt.xlim([360, 460])
        elif k == 482:
            plt.xlim([440, 620])
        elif k == 767:
            plt.xlim([600, 900])
        plt.legend(["R=50000(data)",f"R={k}(data)", f"R={k}(Boxcar)"], fontsize=15)

        plt.title(f'pwv = {l}', fontsize=16)
        plt.xlabel('Wavelength', fontsize=15)
        plt.ylabel('Transmission', fontsize=15)

        plt.show()
'''
#part saving the gaussian file
name = ' '

for k in wave:
    if k == 400:
        name = 'blue'
    elif k == 482:
        name = 'green'
    elif k == 767:
        name = 'red'
    filename_pwv1 = f'data/result_MSE_pwv1.0_{name}_{k}.fits'
    filename_pwv2 = f'data/result_MSE_pwv2.5_{name}_{k}.fits'
    filename_pwv7 = f'data/result_MSE_pwv7.5_{name}_{k}.fits'

    #open files
    file_pwv1 = fits.open(filename_pwv1)
    file_pwv2 = fits.open(filename_pwv2)
    file_pwv7 = fits.open(filename_pwv7)

    #set data
    data_pwv1 = file_pwv1[1].data
    data_pwv2 = file_pwv2[1].data
    data_pwv7 = file_pwv7[1].data

    #close files
    file_pwv1.close()
    file_pwv2.close()
    file_pwv7.close()

    #set wavelength and transmission
    wave = data_pwv1.field(0)
    atmo_pwv1 = data_pwv1.field(1)
    atmo_pwv2 = data_pwv2.field(1)
    atmo_pwv7 = data_pwv7.field(1)

    #set columns
    c1 = fits.Column(name='wavelength', array=wave, format='D')
    c2 = fits.Column(name='pwv1', array=atmo_pwv1, format='D')
    c3 = fits.Column(name='pwv2.5', array=atmo_pwv2, format='D')
    c4 = fits.Column(name='pwv7.5', array=atmo_pwv7, format='D')

    cols = fits.ColDefs([c1,c2,c3,c4])
    table_hdu = fits.BinTableHDU.from_columns(cols)

    primary_hdu = fits.PrimaryHDU()
    primary_hdu.header['DATE'] = f'{day} {month} {year}'
    table_hdu.header['DATE'] = f'{day} {month} {year}'

    hdul = fits.HDUList([primary_hdu, table_hdu])
    hdul.writeto(f'SKY/MSE_AM1_box_{name}_HR.fits', overwrite=True)
    hdul.writeto(f'SKY/MSE_AM1_box_{name}_HR.fits', overwrite=True)
'''


