"""Output module of MSE-ETC.


Modification Log:
    * 2021.01.19 - First created by Tae-Geun Ji & Soojong Pak
    * 2021.02.25 - Version 0.1.2 was updated by Taeeun Kim
    * 2021.03.24 - Updated by Tae-Geun Ji
    * 2021.03.29 - Updated by Tae-Geun Ji
    * 2021.04.09 - Updated by Hojae Ahn
    * 2021.05.18 - Updated by Changgon Kim
    * 2021.06.03 - Updated by Hojae Ahn
"""

from parameters import *
from pylab import *
import initial_values as ini
import matplotlib.pyplot as plt
import gui
import time


def print_info_single(n, airmass, pwv, exp_t, exp_n, mag, sky, data):
    print('Airmass           = %.1f' % airmass)
    print('PWV [mm]          = %.1f' % pwv)
    print('Exposure Time [s] = %d' % exp_t)
    print('Exposure Number   = %d' % exp_n)
    print(' ')
    print('Band\t Mag. \t Sky \t S/N')

    band = ['[Blue]', '[Green]', '[Red]', '[NIR]']

    for i in range(n):
        print('%s\t %.2f \t %.2f \t ' % (band[i], mag[i], sky[i]), end='')
        if data[i] == 0.0:
            print('N/A')
        else:
            print('%f' % (data[i]))


def print_info_exp_time(n, airmass, pwv, target_sn, mag, sky, data):
    print('Airmass           = %.1f' % airmass)
    print('PWV [mm]          = %.1f' % pwv)
    print('Exposure Number   = 1')
    print('Target S/N   = %d' % target_sn)
    print(' ')
    print('Band\t Mag. \t Sky \t ExpTime [s]')

    band = ['[Blue]', '[Green]', '[Red]', '[NIR]']

    for i in range(n):
        print('%s\t %.2f \t %.2f \t ' % (band[i], mag[i], sky[i]), end='')
        if data[i] == 0.0:
            print('N/A')
        else:
            print('%f' % (data[i]))


def display_single(res_mode, airmass, pwv, exp_t, exp_n, mag, sky, data, wave, overlap):

    if gui.MainGUI.save:
        filename = save_single(res_mode, airmass, pwv, exp_t, exp_n, mag, sky, data, wave, overlap)

    print('==========================================================================')
    print('The calculation Signal-to-Noise from single magnitude input')
    print(' ')

    if res_mode == "LR":
        print('Resolution Mode   = Low Resolution')
        n = len(CTR_LR)
        print_info_single(n, airmass, pwv, exp_t, exp_n, mag, sky, data)
        print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_LR[4]))
        if overlap is True:
            print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[5], sky[5], data[5], BAND_LR[5]))

    elif res_mode == "MR":
        print('Resolution Mode   = Moderate Resolution')
        n = len(CTR_MR)
        print_info_single(n, airmass, pwv, exp_t, exp_n, mag, sky, data)
        print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[3], sky[3], data[3], BAND_MR[3]))

    elif res_mode == "HR":
        print('Resolution Mode   = High Resolution')
        n = len(CTR_HR)
        print_info_single(n, airmass, pwv, exp_t, exp_n, mag, sky, data)
        print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[3], sky[3], data[3], BAND_HR[3]))
        if overlap is True:
            print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_HR[4]))


    """
    if res_mode == "LR":

        print('Resolution Mode   = Low Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print(' ')
        print('Band\t Mag. \t Sky \t S/N')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], data[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], data[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], data[2]))
        print('[NIR]\t %.2f \t %.2f \t %f' % (mag[3], sky[3], data[3]))
        # print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_LR[4]))

        # if overlap is True:
        #   print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[5], sky[5], data[5], BAND_LR[5]))

    elif res_mode == "MR":

        print('Resolution Mode   = Moderate Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print(' ')
        print('Band\t Mag. \t Sky \t S/N')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], data[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], data[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], data[2]))
        # print('[NIR]\t %.2f \t %.2f \t %f' % (mag[3], sky[3], data[3]))
        # print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_MR[4]))

    elif res_mode == "HR":

        print('Resolution Mode   = High Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print(' ')
        print('Band\t Mag. \t Sky \t S/N')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], data[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], data[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], data[2]))
    # print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[3], sky[3], data[3], BAND_HR[3]))

    # if overlap is True:
    #    print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_HR[4]))
    """

    if gui.MainGUI.save:
        display_simple_text("Data file (%s.txt) is saved." % filename)


