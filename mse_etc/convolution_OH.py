from astropy.io import fits
from astropy.convolution import convolve, Box1DKernel, Gaussian1DKernel
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from datetime import datetime

"""

input : KIM_IGRINS_OH_H_40000.dat

output : MSE_AM1_box_OH_data_LR.fits

"""


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

data_wave = np.zeros(nlen1)
data_atmo = np.zeros(nlen1)

for i in range(0, nlen1):
    data_wave[i] = row_nir[i][0]*1000
    data_atmo[i] = row_nir[i][1]

# Convolution
k=1800

bin1 = float(k) / 40000.0
bin2 = float(k)/ 3000.0

binning = bin2 / bin1
print(binning)

#g1 = Box1DKernel(binning)
g1 = Gaussian1DKernel(binning)
z1 = convolve(data_atmo, g1)

# interpolate
func = interpolate.interp1d(data_wave, z1, kind='linear')
result = np.zeros(nlen1)
for i in range(0, nlen1):
    result[i] = func(data_wave[i])

#save result data to fits file

c1 = fits.Column(name='wavelength', array=data_wave, format='D')
c2 = fits.Column(name='result', array=result, format='D')

cols = fits.ColDefs([c1,c2])
table_hdu = fits.BinTableHDU.from_columns(cols)

primary_hdu = fits.PrimaryHDU()
primary_hdu.header['DATE'] = f'{day} {month} {year}'
table_hdu.header['DATE'] = f'{day} {month} {year}'


hdul = fits.HDUList([primary_hdu, table_hdu])

hdul.writeto('data/result_MSE_OH_data_LR.fits', overwrite=True)

# plot
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

ax = plt.subplot(111)
ax.plot(data_wave, data_atmo, 'red', linewidth=1, label='red')
ax.plot(data_wave, result, 'blue', linewidth=1, label='blue')

plt.xlim([1400,1800])
plt.legend(["R=40000(data)", f"R=3000(Gauissian)"], fontsize=15)

plt.xlabel('Wavelength (nm)', fontsize=15)
plt.ylabel('Transmission', fontsize=15)

plt.show()