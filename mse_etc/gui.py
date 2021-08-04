"""Graphical user interface (GUI) module of MSE-ETC.

Modification Log:
    * 2021.01.19 - First created by Tae-Geun Ji & Soojong Pak
    * 2021.02.25 - Updated by Taeeun Kim
    * 2021.03.24 - Updated by Tae-Geun Ji
    * 2021.04.09 - Updated by Hojae Ahn
    * 2021.06.03 - Updated by Hojae Ahn
    * 2021.06.17 - Updated by Tae-Geun Ji
"""

from parameters import *
import tkinter as tk
import tkinter.font as font
import numpy as np
import initial_values as ini
import functions


class MainGUI(tk.Frame):
    """Define the components of GUI."""
    save = False  # class variable for checking whether data will be saved

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # ==== Size of Main Window
        self.master.geometry("1000x800")
        self.master.resizable(False, False)

        self.font_section = font.Font(family="Verdana", size=13)
        self.font = font.Font(family="Arial", size=11)

        # ==== Settings for Title Window
        self.title_window = tk.PanedWindow(self.master, orient="vertical")
        self.title_frame = tk.LabelFrame(self.title_window, bg=ini.c0, bd=0)
        self.title_window.add(self.title_frame)
        self.title_window.place(x=0, y=0, width=1000, height=135)

        self.image_logo = tk.PhotoImage(file="mse_logo.png")
        self.label_logo = tk.Label(self.title_window, image=self.image_logo)
        self.label_logo.place(x=100, y=0)

        # ==== Settings for Spectral Resolution Mode Window  # change 20210603 hojae
        self.res_window = tk.PanedWindow(self.master, orient="vertical")
        self.res_frame = tk.LabelFrame(self.res_window, bg=ini.c0, bd=0)
        self.res_window.add(self.res_frame)
        self.res_window.place(x=0, y=135, width=1000, height=100)

        self.res_label = tk.Label(self.res_window, text="Resolution Mode Selection",
                                  font=self.font_section, bg=ini.c0, fg=ini.c3)
        self.res_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.resolution = tk.StringVar()
        self.resolution.set("LR")

        self.low_radio = tk.Radiobutton(self.res_frame, text="Low Resolution", variable=self.resolution,
                                        value="LR", font=self.font, fg=ini.c3, bg=ini.c0, selectcolor=ini.c4,
                                        command=self.ui_enable)
        self.low_radio.place(relx=0.25, rely=0.6, anchor=tk.CENTER)

        self.mod_radio = tk.Radiobutton(self.res_frame, text="Moderate Resolution", variable=self.resolution,
                                        value="MR", font=self.font, fg=ini.c3, bg=ini.c0, selectcolor=ini.c4,
                                        command=self.ui_enable)
        self.mod_radio.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.high_radio = tk.Radiobutton(self.res_frame, text="High Resolution", variable=self.resolution,
                                         value="HR", font=self.font, fg=ini.c3, bg=ini.c0, selectcolor=ini.c4,
                                         command=self.ui_enable)
        self.high_radio.place(relx=0.75, rely=0.6, anchor=tk.CENTER)

        # ==== Settings for Calculate Method Window
        self.mode_window = tk.PanedWindow(self.master, orient="vertical")
        self.mode_frame = tk.LabelFrame(self.mode_window, bg=ini.c1, bd=0)
        self.mode_window.add(self.mode_frame)
        self.mode_window.place(x=0, y=235, width=1000, height=100)

        self.mode_label = tk.Label(self.mode_window, text="Calculation Mode Selection",
                                   font=self.font_section, bg=ini.c1)
        self.mode_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.mode = tk.StringVar()
        self.mode.set("S/N Calculation")

        self.sn_radio = tk.Radiobutton(self.mode_frame, text="S/N Calculation", variable=self.mode,
                                       value="S/N Calculation", font=self.font, bg=ini.c1, command=self.ui_enable)
        self.sn_radio.place(relx=0.15, rely=0.6, anchor=tk.CENTER)

        self.exptime_radio = tk.Radiobutton(self.mode_frame, text="ExpTime Calculation", variable=self.mode,
                                            value="ExpTime Calculation", font=self.font, bg=ini.c1,
                                            command=self.ui_enable)
        self.exptime_radio.place(relx=0.37, rely=0.6, anchor=tk.CENTER)

        self.sn_mag_radio = tk.Radiobutton(self.mode_frame, text="S/N vs. Magnitude", variable=self.mode,
                                           value="S/N vs. Magnitude", font=self.font, bg=ini.c1, command=self.ui_enable)
        self.sn_mag_radio.place(relx=0.61, rely=0.6, anchor=tk.CENTER)

        self.sn_wave_radio = tk.Radiobutton(self.mode_frame, text="S/N vs. Wavelength", variable=self.mode,
                                            value="S/N vs. Wavelength", font=self.font, bg=ini.c1,
                                            command=self.ui_enable)
        self.sn_wave_radio.place(relx=0.84, rely=0.6, anchor=tk.CENTER)

        # ==== Settings for User Input Parameters Window
        self.input_window = tk.PanedWindow(self.master, orient="vertical")
        self.input_frame = tk.LabelFrame(self.input_window, bg=ini.c2, bd=0)
        self.input_window.add(self.input_frame)
        self.input_window.place(x=0, y=335, width=1000, height=400)

        self.input_label = tk.Label(self.input_window, text="User Input Parameters", font=self.font_section, bg=ini.c2)
        self.input_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        # PWV
        self.pwv_label = tk.Label(self.input_frame, text="PWV [mm] = ", font=self.font, bg=ini.c2)
        self.pwv_label.place(x=190, y=40, anchor=tk.E)
        self.pwv_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                  textvariable=tk.DoubleVar(value=ini.pwv), font=self.font)
        self.pwv_entry.place(x=190, y=40, anchor=tk.W)

        # Exposure Time
        self.exp_time_label = tk.Label(self.input_frame, text="Exp. Time [sec] = ", font=self.font, bg=ini.c2)
        self.exp_time_label.place(x=190, y=70, anchor=tk.E)
        self.exp_time_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.exp_time), font=self.font)
        self.exp_time_entry.place(x=190, y=70, anchor=tk.W)

        # Number of Exposure
        self.exp_num_label = tk.Label(self.input_frame, text="Number of Exp. = ", font=self.font, bg=ini.c2)
        self.exp_num_label.place(x=190, y=100, anchor=tk.E)
        self.exp_num_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                      textvariable=tk.DoubleVar(value=ini.exp_number), font=self.font)
        self.exp_num_entry.place(x=190, y=100, anchor=tk.W)

        # Target S/N #add 210408 hojae
        self.target_sn_label = tk.Label(self.input_frame, text="Target S/N = ", font=self.font, bg=ini.c2)
        self.target_sn_label.place(x=190, y=130, anchor=tk.E)
        self.target_sn_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                        textvariable=tk.DoubleVar(value=ini.snr), font=self.font)
        self.target_sn_entry.place(x=190, y=130, anchor=tk.W)

        # Target Magnitude (AB)
        self.magnitude_label = tk.Label(self.input_frame, text="Target Magnitude (AB):", font=self.font, bg=ini.c2)
        self.magnitude_label.place(x=20, y=170, anchor=tk.W)

        self.mag_blue_label = tk.Label(self.input_frame, text="Blue", font=self.font, bg=ini.c2)
        self.mag_blue_label.place(x=20, y=200, anchor=tk.W)
        self.mag_green_label = tk.Label(self.input_frame, text="Green", font=self.font, bg=ini.c2)
        self.mag_green_label.place(x=90, y=200, anchor=tk.W)
        self.mag_red_label = tk.Label(self.input_frame, text="Red", font=self.font, bg=ini.c2)
        self.mag_red_label.place(x=160, y=200, anchor=tk.W)
        self.mag_nir_label = tk.Label(self.input_frame, text="NIR", font=self.font, bg=ini.c2)
        self.mag_nir_label.place(x=230, y=200, anchor=tk.W)

        self.mag_blue_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.min_mag), font=self.font)
        self.mag_blue_entry.place(x=20, y=230, anchor=tk.W)
        self.mag_green_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                        textvariable=tk.DoubleVar(value=ini.min_mag), font=self.font)
        self.mag_green_entry.place(x=90, y=230, anchor=tk.W)
        self.mag_red_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                      textvariable=tk.DoubleVar(value=ini.min_mag), font=self.font)
        self.mag_red_entry.place(x=160, y=230, anchor=tk.W)
        self.mag_nir_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                      textvariable=tk.DoubleVar(value=ini.min_mag), font=self.font)
        self.mag_nir_entry.place(x=230, y=230, anchor=tk.W)

        self.set_wave_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.wave), font=self.font, bg="khaki")
        self.set_wave_entry.place(x=300, y=200, anchor=tk.W)

        self.mag_wave_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.min_mag), font=self.font, bg="khaki")
        self.mag_wave_entry.place(x=300, y=230, anchor=tk.W)

        # Sky Brightness (AB)
        self.sky_label = tk.Label(self.input_frame, text="Sky Brightness (AB):", font=self.font, bg=ini.c2)
        self.sky_label.place(x=20, y=290, anchor=tk.W)

        self.sky_blue_label = tk.Label(self.input_frame, text="Blue", font=self.font, bg=ini.c2)
        self.sky_blue_label.place(x=20, y=320, anchor=tk.W)
        self.sky_green_label = tk.Label(self.input_frame, text="Green", font=self.font, bg=ini.c2)
        self.sky_green_label.place(x=90, y=320, anchor=tk.W)
        self.sky_red_label = tk.Label(self.input_frame, text="Red", font=self.font, bg=ini.c2)
        self.sky_red_label.place(x=160, y=320, anchor=tk.W)
        self.sky_nir_label = tk.Label(self.input_frame, text="NIR", font=self.font, bg=ini.c2)
        self.sky_nir_label.place(x=230, y=320, anchor=tk.W)

        self.sky_blue_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.sky[0]), font=self.font)
        self.sky_blue_entry.place(x=20, y=350, anchor=tk.W)
        self.sky_green_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                        textvariable=tk.DoubleVar(value=ini.sky[1]), font=self.font)
        self.sky_green_entry.place(x=90, y=350, anchor=tk.W)
        self.sky_red_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                      textvariable=tk.DoubleVar(value=ini.sky[2]), font=self.font)
        self.sky_red_entry.place(x=160, y=350, anchor=tk.W)
        self.sky_nir_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                      textvariable=tk.DoubleVar(value=ini.sky[3]), font=self.font)
        self.sky_nir_entry.place(x=230, y=350, anchor=tk.W)

        self.sky_wave_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.sky[4]), font=self.font, bg="khaki")
        self.sky_wave_entry.place(x=300, y=350, anchor=tk.W)

        # Mag. Range (AB)
        self.mag_range_label = tk.Label(self.input_frame, text="Mag. Range (AB):", font=self.font, bg=ini.c2)
        self.mag_range_label.place(x=400, y=80, anchor=tk.W)

        self.min_mag_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                      textvariable=tk.DoubleVar(value=ini.min_mag), font=self.font)
        self.min_mag_entry.place(x=530, y=80, anchor=tk.W)
        self.max_mag_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                      textvariable=tk.DoubleVar(value=ini.max_mag), font=self.font)
        self.max_mag_entry.place(x=610, y=80, anchor=tk.W)

        self.bar_label = tk.Label(self.input_frame, text="-", font=self.font, bg=ini.c2)
        self.bar_label.place(x=590, y=80, anchor=tk.W)

        # Wavelength Range: Blue, Green, Red, NIR
        self.wave_range_label = tk.Label(self.input_frame, text="Wave. Range:", font=self.font, bg=ini.c2)
        self.wave_range_label.place(x=400, y=130, anchor=tk.W)

        self.wave_mode = tk.StringVar()
        self.wave_mode.set("Blue")

        self.wave_blue_radio = tk.Radiobutton(self.input_frame, text="Blue", variable=self.wave_mode,
                                              value="Blue", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_blue_radio.place(x=520, y=130, anchor=tk.W)

        self.wave_green_radio = tk.Radiobutton(self.input_frame, text="Green", variable=self.wave_mode,
                                               value="Green", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_green_radio.place(x=590, y=130, anchor=tk.W)

        self.wave_red_radio = tk.Radiobutton(self.input_frame, text="Red", variable=self.wave_mode,
                                             value="Red", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_red_radio.place(x=660, y=130, anchor=tk.W)

        self.wave_nir_radio = tk.Radiobutton(self.input_frame, text="NIR", variable=self.wave_mode,
                                             value="NIR", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_nir_radio.place(x=730, y=130, anchor=tk.W)

        self.set_wave_radio = tk.Radiobutton(self.input_frame, text="", variable=self.wave_mode,
                                             value="Input Wave", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.set_wave_radio.place(x=800, y=130, anchor=tk.W)

        self.min_wave_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.min_wave), font=self.font, bg="khaki")
        self.min_wave_entry.place(x=830, y=130, anchor=tk.W)

        self.max_wave_entry = tk.Entry(self.input_frame, width=6, justify=tk.CENTER,
                                       textvariable=tk.DoubleVar(value=ini.max_wave), font=self.font, bg="khaki")
        self.max_wave_entry.place(x=910, y=130, anchor=tk.W)

        self.bar_label = tk.Label(self.input_frame, text="-", font=self.font, bg=ini.c2)
        self.bar_label.place(x=890, y=130, anchor=tk.W)

        # Wavelength Range: B1 - B7
        self.wave_b1_radio = tk.Radiobutton(self.input_frame, text="B1", variable=self.wave_mode,
                                            value="B1", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_b1_radio.place(x=520, y=150, anchor=tk.W)

        self.wave_b2_radio = tk.Radiobutton(self.input_frame, text="B2", variable=self.wave_mode,
                                            value="B2", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_b2_radio.place(x=520, y=170, anchor=tk.W)

        self.wave_b3_radio = tk.Radiobutton(self.input_frame, text="B3", variable=self.wave_mode,
                                            value="B3", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_b3_radio.place(x=520, y=190, anchor=tk.W)

        self.wave_b4_radio = tk.Radiobutton(self.input_frame, text="B4", variable=self.wave_mode,
                                            value="B4", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_b4_radio.place(x=520, y=210, anchor=tk.W)

        self.wave_b5_radio = tk.Radiobutton(self.input_frame, text="B5", variable=self.wave_mode,
                                            value="B5", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_b5_radio.place(x=520, y=230, anchor=tk.W)

        self.wave_b6_radio = tk.Radiobutton(self.input_frame, text="B6", variable=self.wave_mode,
                                            value="B6", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_b6_radio.place(x=520, y=250, anchor=tk.W)

        self.wave_b7_radio = tk.Radiobutton(self.input_frame, text="B7", variable=self.wave_mode,
                                            value="B7", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_b7_radio.place(x=520, y=270, anchor=tk.W)

        # Wavelength Range: G1 - G12
        self.wave_g1_radio = tk.Radiobutton(self.input_frame, text="G1", variable=self.wave_mode,
                                            value="G1", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g1_radio.place(x=590, y=150, anchor=tk.W)

        self.wave_g2_radio = tk.Radiobutton(self.input_frame, text="G2", variable=self.wave_mode,
                                            value="G2", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g2_radio.place(x=590, y=170, anchor=tk.W)

        self.wave_g3_radio = tk.Radiobutton(self.input_frame, text="G3", variable=self.wave_mode,
                                            value="G3", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g3_radio.place(x=590, y=190, anchor=tk.W)

        self.wave_g4_radio = tk.Radiobutton(self.input_frame, text="G4", variable=self.wave_mode,
                                            value="G4", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g4_radio.place(x=590, y=210, anchor=tk.W)

        self.wave_g5_radio = tk.Radiobutton(self.input_frame, text="G5", variable=self.wave_mode,
                                            value="G5", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g5_radio.place(x=590, y=230, anchor=tk.W)

        self.wave_g6_radio = tk.Radiobutton(self.input_frame, text="G6", variable=self.wave_mode,
                                            value="G6", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g6_radio.place(x=590, y=250, anchor=tk.W)

        self.wave_g7_radio = tk.Radiobutton(self.input_frame, text="G7", variable=self.wave_mode,
                                            value="G7", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g7_radio.place(x=590, y=270, anchor=tk.W)

        self.wave_g8_radio = tk.Radiobutton(self.input_frame, text="G8", variable=self.wave_mode,
                                            value="G8", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g8_radio.place(x=590, y=290, anchor=tk.W)

        self.wave_g9_radio = tk.Radiobutton(self.input_frame, text="G9", variable=self.wave_mode,
                                            value="G9", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g9_radio.place(x=590, y=310, anchor=tk.W)

        self.wave_g10_radio = tk.Radiobutton(self.input_frame, text="G10", variable=self.wave_mode,
                                             value="G10", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g10_radio.place(x=590, y=330, anchor=tk.W)

        self.wave_g11_radio = tk.Radiobutton(self.input_frame, text="G11", variable=self.wave_mode,
                                             value="G110", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g11_radio.place(x=590, y=350, anchor=tk.W)

        self.wave_g12_radio = tk.Radiobutton(self.input_frame, text="G12", variable=self.wave_mode,
                                             value="G12", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_g12_radio.place(x=590, y=370, anchor=tk.W)

        # Wavelength Range: R1 - R9
        self.wave_r1_radio = tk.Radiobutton(self.input_frame, text="R1", variable=self.wave_mode,
                                            value="R1", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r1_radio.place(x=660, y=150, anchor=tk.W)

        self.wave_r2_radio = tk.Radiobutton(self.input_frame, text="R2", variable=self.wave_mode,
                                            value="R2", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r2_radio.place(x=660, y=170, anchor=tk.W)

        self.wave_r3_radio = tk.Radiobutton(self.input_frame, text="R3", variable=self.wave_mode,
                                            value="R3", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r3_radio.place(x=660, y=190, anchor=tk.W)

        self.wave_r4_radio = tk.Radiobutton(self.input_frame, text="R4", variable=self.wave_mode,
                                            value="R4", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r4_radio.place(x=660, y=210, anchor=tk.W)

        self.wave_r5_radio = tk.Radiobutton(self.input_frame, text="R5", variable=self.wave_mode,
                                            value="R5", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r5_radio.place(x=660, y=230, anchor=tk.W)

        self.wave_r6_radio = tk.Radiobutton(self.input_frame, text="R6", variable=self.wave_mode,
                                            value="R6", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r6_radio.place(x=660, y=250, anchor=tk.W)

        self.wave_r7_radio = tk.Radiobutton(self.input_frame, text="R7", variable=self.wave_mode,
                                            value="R7", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r7_radio.place(x=660, y=270, anchor=tk.W)

        self.wave_r8_radio = tk.Radiobutton(self.input_frame, text="R8", variable=self.wave_mode,
                                            value="R8", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r8_radio.place(x=660, y=290, anchor=tk.W)

        self.wave_r9_radio = tk.Radiobutton(self.input_frame, text="R9", variable=self.wave_mode,
                                            value="R9", command=self.ui_wave_enable, font=self.font, bg=ini.c2)
        self.wave_r9_radio.place(x=660, y=310, anchor=tk.W)

        # Run & Save
        self.execute_window = tk.PanedWindow(self.master, orient="vertical")
        self.execute_frame = tk.LabelFrame(self.execute_window, bg=ini.c0, bd=0)
        self.execute_window.add(self.execute_frame)
        self.execute_window.place(x=0, y=735, width=1000, height=65)

        self.run_button = tk.Button(self.execute_frame, text="RUN ONLY", width=15, command=self.run,
                                    font=self.font, bg=ini.c3)
        self.run_button.place(relx=0.35, rely=0.5, anchor=tk.CENTER)

        self.run_button = tk.Button(self.execute_frame, text="RUN & SAVE", width=15, command=self.run_save,
                                    font=self.font, bg=ini.c3)
        self.run_button.place(relx=0.65, rely=0.5, anchor=tk.CENTER)

        # Global variables
        self.mag = 0
        self.sky = 0
        self.min_wave = 0
        self.max_wave = 0

        # GUI Initialization
        self.ui_enable()
        self.ui_wave_enable()

        print('...... Reading order index for high resolution mode.')

        self.index = []
        self.order = []
        self.min_order_wave = []
        self.max_order_wave = []

        f = open("Index_Order_HR.dat", 'r')
        lines = f.readlines()

        for i in lines:
            i = i.strip()
            self.index.append(i.split('\t')[0])
            self.order.append(i.split('\t')[1])
            self.min_order_wave.append(i.split('\t')[2])
            self.max_order_wave.append(i.split('\t')[3])

        f.close()

        self.func = functions.Functions()

        print('...... Done!')

    def ui_exp_time(self, status):  # add 210408 hojae
        self.exp_time_entry.config(state=status)

    def ui_exp_num(self, status):  # add 210408 hojae
        self.exp_num_entry.config(state=status)

    def ui_target_sn(self, status):  # add 210408 hojae
        self.target_sn_entry.config(state=status)

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
            if self.resolution.get() == "HR":
                self.wave_nir_radio.config(state='disable')
            else:
                self.wave_nir_radio.config(state=status)

            if self.wave_mode.get() != "Input Wave":
                self.min_wave_entry.config(state='disable')
                self.max_wave_entry.config(state='disable')

    def ui_wave_add(self, status):  # add 20210617 by T-G. Ji
        self.wave_b1_radio.config(state=status)
        self.wave_b2_radio.config(state=status)
        self.wave_b3_radio.config(state=status)
        self.wave_b4_radio.config(state=status)
        self.wave_b5_radio.config(state=status)
        self.wave_b6_radio.config(state=status)
        self.wave_b7_radio.config(state=status)

        self.wave_g1_radio.config(state=status)
        self.wave_g2_radio.config(state=status)
        self.wave_g3_radio.config(state=status)
        self.wave_g4_radio.config(state=status)
        self.wave_g5_radio.config(state=status)
        self.wave_g6_radio.config(state=status)
        self.wave_g7_radio.config(state=status)
        self.wave_g8_radio.config(state=status)
        self.wave_g9_radio.config(state=status)
        self.wave_g10_radio.config(state=status)
        self.wave_g11_radio.config(state=status)
        self.wave_g12_radio.config(state=status)

        self.wave_r1_radio.config(state=status)
        self.wave_r2_radio.config(state=status)
        self.wave_r3_radio.config(state=status)
        self.wave_r4_radio.config(state=status)
        self.wave_r5_radio.config(state=status)
        self.wave_r6_radio.config(state=status)
        self.wave_r7_radio.config(state=status)
        self.wave_r8_radio.config(state=status)
        self.wave_r9_radio.config(state=status)

    def ui_enable(self):  # add 20210324 by T-G. Ji

        if self.mode.get() == "S/N Calculation":
            self.ui_exp_time('normal')
            self.ui_exp_num('normal')
            self.ui_target_sn('disable')
            self.ui_mag_range('disable')
            self.ui_wave_range('disable')  # add 210408 hojae
            self.ui_wave_add('disable')
            self.ui_target_magnitude('normal')
            self.ui_sky_brightness('normal')

        elif self.mode.get() == "ExpTime Calculation":  # add 210408 hojae
            self.ui_exp_time('disable')
            self.exp_num_entry.delete(0, len(self.exp_num_entry.get()))
            self.exp_num_entry.insert(-1, "1")
            self.ui_exp_num('disable')
            self.ui_target_sn('normal')
            self.ui_mag_range('disable')
            self.ui_wave_range('disable')
            self.ui_wave_add('disable')
            self.ui_target_magnitude('normal')
            self.ui_sky_brightness('normal')

        elif self.mode.get() == "S/N vs. Magnitude":
            self.ui_exp_time('normal')
            self.ui_exp_num('normal')
            self.ui_target_sn('disable')
            self.ui_target_magnitude('disable')
            self.ui_wave_range('disable')
            self.ui_wave_add('disable')
            self.ui_mag_range('normal')
            self.ui_sky_brightness('normal')

        elif self.mode.get() == "S/N vs. Wavelength":
            self.ui_exp_time('normal')
            self.ui_exp_num('normal')
            self.ui_target_sn('disable')
            self.ui_target_magnitude('normal')
            self.ui_sky_brightness('disable')
            self.ui_wave_range('normal')
            self.ui_mag_range('disable')
            self.set_wave_entry.config(state='disable')

            if self.resolution.get() == "HR":
                self.ui_wave_add('normal')
            else:
                self.ui_wave_add('disable')

    def ui_wave_enable(self):  # add 20210324 by T-G. Ji
        if self.wave_mode.get() == "Input Wave":
            self.min_wave_entry.config(state='normal')
            self.max_wave_entry.config(state='normal')

        else:
            self.min_wave_entry.config(state='disable')
            self.max_wave_entry.config(state='disable')

    # change 20210324 by T-G. Ji
    def run(self):
        res_mode = self.resolution.get()
        wave_mode = self.wave_mode.get()
        cal_mode = self.mode.get()
        set_wave = float(self.set_wave_entry.get())
        pwv = float(self.pwv_entry.get())
        exp_t = float(self.exp_time_entry.get())
        exp_n = float(self.exp_num_entry.get())
        target_sn = float(self.target_sn_entry.get())
        min_mag = float(self.min_mag_entry.get())
        max_mag = float(self.max_mag_entry.get())

        mag_arr = [float(self.mag_blue_entry.get()), float(self.mag_green_entry.get()),
                   float(self.mag_red_entry.get()), float(self.mag_nir_entry.get()),
                   float(self.mag_wave_entry.get()), float(self.mag_wave_entry.get())]

        sky_arr = [float(self.sky_blue_entry.get()), float(self.sky_green_entry.get()),
                   float(self.sky_red_entry.get()), float(self.sky_nir_entry.get()),
                   float(self.sky_wave_entry.get()), float(self.sky_wave_entry.get())]

        if cal_mode == "S/N Calculation":
            self.func.cal_signal_to_noise(res_mode, pwv, exp_t, exp_n, mag_arr, sky_arr, set_wave, True)

        elif cal_mode == "ExpTime Calculation":
            self.func.cal_exp_time(res_mode, pwv, target_sn, mag_arr, sky_arr, set_wave)

        elif cal_mode == "S/N vs. Magnitude":
            self.func.plot_sn_mag(res_mode, pwv, exp_t, exp_n, min_mag, max_mag, sky_arr)

        elif cal_mode == "S/N vs. Wavelength":
            if res_mode == "LR":
                if wave_mode == "Blue":
                    self.mag = float(self.mag_blue_entry.get())
                    self.sky = float(self.sky_blue_entry.get())
                    self.min_wave = WAVE_BAND_LR[0][0]
                    self.max_wave = WAVE_BAND_LR[0][1]

                elif wave_mode == "Green":
                    self.mag = float(self.mag_green_entry.get())
                    self.sky = float(self.sky_green_entry.get())
                    self.min_wave = WAVE_BAND_LR[1][0]
                    self.max_wave = WAVE_BAND_LR[1][1]

                elif wave_mode == "Red":
                    self.mag = float(self.mag_red_entry.get())
                    self.sky = float(self.sky_red_entry.get())
                    self.min_wave = WAVE_BAND_LR[2][0]
                    self.max_wave = WAVE_BAND_LR[2][1]

                elif wave_mode == "NIR":
                    self.mag = float(self.mag_nir_entry.get())
                    self.sky = float(self.sky_nir_entry.get())
                    self.min_wave = WAVE_BAND_LR[3][0]
                    self.max_wave = WAVE_BAND_LR[3][1]

                else:
                    self.mag = float(self.mag_wave_entry.get())
                    self.sky = float(self.sky_wave_entry.get())
                    self.min_wave = float(self.min_wave_entry.get())
                    self.max_wave = float(self.max_wave_entry.get())

                self.func.plot_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, self.mag, self.sky,
                                       self.min_wave, self.max_wave)

            elif res_mode == "MR":
                if wave_mode == "Blue":
                    self.mag = float(self.mag_blue_entry.get())
                    self.sky = float(self.sky_blue_entry.get())
                    self.min_wave = WAVE_BAND_MR[0][0]
                    self.max_wave = WAVE_BAND_MR[0][1]

                elif wave_mode == "Green":
                    self.mag = float(self.mag_green_entry.get())
                    self.sky = float(self.sky_green_entry.get())
                    self.min_wave = WAVE_BAND_MR[1][0]
                    self.max_wave = WAVE_BAND_MR[1][1]

                elif wave_mode == "Red":
                    self.mag = float(self.mag_red_entry.get())
                    self.sky = float(self.sky_red_entry.get())
                    self.min_wave = WAVE_BAND_MR[2][0]
                    self.max_wave = WAVE_BAND_MR[2][1]

                elif wave_mode == "NIR":
                    self.mag = float(self.mag_nir_entry.get())
                    self.sky = float(self.sky_nir_entry.get())
                    self.min_wave = WAVE_BAND_MR[3][0]
                    self.max_wave = WAVE_BAND_MR[3][1]

                else:
                    self.mag = float(self.mag_wave_entry.get())
                    self.sky = float(self.sky_wave_entry.get())
                    self.min_wave = float(self.min_wave_entry.get())
                    self.max_wave = float(self.max_wave_entry.get())

                self.func.plot_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, self.mag, self.sky,
                                       self.min_wave, self.max_wave)

            elif res_mode == "HR":
                if wave_mode == "Blue":
                    self.mag = float(self.mag_blue_entry.get())
                    self.sky = float(self.sky_blue_entry.get())
                    self.min_wave = WAVE_BAND_HR[0][0]
                    self.max_wave = WAVE_BAND_HR[0][1]

                elif wave_mode == "Green":
                    self.mag = float(self.mag_green_entry.get())
                    self.sky = float(self.sky_green_entry.get())
                    self.min_wave = WAVE_BAND_HR[1][0]
                    self.max_wave = WAVE_BAND_HR[1][1]

                elif wave_mode == "Red":
                    self.mag = float(self.mag_red_entry.get())
                    self.sky = float(self.sky_red_entry.get())
                    self.min_wave = WAVE_BAND_HR[2][0]
                    self.max_wave = WAVE_BAND_HR[2][1]

                elif wave_mode == "Input Wave":
                    self.mag = float(self.mag_wave_entry.get())
                    self.sky = float(self.sky_wave_entry.get())
                    self.min_wave = float(self.min_wave_entry.get())
                    self.max_wave = float(self.max_wave_entry.get())

                else:
                    self.mag = float(self.mag_wave_entry.get())
                    self.sky = float(self.sky_wave_entry.get())

                    self.min_wave = np.zeros(2)
                    self.max_wave = np.zeros(2)

                    order = 0
                    for i in range(len(self.index)):
                        if wave_mode == self.index[i]:
                            self.min_wave[0] = float(self.min_order_wave[i])
                            self.min_wave[1] = float(self.min_order_wave[i + 1])
                            self.max_wave[0] = float(self.max_order_wave[i])
                            self.max_wave[1] = float(self.max_order_wave[i + 1])
                            order = int(self.order[i])

                            break

                    self.func.plot_sn_wave_order(res_mode, wave_mode, order, pwv, exp_t, exp_n, self.mag, self.sky,
                                                 self.min_wave, self.max_wave)
                    return None

            self.func.plot_sn_wave(res_mode, wave_mode, pwv, exp_t, exp_n, self.mag, self.sky,
                                   self.min_wave, self.max_wave)

        else:
            return None

    def run_save(self):  # add 20210603 Hojae
        MainGUI.save = True
        self.run()
        MainGUI.save = False