def save_single(res_mode, airmass, pwv, exp_t, exp_n, mag, sky, data, wave, overlap):
    now = time.localtime()
    filename = '%d%02d%02d_%02d%02d%02d' % (now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
    f1 = open('./user_saved_data/%s.txt' % filename, 'w')

    f1.write('======================================================\n')
    f1.write('The calculation Signal-to-Noise from single magnitude input\n')
    f1.write('\n')

    if res_mode == "LR":

        f1.write('Resolution Mode   = Low Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('\n')
        f1.write('Band\t Mag. \t Sky \t S/N\n')
        f1.write('[Blue]\t %.2f \t %.2f \t %f\n' % (mag[0], sky[0], data[0]))
        f1.write('[Green]\t %.2f \t %.2f \t %f\n' % (mag[1], sky[1], data[1]))
        f1.write('[Red]\t %.2f \t %.2f \t %f\n' % (mag[2], sky[2], data[2]))
        f1.write('[NIR]\t %.2f \t %.2f \t %f\n' % (mag[3], sky[3], data[3]))
        f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[4], sky[4], data[4], BAND_LR[4]))

        if overlap is True:
            f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[5], sky[5], data[5], BAND_LR[5]))

    elif res_mode == "MR":

        f1.write('Resolution Mode   = Moderate Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('\n')
        f1.write('Band\t Mag. \t Sky \t S/N\n')
        f1.write('[Blue]\t %.2f \t %.2f \t %f\n' % (mag[0], sky[0], data[0]))
        f1.write('[Green]\t %.2f \t %.2f \t %f\n' % (mag[1], sky[1], data[1]))
        f1.write('[Red]\t %.2f \t %.2f \t %f\n' % (mag[2], sky[2], data[2]))
        f1.write('[NIR]\t %.2f \t %.2f \t %f\n' % (mag[3], sky[3], data[3]))
        f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[4], sky[4], data[4], BAND_MR[4]))

        if overlap is True:
            f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[5], sky[5], data[5], BAND_MR[5]))

    elif res_mode == "HR":

        f1.write('Resolution Mode   = High Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('\n')
        f1.write('Band\t Mag. \t Sky \t S/N\n')
        f1.write('[Blue]\t %.2f \t %.2f \t %f\n' % (mag[0], sky[0], data[0]))
        f1.write('[Green]\t %.2f \t %.2f \t %f\n' % (mag[1], sky[1], data[1]))
        f1.write('[Red]\t %.2f \t %.2f \t %f\n' % (mag[2], sky[2], data[2]))
        f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[3], sky[3], data[3], BAND_HR[3]))

        if overlap is True:
            f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[4], sky[4], data[4], BAND_HR[4]))

    f1.close()

    return filename


def display_simple_text(text):
    print('==========================================================================')
    print(text)


