# -*- coding: utf-8 -*-
"""Main module of mse etc.

Modification Log:
    * 2021.01.19 - First created by Tae-Geun Ji & Soojong Pak
    * 2021.02.25 - Version 0.1.2 was updated by Taeeun Kim
    * 2021.03.24 - Version 0.2.0 was updated by Tae-Geun Ji
    * 2021.04.09 - Version 0.3.0 was updated by Hojae Ahn
    * 2021.04.27 - Version 0.3.1 was updated by Mingyeong Yang
    * 2021.06.03 - Version 1.1.0 was updated by Hojae Ahn
    * 2021.06.17 - Version 1.2.0 was updated by Tae-Geun Ji
    * 2021.08.04 - Version 1.2.1 was updated by Changgon Kim
    * 2023.06.22 - Version 1.3.0 was updated by Tae-Geun Ji
"""

from tkinter import Tk

import initial_values as ini
from gui import MainGUI

if __name__ == '__main__':

    title_name = f'{ini.etc_title} {ini.etc_version} ({ini.etc_date}, {ini.etc_editor})'

    print('=========== ' + title_name + ' ============')
    
    root = Tk()
    root.title(title_name)
    frame = MainGUI(root)
    frame.mainloop()
