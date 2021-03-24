"""
Created on Jan 19, 2020

@Author: Tae-Geun Ji and Soojong PAK
"""

from pylab import *
import matplotlib.pyplot as plt


def display_single(r_mode, t_exp, n_exp, mag, sky, result, mag_wave):

    print('==========================================================================')
    print('The calculation Signal-to-Noise from single magnitude input')
    print(' ')

    if r_mode == "LR":

        print('Resolution Mode   = Low Resolution')
        print('Exposure Time [s] = %d' % t_exp)
        print('Exposure Number   = %d' % n_exp)
        print(' ')
        print('Band\t Mag. \t Sky \t S/N')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], result[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], result[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], result[2]))
        print('[NIR]\t %.2f \t %.2f \t %f' % (mag[3], sky[3], result[3]))
        if mag_wave != 0:
            print('[%d]\t %.2f \t %.2f \t %f' % (mag_wave, mag[4], sky[4], result[4]))

def display_sn_mag(r_mode, t_exp, n_exp, tmag, emag, mag_range, sky, result):

    print('==========================================================================')
    print('The calculation Signal-to-Noise vs. Magnitude')
    print(' ')

    if r_mode == "LR":

        print('Resolution Mode   = Low Resolution')
        print('Exposure Time [s] = %d' % t_exp)
        print('Exposure Number   = %d' % n_exp)
        print('Magnitude Range [mag] : %.2f' % tmag + ' - ' + '%.2f' % emag)
        print(' ')
        print('Band\t Sky')
        print('[Blue]\t %.2f' % (sky[0]))
        print('[Green]\t %.2f' % (sky[1]))
        print('[Red]\t %.2f' % (sky[2]))
        print('[NIR]\t %.2f' % (sky[3]))

        plt.figure(num=None,figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

        ax = plt.subplot(111)
        ax.plot(mag_range, result[0], 'b', mag_range, result[1], 'g',
                mag_range, result[2], 'r', mag_range, result[3], 'black', linewidth=1)

        plt.title('ETC version 0.1.0 (t=' + '%d' % t_exp + 's, N=' + '%d' % n_exp + ')',fontsize=16)
        plt.xlabel('Point Target Magnitude (AB)', fontsize=15)
        plt.ylabel('Signal-to-Noise',fontsize=15)
        plt.legend(['Blue_LR', 'Green_LR', 'Red_LR', 'NIR_LR'], fontsize=15)

        locs, labels = xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = yticks()
        plt.setp(labels,'fontsize', 'large')

        ax.set_yscale('log')
        ax.axis([tmag, emag, 1, 1000])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

        plt.show()

def display_sn_wave(r_mode, t_exp, n_exp, mag, sky, result, twave, ewave, wave_index):
    print('Resolution Mode   = Low Resolution')
    print('Exposure Time [s] = %d' % t_exp)
    print('Exposure Number   = %d' % n_exp)
    print('Wave Range [nm] : %d' % twave + ' ~ ' + '%d' % ewave)
    print('Mag = %s\t Sky = %s' % (mag, sky))
    print(wave_index)
    print(result)
    print(np.where(result == 210.94659852))
    plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
    plt.title('ETC version 0.1.2 (t=' + '%d' % t_exp + 's, N=' + '%d' % n_exp + ')', fontsize=16)
    plt.xlabel('Wavelength (nm)', fontsize=15)
    plt.ylabel('Signal-to-Noise', fontsize=15)
    plt.scatter(wave_index, result, s=0.5, c='k')
    plt.grid()
    plt.show()