def display_exp_time(res_mode, airmass, pwv, target_sn, mag, sky, data, wave, overlap):

    if gui.MainGUI.save:
        filename = save_exp_time(res_mode, pwv, target_sn, mag, sky, data, overlap)

    print('==========================================================================')
    print('The calculation exposure time for target S/N')
    print(' ')

    if res_mode == "LR":
        print('Resolution Mode   = Low Resolution')
        n = len(CTR_LR)
        print_info_exp_time(n, airmass, pwv, target_sn, mag, sky, data)
        print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_LR[4]))
        if overlap is True:
            print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[5], sky[5], data[5], BAND_LR[5]))

    elif res_mode == "MR":
        print('Resolution Mode   = Moderate Resolution')
        n = len(CTR_MR)
        print_info_exp_time(n, airmass, pwv, target_sn, mag, sky, data)
        print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[3], sky[3], data[3], BAND_MR[3]))

    elif res_mode == "HR":
        print('Resolution Mode   = High Resolution')
        n = len(CTR_HR)
        print_info_exp_time(n, airmass, pwv, target_sn, mag, sky, data)
        print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[3], sky[3], data[3], BAND_HR[3]))
        if overlap is True:
            print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_HR[4]))


    """
    if res_mode == "LR":

        print('Resolution Mode   = Low Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Number   = 1')
        print('Target S/N   = %d' % target_sn)
        print(' ')
        print('Band\t Mag. \t Sky \t ExpTime [s]')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], data[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], data[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], data[2]))
        print('[NIR]\t %.2f \t %.2f \t %f' % (mag[3], sky[3], data[3]))
        #print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_LR[4]))

        #if overlap is True:
            #print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[5], sky[5], data[5], BAND_LR[5]))

    elif res_mode == "MR":

        print('Resolution Mode   = Moderate Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Number   = 1')
        print('Target S/N   = %d' % target_sn)
        print(' ')
        print('Band\t Mag. \t Sky \t ExpTime [s]')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], data[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], data[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], data[2]))
        #print('[NIR]\t %.2f \t %.2f \t %f' % (mag[3], sky[3], data[3]))
        #print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_MR[4]))
        
        #if overlap is True:
            #print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[5], sky[5], data[5], BAND_MR[5]))
        
    elif res_mode == "HR":

        print('Resolution Mode   = High Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Number   = 1')
        print('Target S/N   = %d' % target_sn)
        print(' ')
        print('Band\t Mag. \t Sky \t ExpTime [s]')
        print('[Blue]\t %.2f \t %.2f \t %f' % (mag[0], sky[0], data[0]))
        print('[Green]\t %.2f \t %.2f \t %f' % (mag[1], sky[1], data[1]))
        print('[Red]\t %.2f \t %.2f \t %f' % (mag[2], sky[2], data[2]))
        #print('[NIR]\t %.2f \t %.2f \t %f' % (mag[3], sky[3], data[3]))
        #print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[4], sky[4], data[4], BAND_HR[4]))
    
        #if overlap is True:
            #print('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)' % (wave, mag[5], sky[5], data[5], BAND_HR[5]))
        """

    if gui.MainGUI.save:
        display_simple_text("Data file (%s.txt) is saved." % filename)


def save_exp_time(res_mode, airmass, pwv, target_sn, mag, sky, data, wave, overlap):
    now = time.localtime()
    filename = '%d%02d%02d_%02d%02d%02d' % (now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
    f1 = open('./user_saved_data/%s.txt' % filename, 'w')

    f1.write('======================================================\n')
    f1.write('The calculation exposure time for target S/N\n')
    f1.write('\n')

    if res_mode == "LR":

        f1.write('Resolution Mode   = Low Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Number   = 1\n')
        f1.write('Target S/N   = %d\n' % target_sn)
        f1.write('\n')
        f1.write('Band\t Mag. \t Sky \t ExpTime [s]\n')
        f1.write('[Blue]\t %.2f \t %.2f \t %f\n' % (mag[0], sky[0], data[0]))
        f1.write('[Green]\t %.2f \t %.2f \t %f\n' % (mag[1], sky[1], data[1]))
        f1.write('[Red]\t %.2f \t %.2f \t %f\n' % (mag[2], sky[2], data[2]))
        f1.write('[NIR]\t %.2f \t %.2f \t %f\n' % (mag[3], sky[3], data[3]))
        f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[4], sky[4], data[4], BAND_LR[4]))

        if overlap is True:
            f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[5], sky[5], data[5], BAND_LR[5]))

    elif res_mode == "MR":

        f1.write('Resolution Mode   = Moderate Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Number   = 1\n')
        f1.write('Target S/N   = %d\n' % target_sn)
        f1.write('\n')
        f1.write('Band\t Mag. \t Sky \t ExpTime [s]\n')
        f1.write('[Blue]\t %.2f \t %.2f \t %f\n' % (mag[0], sky[0], data[0]))
        f1.write('[Green]\t %.2f \t %.2f \t %f\n' % (mag[1], sky[1], data[1]))
        f1.write('[Red]\t %.2f \t %.2f \t %f\n' % (mag[2], sky[2], data[2]))
       # f1.write('[NIR]\t %.2f \t %.2f \t %f\n' % (mag[3], sky[3], data[3]))
        f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[4], sky[4], data[4], BAND_MR[4]))

        if overlap is True:
            f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[5], sky[5], data[5], BAND_MR[5]))

    elif res_mode == "HR":

        f1.write('Resolution Mode   = High Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Number   = 1\n')
        f1.write('Target S/N   = %d\n' % target_sn)
        f1.write('\n')
        f1.write('Band\t Mag. \t Sky \t ExpTime [s]\n')
        f1.write('[Blue]\t %.2f \t %.2f \t %f\n' % (mag[0], sky[0], data[0]))
        f1.write('[Green]\t %.2f \t %.2f \t %f\n' % (mag[1], sky[1], data[1]))
        f1.write('[Red]\t %.2f \t %.2f \t %f\n' % (mag[2], sky[2], data[2]))
        f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[3], sky[3], data[3], BAND_HR[3]))

        if overlap is True:
            f1.write('[%.1f]\t %.2f \t %.2f \t %f \t (Band = %s)\n' % (wave, mag[4], sky[4], data[4], BAND_HR[4]))

    f1.close()
    return filename


