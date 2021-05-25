"""Initial values module of MSE-ETC.

Modification Log:
    * 2021.01.19 - First created by Tae-Geun Ji & Soojong Pak
    * 2021.03.24 - Updated by Tae-Geun Ji
    * 2021.04.27 - Updated by Tae-Geun Ji
"""

# ==== Initial Parameter Settings

# Colors
c0 = "midnight blue" # add 20210324 by Tae-Geun Ji
c1 = "light blue"
c2 = "lavender"

ini_etc_title = "MSE Exposure Time Calculator"  # add 20210324 by Tae-Geun Ji
ini_etc_version = "v1.0.0"  # change 20210427 by Tae-Geun Ji

ini_pwv = 1
ini_exptime = 1200
ini_expnumber = 3
ini_sn = 200
ini_min_mag = 18.0
ini_max_mag = 26.0
ini_wave = 482
ini_sky = [20.7, 20.7, 20.7, 20.7, 20.7]         # Sky brightness in V-band [mag arcsec-2]
ini_min_wave= 360
ini_max_wave = 1320
