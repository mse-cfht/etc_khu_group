"""
Created on Jan 19, 2020

@Author: Tae-Geun Ji and Soojong PAK
"""

from parameters import *
from pylab import *
import matplotlib.pyplot as plt


def display_single(res_mode, pwv, exp_t, exp_n, mag, sky, data, wave):

    print('==========================================================================')
    print('The calculation Signal-to-Noise from single magnitude input')
    print(' ')

    if res_mode == "LR":

        print('Resolution Mode   = Low Resolution')
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print(' ')
        print('Band\t Mag. \t Sky \t S/N')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], data[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], data[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], data[2]))
        print('[NIR]\t %.2f \t %.2f \t %f' % (mag[3], sky[3], data[3]))
        print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_LR[4]))

        if RES_LR[5] != -1:
            print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[5], sky[5], data[5], BAND_LR[5]))

def display_sn_mag(res_mode, pwv, exp_t, exp_n, min_mag, max_mag, mag_range, sky, result):

    print('==========================================================================')
    print('The calculation Signal-to-Noise vs. Magnitude')
    print(' ')

    if res_mode == "LR":

        print('Resolution Mode   = Low Resolution')
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print('Magnitude Range [mag] : %.2f' % min_mag + ' - ' + '%.2f' % max_mag)
        print(' ')
        print('Band\t Sky')
        print('[Blue]\t %.2f' % (sky[0]))
        print('[Green]\t %.2f' % (sky[1]))
        print('[Red]\t %.2f' % (sky[2]))
        print('[NIR]\t %.2f' % (sky[3]))

        plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

        ax = plt.subplot(111)
        ax.plot(mag_range, result[0], 'b', mag_range, result[1], 'g',
                mag_range, result[2], 'r', mag_range, result[3], 'black', linewidth=1)

        plt.title('ETC version 0.2.0 (t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')',fontsize=16)
        plt.xlabel('Point Target Magnitude (AB)', fontsize=15)
        plt.ylabel('Signal-to-Noise',fontsize=15)
        plt.legend(['Blue_LR', 'Green_LR', 'Red_LR', 'NIR_LR'], fontsize=15)

        locs, labels = xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = yticks()
        plt.setp(labels,'fontsize', 'large')

        ax.set_yscale('log')
        ax.axis([min_mag, max_mag, 1, 1000])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

        plt.show()


def display_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave, sn_arr, wave_arr):

    print('==========================================================================')
    print('The calculation Signal-to-Noise vs. Wavelength')
    print(' ')

    if res_mode == "LR":
        print('Resolution Mode   = Low Resolution')
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print('Magnitude = %.2f' % mag)
        print('Sky = %.2f' % sky)
        print('Calculated Wavelength Range [nm] : %.2f' % min_wave + ' - ' + '%.2f' % max_wave)
        print(' ')

        plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

        ax = plt.subplot(111)

        if wave_mode == "Input Wave":
            ax.plot(wave_arr[0], sn_arr[0], 'blue', linewidth=1, label='Blue')
            ax.plot(wave_arr[1], sn_arr[1], 'green', linewidth=1, label='Green')
            ax.plot(wave_arr[2], sn_arr[2], 'red', linewidth=1, label='Red')
            ax.plot(wave_arr[3], sn_arr[3], 'black', linewidth=1, label='NIR')

            plt.legend(fontsize=15)
        else:
            ax.plot(wave_arr, sn_arr, 'black', linewidth=1)
            plt.legend([wave_mode], fontsize=15)

        plt.title('ETC version 0.2.0 (pwv=' + '%.1f' % pwv + ', t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')',
                      fontsize=16)
        plt.xlabel('Wavelength', fontsize=15)
        plt.ylabel('SNR', fontsize=15)

        #plt.legend([wave_mode], fontsize=15)

        locs, labels = xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = yticks()
        plt.setp(labels, 'fontsize', 'large')

        # ax.set_yscale('log')
        plt.xlim([min_wave, max_wave])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

        plt.show()
        """
        else:
            print('Resolution Mode   = Low Resolution')
            print('PWV [mm]          = %.1f' % pwv)
            print('Exposure Time [s] = %d' % exp_t)
            print('Exposure Number   = %d' % exp_n)
            print('Magnitude = %.2f' % mag)
            print('Sky = %.2f' % sky)
            print('Calculated Wavelength Range [nm] : %.2f' % min_wave + ' - ' + '%.2f' % max_wave)
            print(' ')

            plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

            ax = plt.subplot(111)
            ax.plot(wave_arr, sn_arr, 'black', linewidth=1)

            plt.title('ETC version 0.2.0 (pwv=' + '%.1f' % pwv + ', t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')',
                      fontsize=16)
            plt.xlabel('Wavelength', fontsize=15)
            plt.ylabel('SNR',fontsize=15)
            plt.legend([wave_mode], fontsize=15)

            locs, labels = xticks()
            plt.setp(labels, 'fontsize', 'large')
            locs, labels = yticks()
            plt.setp(labels,'fontsize', 'large')

            #ax.set_yscale('log')
            plt.xlim([min_wave, max_wave])
            ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
            ax.grid(color='k', linestyle='-', which='major', linewidth=1)

            plt.show()
        """