def display_sn_mag(res_mode, airmass, pwv, exp_t, exp_n, min_mag, max_mag, mag_range, sky, result):

    if gui.MainGUI.save:
        filename = save_sn_mag(res_mode, airmass, pwv, exp_t, exp_n, min_mag, max_mag, mag_range, sky, result)

    print('==========================================================================')
    print('The calculation Signal-to-Noise vs. Magnitude')
    print(' ')

    if res_mode == "LR":

        print('Resolution Mode   = Low Resolution')
        print('Airmass           = %.1f' % airmass)
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

        plt.title('MSE-ETC' + ' ' + ini.etc_version + ' ' + '(t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')',fontsize=16)
        plt.xlabel('Point Target Magnitude (AB)', fontsize=15)
        plt.ylabel('Signal-to-Noise',fontsize=15)
        plt.legend(['Blue_LR', 'Green_LR', 'Red_LR', 'NIR_LR'], fontsize=15)

        locs, labels = plt.xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = plt.yticks()
        plt.setp(labels,'fontsize', 'large')

        ax.set_yscale('log')
        ax.axis([min_mag, max_mag, 1, 1000])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

    elif res_mode == "MR":

        print('Resolution Mode   = Moderate Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print('Magnitude Range [mag] : %.2f' % min_mag + ' - ' + '%.2f' % max_mag)
        print(' ')
        print('Band\t Sky')
        print('[Blue]\t %.2f' % (sky[0]))
        print('[Green]\t %.2f' % (sky[1]))
        print('[Red]\t %.2f' % (sky[2]))
        #print('[NIR]\t %.2f' % (sky[3]))

        plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

        ax = plt.subplot(111)
        ax.plot(mag_range, result[0], 'b', mag_range, result[1], 'g',
                mag_range, result[2], 'r', linewidth=1)

        plt.title('MSE-ETC' + ' ' + ini.etc_version + ' ' + '(t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')', fontsize=16)
        plt.xlabel('Point Target Magnitude (AB)', fontsize=15)
        plt.ylabel('Signal-to-Noise', fontsize=15)
        plt.legend(['Blue_MR', 'Green_MR', 'Red_MR'], fontsize=15)

        locs, labels = plt.xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = plt.yticks()
        plt.setp(labels, 'fontsize', 'large')

        ax.set_yscale('log')
        ax.axis([min_mag, max_mag, 1, 1000])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

    elif res_mode == "HR":

        print('Resolution Mode   = High Resolution')
        print('Airmass           = %.1f' % airmass)
        print('PWV [mm]          = %.1f' % pwv)
        print('Exposure Time [s] = %d' % exp_t)
        print('Exposure Number   = %d' % exp_n)
        print('Magnitude Range [mag] : %.2f' % min_mag + ' - ' + '%.2f' % max_mag)
        print(' ')
        print('Band\t Sky')
        print('[Blue]\t %.2f' % (sky[0]))
        print('[Green]\t %.2f' % (sky[1]))
        print('[Red]\t %.2f' % (sky[2]))
        #print('[NIR]\t %.2f' % (sky[3]))

        plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

        ax = plt.subplot(111)
        ax.plot(mag_range, result[0], 'b', mag_range, result[1], 'g',
                mag_range, result[2], 'r', linewidth=1)

        plt.title('MSE-ETC' + ' ' + ini.etc_version + ' ' + '(t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')', fontsize=16)
        plt.xlabel('Point Target Magnitude (AB)', fontsize=15)
        plt.ylabel('Signal-to-Noise', fontsize=15)
        plt.legend(['Blue_HR', 'Green_HR', 'Red_HR'], fontsize=15)

        locs, labels = plt.xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = plt.yticks()
        plt.setp(labels, 'fontsize', 'large')

        ax.set_yscale('log')
        ax.axis([min_mag, max_mag, 1, 1000])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

    if gui.MainGUI.save:
       display_simple_text("Data file (%s.txt) is saved." % filename)

    plt.show()


def save_sn_mag(res_mode, airmass, pwv, exp_t, exp_n, min_mag, max_mag, mag_range, sky, result):

    now = time.localtime()
    filename = '%d%02d%02d_%02d%02d%02d' % (now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
    f1 = open('./user_saved_data/%s.txt' % filename, 'w')

    f1.write('======================================================\n')
    f1.write('The calculation Signal-to-Noise vs. Magnitude\n')
    f1.write('\n')

    if res_mode == "LR":

        f1.write('Resolution Mode   = Low Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('Magnitude Range [mag] : %.2f' % min_mag + ' - ' + '%.2f\n' % max_mag)
        f1.write('\n')
        f1.write('Band\t Sky\n')
        f1.write('[Blue]\t %.2f\n' % (sky[0]))
        f1.write('[Green]\t %.2f\n' % (sky[1]))
        f1.write('[Red]\t %.2f\n' % (sky[2]))
        f1.write('[NIR]\t %.2f\n' % (sky[3]))

        f1.write('\n========== Plot data ==========\n')
        f1.write('Point Target Magnitude[ABmag]\tSNR_Blue\tSNR_Green\tSNR_Red\tSNR_NIR\n')
        for i in range(len(mag_range)):
            f1.write('%.3f\t%.3f\t%.3f\t%.3f\t%.3f\n' % (mag_range[i],result[0][i],result[1][i],result[2][i],result[3][i]))

    elif res_mode == "MR":

        f1.write('Resolution Mode   = Moderate Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('Magnitude Range [mag] : %.2f' % min_mag + ' - ' + '%.2f\n' % max_mag)
        f1.write('\n')
        f1.write('Band\t Sky\n')
        f1.write('[Blue]\t %.2f\n' % (sky[0]))
        f1.write('[Green]\t %.2f\n' % (sky[1]))
        f1.write('[Red]\t %.2f\n' % (sky[2]))
        #f1.write('[NIR]\t %.2f\n' % (sky[3]))

        f1.write('\n========== Plot data ==========\n')
        f1.write('Point Target Magnitude[ABmag]\tSNR_Blue\tSNR_Green\tSNR_Red\n')
        for i in range(len(mag_range)):
            f1.write('%.3f\t%.3f\t%.3f\t%.3f\t%.3f\n' % (mag_range[i],result[0][i],result[1][i],result[2][i]))

    elif res_mode == "HR":

        f1.write('Resolution Mode   = High Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('Magnitude Range [mag] : %.2f' % min_mag + ' - ' + '%.2f\n' % max_mag)
        f1.write('\n')
        f1.write('Band\t Sky\n')
        f1.write('[Blue]\t %.2f\n' % (sky[0]))
        f1.write('[Green]\t %.2f\n' % (sky[1]))
        f1.write('[Red]\t %.2f\n' % (sky[2]))
        #f1.write('[NIR]\t %.2f\n' % (sky[3]))

        f1.write('\n========== Plot data ===========\n')
        f1.write('Point Target Magnitude[ABmag]\tSNR_Blue\tSNR_Green\tSNR_Red\n')
        for i in range(len(mag_range)):
            f1.write('%.3f\t%.3f\t%.3f\t%.3f\n' % (mag_range[i],result[0][i],result[1][i],result[2][i]))
    f1.close()

    return filename


def display_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave, sn_arr, wave_arr):

    if gui.MainGUI.save:
        filename = save_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave, sn_arr, wave_arr)

    print('==========================================================================')
    print('The calculation Signal-to-Noise vs. Wavelength')
    print(' ')

    if res_mode == "LR":
        print('Resolution Mode   = Low Resolution')
        print('Airmass           = %.1f' % airmass)
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

        plt.title('MSE-ETC' + ' ' + ini.etc_version + ' '
                  + '(pwv=' + '%.1f' % pwv + ', t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')', fontsize=16)
        plt.xlabel('Wavelength', fontsize=15)
        plt.ylabel('SNR', fontsize=15)

        locs, labels = xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = yticks()
        plt.setp(labels, 'fontsize', 'large')

        plt.xlim([min_wave, max_wave])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)


    elif res_mode == "MR":

        print('Resolution Mode   = Moderate Resolution')
        print('Airmass           = %.1f' % airmass)
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

        plt.title('MSE-ETC' + ' ' + ini.etc_version + ' ' + '(pwv=' + '%.1f' % pwv + ', t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')',
                  fontsize=16)
        plt.xlabel('Wavelength', fontsize=15)
        plt.ylabel('SNR', fontsize=15)

        locs, labels = xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = yticks()
        plt.setp(labels, 'fontsize', 'large')

        plt.xlim([min_wave, max_wave])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

    elif res_mode == "HR":

        print('Resolution Mode   = High Resolution')
        print('Airmass           = %.1f' % airmass)
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

            plt.legend(fontsize=15)
        else:
            ax.plot(wave_arr, sn_arr, 'black', linewidth=1)
            plt.legend([wave_mode], fontsize=15)

        plt.title('MSE-ETC' + ' ' + ini.etc_version + ' ' + '(pwv=' + '%.1f' % pwv + ', t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')',
                  fontsize=16)
        plt.xlabel('Wavelength', fontsize=15)
        plt.ylabel('SNR', fontsize=15)

        locs, labels = xticks()
        plt.setp(labels, 'fontsize', 'large')
        locs, labels = yticks()
        plt.setp(labels, 'fontsize', 'large')

        plt.xlim([min_wave, max_wave])
        ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
        ax.grid(color='k', linestyle='-', which='major', linewidth=1)

    if gui.MainGUI.save:
        display_simple_text("Data file (%s.txt) is saved." % filename)

    plt.show()


