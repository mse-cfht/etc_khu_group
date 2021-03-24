"""
Created on Jan 19, 2020

@Author: Tae-Geun Ji and Soojong PAK
"""

from initial_values import *
from functions import *
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from interpolate import *
import output

class MainGUI(Frame):

    def __init__(self, master):
        super(MainGUI, self).__init__(master)

        print('==========================================================================')
        print('MSE Exposure Time Calculator')
        print('Version = 0.1.2')

        # Global Parameters
        self.resolution = StringVar()
        self.mode = StringVar()
        self.mode.set("S/N Calculation")
        self.wave = StringVar()
        # UI settings for panels
        self.font_title = font.Font(family="Arial", size=14)

        self.mainframe = PanedWindow(self.master, orient="vertical")
        self.logo_frame = LabelFrame(self.mainframe, text="")
        self.combo_frame = LabelFrame(self.mainframe, text="Resolution Mode Selection")
        self.mode_frame = LabelFrame(self.mainframe, text="Calculation Mode Selection")
        self.input_frame = LabelFrame(self.mainframe, text="User Input Parameters")
        self.btn_frame = Frame(self.mainframe)

        self.mainframe.add(self.logo_frame)
        self.mainframe.add(self.combo_frame)
        self.mainframe.add(self.mode_frame)
        self.mainframe.add(self.input_frame)
        self.mainframe.add(self.btn_frame)
        self.mainframe.grid(padx=10, pady=10)

        # UI settings for title
        self.img = PhotoImage(file="mse_logo.png").subsample(6)
        self.label_logo = Label(self.logo_frame, image=self.img)
        self.label_logo.grid(row=0, column=0)

        self.label_title = Label(self.logo_frame, text="Exposure Time Calculator v0.1.2 (in development)",
                                 font=self.font_title)
        self.label_title.grid(row=1, column=0, padx=30, pady=5)

        # UI settings for resolution selection panel
        self.cmb_rmode = ttk.Combobox(self.combo_frame, width=13, state="readonly", textvariable=self.resolution)
        self.cmb_rmode.grid(row=0, column=0, padx=30, pady=10)
        self.cmb_rmode['values'] = ('LR', 'MR', 'HR')
        self.cmb_rmode.current(0)

        # UI settings for mode selection panel
        self.radio_single = Radiobutton(self.mode_frame, text="S/N Calculation", variable=self.mode,
                                        value="S/N Calculation", command=self.mode_select)
        self.radio_single.grid(row=0, column=1, padx=30, pady=10, sticky=W)

        self.radio_plot = Radiobutton(self.mode_frame, text="S/N vs. Magnitude", variable=self.mode,
                                      value="S/N vs. Magnitude", command=self.mode_select)
        self.radio_plot.grid(row=0, column=2, padx=60, pady=10)

        self.radio_plot = Radiobutton(self.mode_frame, text="S/N vs. Wavelength", variable=self.mode,
                                      value="S/N vs. Wavelength", command=self.mode_select)
        self.radio_plot.grid(row=0, column=3, padx=10, pady=10)

        # UI settings for User Input Parameters panel
        self.label_pwv = Label(self.input_frame, text="PWV [mm] =")
        self.label_pwv.grid(row=0, column=0, padx=30, sticky=W)
        self.edit_pwv = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_pwv))
        self.edit_pwv.grid(row=0, column=0, padx=150, sticky=W)

        self.label_exptime = Label(self.input_frame, text="Exp. Time [sec]  =")
        self.label_exptime.grid(row=1, column=0, padx=30, pady=5, sticky=W)
        self.edit_exptime = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_exptime))
        self.edit_exptime.grid(row=1, column=0, padx=150, sticky=W)

        self.label_number = Label(self.input_frame, text="Number of Exp. =")
        self.label_number.grid(row=2, column=0, padx=30, sticky=W)
        self.edit_number = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_expnumber))
        self.edit_number.grid(row=2, column=0, padx=150, sticky=W)

        self.label_empty = Label(self.input_frame, text="").grid(row=3, column=0)

        self.label_mag = Label(self.input_frame, text="Target Magnitude (AB):")
        self.label_mag.grid(row=4, column=0, padx=30, pady=5, sticky=W)

        self.label_mag_blue = Label(self.input_frame, text="Blue").grid(row=5, column=0, padx=30, sticky=W)
        self.label_mag_green = Label(self.input_frame, text="Green").grid(row=5, column=0, padx=90, sticky=W)
        self.label_mag_red = Label(self.input_frame, text="Red").grid(row=5, column=0, padx=150, sticky=W)
        self.label_mag_nir = Label(self.input_frame, text="NIR").grid(row=5, column=0, padx=210, sticky=W)

        self.edit_magB = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_tmag))
        self.edit_magB.grid(row=6, column=0, padx=30, sticky=W)
        self.edit_magG = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_tmag))
        self.edit_magG.grid(row=6, column=0, padx=90, sticky=W)
        self.edit_magR = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_tmag))
        self.edit_magR.grid(row=6, column=0, padx=150, sticky=W)
        self.edit_magN = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_tmag))
        self.edit_magN.grid(row=6, column=0, padx=210, sticky=W)

        self.edit_mag_wave = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_wave))
        self.edit_mag_wave.grid(row=5, column=0, padx=270, sticky=W)
        self.edit_magW = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_tmag))
        self.edit_magW.grid(row=6, column=0, padx=270, sticky=W)

        self.label_empty = Label(self.input_frame, text="").grid(row=7, column=0)

        self.label_sky = Label(self.input_frame, text="Sky Brightness (AB):").grid(row=8, column=0, padx=30, sticky=W)

        self.label_sky_blue = Label(self.input_frame, text="Blue").grid(row=9, column=0, padx=30, sticky=W)
        self.label_sky_green = Label(self.input_frame, text="Green").grid(row=9, column=0, padx=90, sticky=W)
        self.label_sky_red = Label(self.input_frame, text="Red").grid(row=9, column=0, padx=150, sticky=W)
        self.label_sky_nir = Label(self.input_frame, text="NIR").grid(row=9, column=0, padx=210, sticky=W)

        self.edit_skyB = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_sky[0]))
        self.edit_skyB.grid(row=10, column=0, padx=30, sticky=W)
        self.edit_skyG = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_sky[1]))
        self.edit_skyG.grid(row=10, column=0, padx=90, sticky=W)
        self.edit_skyR = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_sky[2]))
        self.edit_skyR.grid(row=10, column=0, padx=150, sticky=W)
        self.edit_skyN = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_sky[3]))
        self.edit_skyN.grid(row=10, column=0, padx=210, sticky=W)

        self.label_empty = Label(self.input_frame, text="").grid(row=11, column=0, padx=30, sticky=SW)

        # self.edit_sky_wave = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_wave))
        # self.edit_sky_wave.grid(row=8, column=0, padx=270, sticky=W)
        self.edit_skyW = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_sky[4]))
        self.edit_skyW.grid(row=10, column=0, padx=270, sticky=W)

        self.label_mag_range = Label(self.input_frame, text="Mag. Range (AB):")
        self.label_mag_range.grid(row=0, column=0, padx=90, sticky=E)

        self.edit_tmag = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_tmag))
        self.edit_tmag.grid(row=1, column=0, padx=135, sticky=E)
        self.edit_emag = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_emag))
        self.edit_emag.grid(row=1, column=0, padx=60, sticky=E)
        self.label_bar = Label(self.input_frame, text="-").grid(row=1, column=0, padx=120, sticky=E)

        self.label_wave_range = Label(self.input_frame, text="Wave. Range:")
        self.label_wave_range.grid(row=4, column=0, padx=110, sticky=E)

        self.radio_waveB = Radiobutton(self.input_frame, text="Blue", variable=self.mode,
                                        value="Blue", command=self.mode_select)
        self.radio_waveB.grid(row=5, column=0, padx=140, sticky=E)

        self.radio_waveG = Radiobutton(self.input_frame, text="Green", variable=self.mode,
                                      value="Green", command=self.mode_select)
        self.radio_waveG.grid(row=6, column=0, padx=131,sticky=E)

        self.radio_waveR = Radiobutton(self.input_frame, text="Red", variable=self.mode,
                                      value="Red", command=self.mode_select)
        self.radio_waveR.grid(row=7, column=0, padx=145, sticky=E)

        self.radio_waveN = Radiobutton(self.input_frame, text="NIR", variable=self.mode,
                                      value="NIR", command=self.mode_select)
        self.radio_waveN.grid(row=8, column=0, padx=145, sticky=E)

        self.radio_waveW = Radiobutton(self.input_frame, text=" ", variable=self.mode,
                                      value="Input", command=self.mode_select)
        self.radio_waveW.grid(row=9, column=0, padx=164, sticky=E)

        self.edit_twave = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_twave))
        self.edit_twave.grid(row=9, column=0, padx=115, sticky=E)
        self.edit_ewave = Entry(self.input_frame, width=7, justify=CENTER, textvariable=DoubleVar(value=ini_ewave))
        self.edit_ewave.grid(row=9, column=0, padx=40, sticky=E)
        self.label_bar = Label(self.input_frame, text="-").grid(row=9, column=0, padx=100, sticky=E)


        # Buttons
        self.btn_run = Button(self.btn_frame, text="Run", width=8, command=self.run)
        self.btn_run.grid(row=0, column=1, padx=1, pady=20)

        self.edit_tmag.config(state='disable')
        self.edit_emag.config(state='disable')
        self.edit_twave.config(state='disable')
        self.edit_ewave.config(state='disable')
        self.radio_waveB.config(state='disable')
        self.radio_waveG.config(state='disable')
        self.radio_waveR.config(state='disable')
        self.radio_waveN.config(state='disable')
        self.radio_waveW.config(state='disable')

    def mode_select(self):
        if self.mode.get() == "S/N Calculation":
            self.edit_magB.config(state='normal')
            self.edit_magG.config(state='normal')
            self.edit_magR.config(state='normal')
            self.edit_magN.config(state='normal')
            self.edit_mag_wave.config(state='normal')
            self.edit_magW.config(state='normal')
            self.edit_tmag.config(state='disable')
            self.edit_emag.config(state='disable')
            self.edit_skyB.config(state='normal')
            self.edit_skyG.config(state='normal')
            self.edit_skyR.config(state='normal')
            self.edit_skyN.config(state='normal')
            self.edit_skyW.config(state='normal')
            self.edit_twave.config(state='disable')
            self.edit_ewave.config(state='disable')
            self.radio_waveB.config(state='disable')
            self.radio_waveG.config(state='disable')
            self.radio_waveR.config(state='disable')
            self.radio_waveN.config(state='disable')
            self.radio_waveW.config(state='disable')


        elif self.mode.get() == "S/N vs. Magnitude":
            self.edit_magB.config(state='disable')
            self.edit_magG.config(state='disable')
            self.edit_magR.config(state='disable')
            self.edit_magN.config(state='disable')
            self.edit_mag_wave.config(state='disable')
            self.edit_magW.config(state='disable')
            self.edit_tmag.config(state='normal')
            self.edit_emag.config(state='normal')
            self.edit_skyB.config(state='normal')
            self.edit_skyG.config(state='normal')
            self.edit_skyR.config(state='normal')
            self.edit_skyN.config(state='normal')
            self.edit_skyW.config(state='normal')
            self.edit_twave.config(state='disable')
            self.edit_ewave.config(state='disable')
            self.radio_waveB.config(state='disable')
            self.radio_waveG.config(state='disable')
            self.radio_waveR.config(state='disable')
            self.radio_waveN.config(state='disable')
            self.radio_waveW.config(state='disable')

        elif self.mode.get() == "S/N vs. Wavelength":
            self.edit_magB.config(state='disable')
            self.edit_magG.config(state='disable')
            self.edit_magR.config(state='disable')
            self.edit_magN.config(state='disable')
            self.edit_mag_wave.config(state='disable')
            self.edit_magW.config(state='disable')
            self.edit_tmag.config(state='disable')
            self.edit_emag.config(state='disable')
            self.edit_skyB.config(state='disable')
            self.edit_skyG.config(state='disable')
            self.edit_skyR.config(state='disable')
            self.edit_skyN.config(state='disable')
            self.edit_skyW.config(state='disable')
            self.edit_twave.config(state='normal')
            self.edit_ewave.config(state='normal')
            self.radio_waveB.config(state='normal')
            self.radio_waveG.config(state='normal')
            self.radio_waveR.config(state='normal')
            self.radio_waveN.config(state='normal')
            self.radio_waveW.config(state='normal')


        elif self.mode.get() == "Blue":
            self.edit_magB.config(state='normal')
            self.edit_magG.config(state='disable')
            self.edit_magR.config(state='disable')
            self.edit_magN.config(state='disable')
            self.edit_magW.config(state='disable')
            self.edit_skyB.config(state='normal')
            self.edit_skyG.config(state='disable')
            self.edit_skyR.config(state='disable')
            self.edit_skyN.config(state='disable')
            self.edit_skyW.config(state='disable')
        elif self.mode.get() == "Green":
            self.edit_magB.config(state='disable')
            self.edit_magG.config(state='normal')
            self.edit_magR.config(state='disable')
            self.edit_magN.config(state='disable')
            self.edit_magW.config(state='disable')
            self.edit_skyB.config(state='disable')
            self.edit_skyG.config(state='normal')
            self.edit_skyR.config(state='disable')
            self.edit_skyN.config(state='disable')
            self.edit_skyW.config(state='disable')
        elif self.mode.get() == "Red":
            self.edit_magB.config(state='disable')
            self.edit_magG.config(state='disable')
            self.edit_magR.config(state='normal')
            self.edit_magN.config(state='disable')
            self.edit_magW.config(state='disable')
            self.edit_skyB.config(state='disable')
            self.edit_skyG.config(state='disable')
            self.edit_skyR.config(state='normal')
            self.edit_skyN.config(state='disable')
            self.edit_skyW.config(state='disable')
        elif self.mode.get() == "NIR":
            self.edit_magB.config(state='disable')
            self.edit_magG.config(state='disable')
            self.edit_magR.config(state='disable')
            self.edit_magN.config(state='normal')
            self.edit_magW.config(state='disable')
            self.edit_skyB.config(state='disable')
            self.edit_skyG.config(state='disable')
            self.edit_skyR.config(state='disable')
            self.edit_skyN.config(state='normal')
            self.edit_skyW.config(state='disable')
        elif self.mode.get() == "Input":
            self.edit_magB.config(state='disable')
            self.edit_magG.config(state='disable')
            self.edit_magR.config(state='disable')
            self.edit_magN.config(state='disable')
            self.edit_magW.config(state='normal')
            self.edit_skyB.config(state='disable')
            self.edit_skyG.config(state='disable')
            self.edit_skyR.config(state='disable')
            self.edit_skyN.config(state='disable')
            self.edit_skyW.config(state='normal')

    def run(self):

        mag_arr = [float(self.edit_magB.get()), float(self.edit_magG.get()),
                  float(self.edit_magR.get()), float(self.edit_magN.get()),
                   float(self.edit_magW.get())]

        sky_arr = [float(self.edit_skyB.get()), float(self.edit_skyG.get()),
                    float(self.edit_skyR.get()), float(self.edit_skyN.get()),
                   float(self.edit_skyW.get())]

        mag_wave = float(self.edit_mag_wave.get())

        r_mode = self.cmb_rmode.get()
        t_exp = float(self.edit_exptime.get())
        n_exp = float(self.edit_number.get())

        if self.mode.get() == "S/N Calculation":
            if mag_wave != 0:
                ADD_PARAMETERS(mag_wave)

            single_sn(self.cmb_rmode.get(), float(self.edit_exptime.get()),
                      float(self.edit_number.get()), mag_arr, sky_arr, mag_wave)

        elif self.mode.get() == "S/N vs. Magnitude":

            plot_sn_mag(self.cmb_rmode.get(), float(self.edit_exptime.get()),
                        float(self.edit_number.get()), float(self.edit_tmag.get()),
                        float(self.edit_emag.get()), sky_arr)

        elif self.mode.get() == "Blue":
            mag = float(self.edit_magB.get())
            sky = float(self.edit_skyB.get())
            twave = 360
            ewave = 560
            plot_sn_wave(r_mode, t_exp, n_exp, mag, sky, twave, ewave)


        elif self.mode.get() == "Green":
            mag = float(self.edit_magB.get())
            sky = float(self.edit_skyB.get())
            twave = 540
            ewave = 740
            plot_sn_wave(r_mode, t_exp, n_exp, mag, sky, twave, ewave)

        elif self.mode.get() == "Red":
            mag = float(self.edit_magR.get())
            sky = float(self.edit_skyR.get())
            twave = 715
            ewave = 985
            plot_sn_wave(r_mode, t_exp, n_exp, mag, sky, twave, ewave)


        elif self.mode.get() == "NIR":
            mag = float(self.edit_magN.get())
            sky = float(self.edit_skyN.get())
            twave = 960
            ewave = 1320
            plot_sn_wave(r_mode, t_exp, n_exp, mag, sky, twave, ewave)


        elif self.mode.get() == "Input":
            mag = float(self.edit_magW.get())
            sky = float(self.edit_skyW.get())
            twave = float(self.edit_twave.get())
            ewave = float(self.edit_ewave.get())
            plot_sn_wave(r_mode, t_exp, n_exp, mag, sky, twave, ewave)

