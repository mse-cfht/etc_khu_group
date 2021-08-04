# -*- coding: utf-8 -*-
"""Main module of mse etc.

Modification Log:
    * 2021.01.19 - First created by Tae-Geun Ji & Soojong Pak
    * 2021.02.25 - Version 0.1.2 was updated by Taeeun Kim
    * 2021.03.24 - Version 0.2.0 was updated by Tae-Geun Ji
    * 2021.04.09 - Version 0.3.0 was updated by Hojae Ahn
    * 2021.04.27 - Version 0.3.1 was updated by Mingyeong Yang
    * 2021.06.03 - Version 1.1.0 was updated by Hojae Ahn
	*
"""

from gui import *

if __name__ == '__main__':
    print('=========== ' + ini_etc_title + " " + ini_etc_version + " (" + ini_etc_date + ", " + ini_etc_editor + ') ============')
    root = Tk()
    root.title(ini_etc_title + " " + ini_etc_version + " (" + ini_etc_date + ", " + ini_etc_editor + ')') # change 20210324 by T-G. Ji
    frame = MainGUI(root)
    frame.mainloop()