def display_sn_wave_order(res_mode, wave_mode, order, airmass, pwv, exp_t, exp_n, mag, sky,
                          min_wave, max_wave, sn_arr, wave_arr):

    # if gui.MainGUI.save:
    #    filename = save_sn_wave(res_mode, wave_mode, order, pwv, exp_t, exp_n, mag, sky,
    #                            min_wave, max_wave, sn_arr, wave_arr)

    print('==========================================================================')
    print('The calculation Signal-to-Noise vs. Wavelength')
    print(' ')

    print('Resolution Mode   = High Resolution')
    print('Airmass           = %1.f' % airmass)
    print('PWV [mm]          = %.1f' % pwv)
    print('Exposure Time [s] = %d' % exp_t)
    print('Exposure Number   = %d' % exp_n)
    print('Magnitude = %.2f' % mag)
    print('Sky = %.2f' % sky)
    print('Order Index : ' + wave_mode)
    print('Calculated Wavelength Range [nm] : %.2f' % min_wave[0] + ' - ' + '%.2f' % max_wave[0])
    print('Calculated Wavelength Range [nm] : %.2f' % min_wave[1] + ' - ' + '%.2f' % max_wave[1])
    print(' ')

    plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')

    ax = plt.subplot(111)

    ax.plot(wave_arr[0], sn_arr[0], 'blue', linewidth=1, label=order + 1)
    ax.plot(wave_arr[1], sn_arr[1], 'red', linewidth=1, label=order)

    plt.legend(fontsize=15)

    plt.title('MSE-ETC' + ' ' + ini.etc_version + ' ' + '(Order =' + wave_mode + ' ' + 'pwv=' + '%.1f' % pwv
              + ', t=' + '%d' % exp_t + 's, N=' + '%d' % exp_n + ')', fontsize=16)
    plt.xlabel('Wavelength', fontsize=15)
    plt.ylabel('SNR', fontsize=15)

    locs, labels = xticks()
    plt.setp(labels, 'fontsize', 'large')
    locs, labels = yticks()
    plt.setp(labels, 'fontsize', 'large')

    plt.xlim([min_wave[0], max_wave[1]])

    ax.grid(color='k', linestyle='-', which='minor', linewidth=0.5)
    ax.grid(color='k', linestyle='-', which='major', linewidth=1)

    # if gui.MainGUI.save:
    #    display_simple_text("Data file (%s.txt) is saved." % filename)

    plt.show()