def plot_sn_wave(r_mode, t_exp, n_exp, mag, sky, twave, ewave):
    if r_mode == "LR":
        wave_index = np.arange(twave, ewave, 1)
        nlen = len(wave_index)
        B_sky_LR = np.zeros(nlen)
        signal = np.zeros(nlen)
        noise = np.zeros(nlen)
        result = np.zeros(nlen)

        for i in range(0, nlen):
            ADD_PARAMETERS(wave_index[i])
            B_sky_LR[i] = (t_exp * n_exp) * A_telescope * TAU_atmosphere_LR[4] * \
                          TAU_opt_LR[4] * TAU_IE_LR[4] * S_ZM * 10.0 ** (-0.4 * sky) / (h * LR[4])
            signal[i] = (t_exp * n_exp) * A_telescope * TAU_atmosphere_LR[4] * \
                        TAU_opt_LR[4] * TAU_IE_LR[4] * S_ZM * 10.0 ** (-0.4 * mag) / (h * LR[4])
            noise[i] = math.sqrt(signal[i] + B_sky_LR[i] + N_res * (t_exp * n_dark[4] + n_read[4] ** 2))
            result[i] = signal[i] / noise[i]

        output.display_sn_wave(r_mode, t_exp, n_exp, mag, sky, result, twave, ewave, wave_index)
