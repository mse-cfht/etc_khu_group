"""This is the graphical user interface (GUI) module of MSE-ETC.
This module defines the GUI of MSE-ETC.

Modification Log
2020.01.19 - First created by Tae-Geun Ji & Soojong Pak
2020.02.25 - Updated by Taeeun Kim
2020.03.24 - Updated by Tae-Geun Ji
"""

from initial_values import *
from tkinter import *
from tkinter import ttk
import functions
import interpolate
import tkinter.font as font


class MainGUI(Frame):  # change 20210324 by T-G. Ji: GUI renewal
    """Define the components of GUI."""

    def __init__(self, master):
        super(MainGUI, self).__init__(master)

        # ==== Size of Main Window
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        self.title_font = font.Font(family="Verdana", size=14)
        self.font = font.Font(family="Verdana", size=11)

        # ==== Settings for Title Window
        self.title_window = PanedWindow(self.master, orient="vertical")
        self.title_frame = LabelFrame(self.title_window)
        self.title_window.add(self.title_frame)
        self.title_window.place(x=0, y=0, width=800, height=135)

        self.image_logo = PhotoImage(file="mse_logo.png")
        self.label_logo = Label(self.title_window, image=self.image_logo)
        self.label_logo.place(x=0, y=0)

        # ==== Settings for Spectral Resolution Mode Window
        self.res_window = PanedWindow(self.master, orient="vertical")
        self.res_frame = LabelFrame(self.res_window, bg=c0, bd=0)
        self.res_window.add(self.res_frame)
        self.res_window.place(x=0, y=135, width=800, height=100)

        self.res_label = Label(self.res_window, text="Resolution Mode Selection",
                                      font=self.title_font, bg=c0, fg="white")
        self.res_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.resolution = StringVar()

        self.res_combo = ttk.Combobox(self.res_window, width=12, state="readonly",
                                             textvariable=self.resolution, font=self.font)
        self.res_combo.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.res_combo['values'] = ('LR', 'MR', 'HR')
        self.res_combo.current(0)

        # ==== Settings for Calculate Method Window
        self.mode_window = PanedWindow(self.master, orient="vertical")
        self.mode_frame = LabelFrame(self.mode_window, bg=c1, bd=0)
        self.mode_window.add(self.mode_frame)
        self.mode_window.place(x=0, y=235, width=800, height=100)

        self.mode_label = Label(self.mode_window, text="Calculation Mode Selection", font=self.title_font, bg=c1)
        self.mode_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.mode = StringVar()
        self.mode.set("S/N Calculation")

        self.single_radio = Radiobutton(self.mode_frame, text="S/N Calculation", variable=self.mode,
                                        value="S/N Calculation", font=self.font, bg=c1, command=self.ui_enable)
        self.single_radio.place(relx=0.2, rely=0.6, anchor=CENTER)

        self.single_radio = Radiobutton(self.mode_frame, text="S/N vs. Magnitude", variable=self.mode,
                                        value="S/N vs. Magnitude", font=self.font, bg=c1, command=self.ui_enable)
        self.single_radio.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.single_radio = Radiobutton(self.mode_frame, text="S/N vs. Wavelength", variable=self.mode,
                                        value="S/N vs. Wavelength", font=self.font, bg=c1, command=self.ui_enable)
        self.single_radio.place(relx=0.8, rely=0.6, anchor=CENTER)

        # ==== Settings for User Input Parameters Window
        self.input_window = PanedWindow(self.master, orient="vertical")
        self.input_frame = LabelFrame(self.input_window, bg=c2, bd=0)
        self.input_window.add(self.input_frame)
        self.input_window.place(x=0, y=335, width=800, height=400)

        self.input_label = Label(self.input_window, text="User Input Parameters", font=self.title_font, bg=c2)
        self.input_label.place(relx=0.5, rely=0.05, anchor=CENTER)

        # PWV
        self.pwv_label = Label(self.input_frame, text="PWV [mm] = ", font=self.font, bg=c2)
        self.pwv_label.place(x=190, y=50, anchor=E)
        self.pwv_entry = Entry(self.input_frame, width=6, justify=CENTER,
                               textvariable=DoubleVar(value=ini_pwv), font=self.font)
        self.pwv_entry.place(x=190, y=50, anchor=W)

        # Exposure Time
        self.exp_time_label = Label(self.input_frame, text="Exp. Time [sec] = ", font=self.font, bg=c2)
        self.exp_time_label.place(x=190, y=80, anchor=E)
        self.exp_time_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_exptime), font=self.font)
        self.exp_time_entry.place(x=190, y=80, anchor=W)

        # Number of Exposure
        self.exp_num_label = Label(self.input_frame, text="Number of Exp. = ", font=self.font, bg=c2)
        self.exp_num_label.place(x=190, y=110, anchor=E)
        self.exp_num_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                   textvariable=DoubleVar(value=ini_expnumber), font=self.font)
        self.exp_num_entry.place(x=190, y=110, anchor=W)

        # Target Magnitude (AB)
        self.magnitude_label = Label(self.input_frame, text="Target Magnitude (AB):", font=self.font, bg=c2)
        self.magnitude_label.place(x=20, y=170, anchor=W)

        self.mag_blue_label = Label(self.input_frame, text="Blue", font=self.font, bg=c2)
        self.mag_blue_label.place(x=20, y=200, anchor=W)
        self.mag_green_label = Label(self.input_frame, text="Green", font=self.font, bg=c2)
        self.mag_green_label.place(x=90, y=200, anchor=W)
        self.mag_red_label = Label(self.input_frame, text="Red", font=self.font, bg=c2)
        self.mag_red_label.place(x=160, y=200, anchor=W)
        self.mag_nir_label = Label(self.input_frame, text="NIR", font=self.font, bg=c2)
        self.mag_nir_label.place(x=230, y=200, anchor=W)

        self.mag_blue_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_min_mag), font=self.font)
        self.mag_blue_entry.place(x=20, y=230, anchor=W)
        self.mag_green_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                     textvariable=DoubleVar(value=ini_min_mag), font=self.font)
        self.mag_green_entry.place(x=90, y=230, anchor=W)
        self.mag_red_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                   textvariable=DoubleVar(value=ini_min_mag), font=self.font)
        self.mag_red_entry.place(x=160, y=230, anchor=W)
        self.mag_nir_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                   textvariable=DoubleVar(value=ini_min_mag), font=self.font)
        self.mag_nir_entry.place(x=230, y=230, anchor=W)

        self.set_wave_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_wave), font=self.font, bg="khaki")
        self.set_wave_entry.place(x=300, y=200, anchor=W)

        self.mag_wave_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_min_mag), font=self.font, bg="khaki")
        self.mag_wave_entry.place(x=300, y=230, anchor=W)

        # Sky Brightness (AB)
        self.sky_label = Label(self.input_frame, text="Sky Brightness (AB):", font=self.font, bg=c2)
        self.sky_label.place(x=20, y=290, anchor=W)

        self.sky_blue_label = Label(self.input_frame, text="Blue", font=self.font, bg=c2)
        self.sky_blue_label.place(x=20, y=320, anchor=W)
        self.sky_green_label = Label(self.input_frame, text="Green", font=self.font, bg=c2)
        self.sky_green_label.place(x=90, y=320, anchor=W)
        self.sky_red_label = Label(self.input_frame, text="Red", font=self.font, bg=c2)
        self.sky_red_label.place(x=160, y=320, anchor=W)
        self.sky_nir_label = Label(self.input_frame, text="NIR", font=self.font, bg=c2)
        self.sky_nir_label.place(x=230, y=320, anchor=W)

        self.sky_blue_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_sky[0]), font=self.font)
        self.sky_blue_entry.place(x=20, y=350, anchor=W)
        self.sky_green_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                     textvariable=DoubleVar(value=ini_sky[1]), font=self.font)
        self.sky_green_entry.place(x=90, y=350, anchor=W)
        self.sky_red_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                   textvariable=DoubleVar(value=ini_sky[2]), font=self.font)
        self.sky_red_entry.place(x=160, y=350, anchor=W)
        self.sky_nir_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                   textvariable=DoubleVar(value=ini_sky[3]), font=self.font)
        self.sky_nir_entry.place(x=230, y=350, anchor=W)

        self.sky_wave_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_sky[4]), font=self.font, bg="khaki")
        self.sky_wave_entry.place(x=300, y=350, anchor=W)

        # Mag. Range (AB)
        self.mag_range_label = Label(self.input_frame, text="Mag. Range (AB):", font=self.font, bg=c2)
        self.mag_range_label.place(x=400, y=80, anchor=W)

        self.min_mag_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                   textvariable=DoubleVar(value=ini_min_mag), font=self.font)
        self.min_mag_entry.place(x=550, y=80, anchor=W)
        self.max_mag_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                   textvariable=DoubleVar(value=ini_max_mag), font=self.font)
        self.max_mag_entry.place(x=640, y=80, anchor=W)

        self.bar_label = Label(self.input_frame, text="-", font=self.font, bg=c2)
        self.bar_label.place(x=620, y=80, anchor=W)

        # Wave. Range
        self.wave_range_label = Label(self.input_frame, text="Wave. Range:", font=self.font, bg=c2)
        self.wave_range_label.place(x=400, y=170, anchor=W)

        self.wave_mode = StringVar()
        self.wave_mode.set("Blue")

        self.wave_blue_radio = Radiobutton(self.input_frame, text="Blue", variable=self.wave_mode,
                                           value="Blue", command=self.ui_wave_enable, font=self.font, bg=c2)
        self.wave_blue_radio.place(x=520, y=170, anchor=W)

        self.wave_green_radio = Radiobutton(self.input_frame, text="Green", variable=self.wave_mode,
                                            value="Green", command=self.ui_wave_enable, font=self.font, bg=c2)
        self.wave_green_radio.place(x=520, y=200, anchor=W)

        self.wave_red_radio = Radiobutton(self.input_frame, text="Red", variable=self.wave_mode,
                                          value="Red", command=self.ui_wave_enable, font=self.font, bg=c2)
        self.wave_red_radio.place(x=520, y=230, anchor=W)

        self.wave_nir_radio = Radiobutton(self.input_frame, text="NIR", variable=self.wave_mode,
                                          value="NIR", command=self.ui_wave_enable, font=self.font, bg=c2)
        self.wave_nir_radio.place(x=520, y=260, anchor=W)

        self.set_wave_radio = Radiobutton(self.input_frame, text="", variable=self.wave_mode,
                                          value="Input Wave", command=self.ui_wave_enable, font=self.font, bg=c2)
        self.set_wave_radio.place(x=520, y=290, anchor=W)

        self.min_wave_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_min_wave), font=self.font, bg="khaki")
        self.min_wave_entry.place(x=550, y=290, anchor=W)

        self.max_wave_entry = Entry(self.input_frame, width=6, justify=CENTER,
                                    textvariable=DoubleVar(value=ini_max_wave), font=self.font, bg="khaki")
        self.max_wave_entry.place(x=640, y=290, anchor=W)

        self.bar_label = Label(self.input_frame, text="-", font=self.font, bg=c2)
        self.bar_label.place(x=620, y=290, anchor=W)

        # Run
        self.execute_window = PanedWindow(self.master, orient="vertical")
        self.execute_frame = LabelFrame(self.execute_window, bg=c0, bd=0)
        self.execute_window.add(self.execute_frame)
        self.execute_window.place(x=0, y=735, width=800, height=65)

        self.run_button = Button(self.execute_frame, text="RUN", width=15, command=self.run, font=self.font, bg="white")
        self.run_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Global variables
        self.mag = 0
        self.sky = 0
        self.min_wave = 0
        self.max_wave = 0

        # GUI Initialization
        self.ui_enable()
        self.ui_wave_enable()

        self.mode_func = functions.Functions()
        print('...... Done!')


    def ui_target_magnitude(self, status):  # add 20210324 by T-G. Ji
        self.mag_blue_entry.config(state=status)
        self.mag_green_entry.config(state=status)
        self.mag_red_entry.config(state=status)
        self.mag_nir_entry.config(state=status)
        self.set_wave_entry.config(state=status)
        self.mag_wave_entry.config(state=status)

    def ui_sky_brightness(self, status):  # add 20210324 by T-G. Ji
        self.sky_blue_entry.config(state=status)
        self.sky_green_entry.config(state=status)
        self.sky_red_entry.config(state=status)
        self.sky_nir_entry.config(state=status)
        self.sky_wave_entry.config(state=status)

    def ui_mag_range(self, status):  # add 20210324 by T-G. Ji
        self.min_mag_entry.config(state=status)
        self.max_mag_entry.config(state=status)

    def ui_wave_range(self, status):  # add 20210324 by T-G. Ji
        self.wave_blue_radio.config(state=status)
        self.wave_green_radio.config(state=status)
        self.wave_red_radio.config(state=status)
        self.wave_nir_radio.config(state=status)
        self.set_wave_radio.config(state=status)
        self.min_wave_entry.config(state=status)
        self.max_wave_entry.config(state=status)

        if status == 'normal':
            if self.wave_mode.get() != "Input Wave":
                self.min_wave_entry.config(state='disable')
                self.max_wave_entry.config(state='disable')

    def ui_enable(self):  # add 20210324 by T-G. Ji
        if self.mode.get() == "S/N Calculation":
            self.ui_mag_range('disable')
            self.ui_wave_range('disable')
            self.ui_target_magnitude('normal')
            self.ui_sky_brightness('normal')

        elif self.mode.get() == "S/N vs. Magnitude":
            self.ui_target_magnitude('disable')
            self.ui_wave_range('disable')
            self.ui_mag_range('normal')
            self.ui_sky_brightness('normal')

        elif self.mode.get() == "S/N vs. Wavelength":
            self.ui_target_magnitude('normal')
            self.ui_sky_brightness('disable')
            self.ui_mag_range('disable')
            self.ui_wave_range('normal')
            self.set_wave_entry.config(state='disable')

    def ui_wave_enable(self):  # add 20210324 by T-G. Ji
        if self.wave_mode.get() == "Input Wave":
            self.min_wave_entry.config(state='normal')
            self.max_wave_entry.config(state='normal')

        else:
            self.min_wave_entry.config(state='disable')
            self.max_wave_entry.config(state='disable')

    # change 20210324 by T-G. Ji
    def run(self):
        res_mode = self.res_combo.get()
        wave_mode = self.wave_mode.get()
        cal_mode = self.mode.get()
        set_wave = float(self.set_wave_entry.get())
        pwv = float(self.pwv_entry.get())
        exp_t = float(self.exp_time_entry.get())
        exp_n = float(self.exp_num_entry.get())
        min_mag = float(self.min_mag_entry.get())
        max_mag = float(self.max_mag_entry.get())

        mag_arr = [float(self.mag_blue_entry.get()), float(self.mag_green_entry.get()),
                   float(self.mag_red_entry.get()), float(self.mag_nir_entry.get()),
                   float(self.mag_wave_entry.get()), float(self.mag_wave_entry.get())]

        sky_arr = [float(self.sky_blue_entry.get()), float(self.sky_green_entry.get()),
                   float(self.sky_red_entry.get()), float(self.sky_nir_entry.get()),
                   float(self.sky_wave_entry.get()), float(self.sky_wave_entry.get())]

        # change 20210325 by T-G. Ji
        if res_mode == "LR":
            if cal_mode == "S/N Calculation":
                self.mode_func.signal_to_noise_low(res_mode, pwv, exp_t, exp_n, mag_arr, sky_arr, set_wave)

            elif cal_mode == "S/N vs. Magnitude":
                self.mode_func.plot_sn_mag(res_mode, pwv, exp_t, exp_n, min_mag, max_mag, sky_arr)

            elif cal_mode == "S/N vs. Wavelength":
                if wave_mode == "Blue":
                    self.mag = float(self.mag_blue_entry.get())
                    self.sky = float(self.sky_blue_entry.get())
                    self.min_wave = 360
                    self.max_wave = 560
                elif wave_mode == "Green":
                    self.mag = float(self.mag_green_entry.get())
                    self.sky = float(self.sky_green_entry.get())
                    self.min_wave = 540
                    self.max_wave = 740
                elif wave_mode == "Red":
                    self.mag = float(self.mag_red_entry.get())
                    self.sky = float(self.sky_red_entry.get())
                    self.min_wave = 715
                    self.max_wave = 985
                elif wave_mode == "NIR":
                    self.mag = float(self.mag_nir_entry.get())
                    self.sky = float(self.sky_nir_entry.get())
                    self.min_wave = 960
                    self.max_wave = 1320
                else:
                    self.mag = float(self.mag_wave_entry.get())
                    self.sky = float(self.sky_wave_entry.get())
                    self.min_wave = float(self.min_wave_entry.get())
                    self.max_wave = float(self.max_wave_entry.get())

                self.mode_func.plot_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n,
                                            self.mag, self.sky, self.min_wave, self.max_wave)
            else:
                return None