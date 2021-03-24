# calculation parameters

from math import *

from numpy import *
import numpy as np
from numpy import convolve

from pylab import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, OldScalarFormatter

#================================================
# Reading Telluric absorption and emission data table

#print('>>>>>>>>>>>>>>> ' + ETC_version + ' <<<<<<<<<<<<<<<')

# Tau atmosphere
Tau_atmosphere_band = [0.95, 0.95]  

print('...... Reading Le_IGRINS_AM1_H_40000.dat ......')
ATMO_LE_H = genfromtxt("Le_IGRINS_AM1_H_40000.dat")
print('...... Reading Le_IGRINS_AM1_K_40000.dat ......')
ATMO_LE_K = genfromtxt("Le_IGRINS_AM1_K_40000.dat")

print('...... Reading Kim_IGRINS_OH_H_40000.dat ......')
OH_H = genfromtxt("Kim_IGRINS_OH_H_40000.dat")
print('...... Reading Kim_IGRINS_OH_K_40000.dat ......')
OH_K = genfromtxt("Kim_IGRINS_OH_K_40000.dat") 

#================================================

#This function calculate atmostphere transmission depended on wavelengh
def Get_Tau_atmo(wavelength, transmission2, transmission4, transmission8, pwv):
    N_data = len(wavelength)
    y = np.zeros(N_data)
#    if pwv >= 1 and pwv <= 2:
#        for i in np.arange(0, N_data):
#            y[i] = transmission1[i] + (pwv - 1) * (transmission2[i] - transmission1[i])
    if pwv >= 2 and pwv <= 4:
        for i in np.arange(0, N_data):
            y[i] = transmission2[i] + (pwv - 2) * (transmission4[i] - transmission2[i]) / (4 - 2)
    elif pwv > 4 and pwv <= 8:
        for i in np.arange(0, N_data):
            y[i] = transmission4[i] + (pwv - 4) * (transmission8[i] - transmission4[i]) / (8 - 4)
    return y

def cal_tau_atmo():
    #calculate tau_atmo 
    pwv_type = 2    #it can be 2-8
    Tau_atmosphere_H = Get_Tau_atmo(ATMO_LE_H[:,0], ATMO_LE_H[:,1], ATMO_LE_H[:,2], ATMO_LE_H[:,3], pwv_type)
    Tau_atmosphere_K = Get_Tau_atmo(ATMO_LE_K[:,0], ATMO_LE_K[:,1], ATMO_LE_K[:,2], ATMO_LE_K[:,3], pwv_type)
    #plot values
    plt.plot(ATMO_LE_H[:,0], Tau_atmosphere_H, linewidth=0.5)
    plt.xlabel('wavelength')
    plt.ylabel('throughput')
    plt.title('Tau_atmosphere')
    plt.show()
    plt.plot(ATMO_LE_K[:,0], Tau_atmosphere_K, linewidth=0.5)
    plt.xlabel('wavelength')
    plt.ylabel('throughput')
    plt.title('Tau_atmosphere')
    plt.show()
    #print Tau_atmo
    TAU_atmosphere_LR_H = [Tau_atmosphere_H[2550],Tau_atmosphere_H[3650],Tau_atmosphere_H[3600],Tau_atmosphere_H[3600]]
    TAU_atmosphere_LR_K = [Tau_atmosphere_K[2550],Tau_atmosphere_K[3650],Tau_atmosphere_K[3600],Tau_atmosphere_K[3600]]
    print(TAU_atmosphere_LR_H)
    print(TAU_atmosphere_LR_K)
     
   #  for i in np.arange(0, len(ATMO_LE_H)):
      #   print(Tau_atmosphere_H[i])
         
    # for i in np.arange(0, len(ATMO_LE_K)):
    #     print(Tau_atmosphere_K[i])

cal_tau_atmo()