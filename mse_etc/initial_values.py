"""Initial values module of MSE-ETC.

Modification Log:
    * 2021.01.19 - First created by Tae-Geun Ji & Soojong Pak
    * 2021.03.24 - Updated by Tae-Geun Ji
    * 2021.04.27 - Updated by Tae-Geun Ji
    * 2021.06.03 - Updated by Hojae Ahn
    * 2021.06.17 - Updated by Tae-Geun Ji
    * 2021.09.06 - Updated by Changgon Kim
    * 2023.06.14 - Updated by Tae-Geun Ji
"""

# Colors
c0 = "midnight blue"
c1 = "light blue"
c2 = "lavender"
c3 = "white"
c4 = "black"

# Titles
etc_title = "MSE Exposure Time Calculator"
etc_version = "v1.3.1"
etc_date = "20231115"
etc_editor = "TJ"

# Gui parameters
airmass = 1
pwv = 1
exp_time = 1200
exp_number = 3
snr = 200
min_mag = 18.0
max_mag = 26.0
wave = 482
sky = [20.7, 20.7, 20.7, 20.7, 20.7]
min_wave = 360
max_wave = 1800
