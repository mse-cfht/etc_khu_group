"""This is the main module of MSE-ETC.
This module executes the MSE-ETC.

Modification Log
2020.01.19 - The first MSE-ETC version was created by Tae-Geun Ji & Soojong Pak
2020.02.25 - Version 0.1.2 was updated by Taeeun Kim
2020.03.24 - Version 0.2.0 was updated by Tae-Geun Ji
"""

from gui import *

if __name__ == '__main__':
    print('============= ' + ini_etc_title + " " + ini_etc_version + ' =============')
    root = Tk()
    root.title(ini_etc_title + " " + ini_etc_version) # change 20210324 by T-G. Ji
    frame = MainGUI(root)
    frame.mainloop()