def save_sn_wave(res_mode, wave_mode, airmass, pwv, exp_t, exp_n, mag, sky, min_wave, max_wave, sn_arr, wave_arr):

    now = time.localtime()
    filename = '%d%02d%02d_%02d%02d%02d' % (now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
    f1 = open('./user_saved_data/%s.txt' % filename, 'w')

    f1.write('======================================================\n')
    f1.write('The calculation Signal-to-Noise vs. Wavelength\n')
    f1.write('\n')

    if res_mode == "LR":
        f1.write('Resolution Mode   = Low Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('Magnitude = %.2f\n' % mag)
        f1.write('Sky = %.2f\n' % sky)
        f1.write('Calculated Wavelength Range [nm] : %.2f' % min_wave + ' - ' + '%.2f\n' % max_wave)

        f1.write('\n========== Plot data ===========\n')

        if wave_mode == "Input Wave":
            f1.write('1. Blue\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[0][i], sn_arr[0][i]))

            f1.write('\n2. Green\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[1][i], sn_arr[1][i]))

            f1.write('\n3. Red\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[2][i], sn_arr[2][i]))

            f1.write('\n4. NIR\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[3][i], sn_arr[3][i]))
        """
        else:
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr)):
                f1.write('%.3f\t%.3f\n' % (wave_arr[i], sn_arr[i]))
        """

    elif res_mode == "MR":

        f1.write('Resolution Mode   = Moderate Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('Magnitude = %.2f\n' % mag)
        f1.write('Sky = %.2f\n' % sky)
        f1.write('Calculated Wavelength Range [nm] : %.2f' % min_wave + ' - ' + '%.2f\n' % max_wave)

        f1.write('\n========== Plot data ===========\n')

        if wave_mode == "Input Wave":
            f1.write('1. Blue\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[0][i], sn_arr[0][i]))

            f1.write('\n2. Green\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[1][i], sn_arr[1][i]))

            f1.write('\n3. Red\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[2][i], sn_arr[2][i]))
            """
            f1.write('\n4. NIR\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[3][i], sn_arr[3][i]))
            
        else:
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr)):
                f1.write('%.3f\t%.3f\n' % (wave_arr[i], sn_arr[i]))
            """

    elif res_mode == "HR":

        f1.write('Resolution Mode   = High Resolution\n')
        f1.write('Airmass           = %.1f\n' % airmass)
        f1.write('PWV [mm]          = %.1f\n' % pwv)
        f1.write('Exposure Time [s] = %d\n' % exp_t)
        f1.write('Exposure Number   = %d\n' % exp_n)
        f1.write('Magnitude = %.2f\n' % mag)
        f1.write('Sky = %.2f\n' % sky)
        f1.write('Calculated Wavelength Range [nm] : %.2f' % min_wave + ' - ' + '%.2f\n' % max_wave)

        f1.write('\n========== Plot data ===========\n')

        if wave_mode == "Input Wave":
            f1.write('1. Blue\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[0][i], sn_arr[0][i]))

            f1.write('\n2. Green\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[1][i], sn_arr[1][i]))

            f1.write('\n3. Red\n')
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr[0])):
                f1.write('%.3f\t%.3f\n' % (wave_arr[2][i], sn_arr[2][i]))
        """
        else:
            f1.write('Wavelength[nm]\tSNR\n')
            for i in range(len(wave_arr)):
                f1.write('%.3f\t%.3f\n' % (wave_arr[i], sn_arr[i]))
        """
    f1.close()

    return filename
