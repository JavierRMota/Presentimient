############ TAGS TO BE USED WITH EXTENSION "BETTER COMMENTS"
    # $ TÍTULO / DONE
    # & Subtítulo
    # ! Warning
    #  * Demo
    #  ? Duda/aclaración
    # % To do
    #  x Borrado
    ############

import sys
import os
import random
import ctypes
import pandas
import numpy
import requests
import json
import time
import threading
from datetime import datetime, timedelta
from PIL import Image
import glob
from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime, Qt, QTimer, QEventLoop, QDir
from PyQt5.QtWidgets import (QApplication, QComboBox,QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit,
        QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QSpinBox, QDesktopWidget, 
        QCheckBox, QFileDialog, QTabWidget, QSizePolicy)

#? README
    #? Intervalo entre 0 y 99 segundos
    #? Max no. de trials = 99
    #? To export, add the ".csv" extension
    #? For Neulog, you need to open Neulog API

#$ TODO:
    #! Sharing code
        #! Dynamic "path_REG_dll"
    #! Diseño  
        #! Agregar imagen de diseño experimental   
        #! Add Z0 a Phys Data, a lado de Trial e Instances
        #! Add info
        #! Add manual
        #! Adaptar exports
    #! Cerrar puertas de errores
        #! Don't close if RNG is not selected
        #! Don't close if error at exporting
        #! Don't close if statistical analysis can't be realized
        #! Don't close if no library is selected
        #! Alertar si no se ha elegido banco de imagenes
        #! no salir si no hay port en neulog
        #! Revisar otras "#!"
    #! Evitar que haya diferente sample rate entre neulogs (no se puede y rompe)
    #! Solucionar on-demand procedure; rompería el sample calculado para el neulog
    #! Compilar con https://pypi.org/project/auto-py-to-exe/

#! LOW PRIORITY:
    #! Falta agregar "Opened", "GetBits", "GetBytes" y "APIVersion" a la clase PsyREG
    #! Include FOR loop for each psyleron connected en "click_refresh_sources"
    #! agregar dimensiones de análisis (Ej. Miedo[Muerte-Peligro, Animales-Lesiones, etc.])

#$ WISHLIST:
    #! Separación entre hombres y mujeres
    #! Seleccionar estímulos visuales
        #$ Images (DONE)
        #! Light flashes
    #! Seleccionar estímulos auditivos
        #! Estruendos
        #! Silencio
        #! Ruido blanco
    #! Physiological sensors
        #! Neulog
        #! Emotiv
        #! Vernier Go-Direct
        #! BIOPAC

################################3

class Pseudo_RNG():
    def __init__(self):  
        self.name = "Pseudo-RNG"
    def get_bits(self, maxbts):
        str_list = []
        for x in range(maxbts):
            str_list.append(random.randrange(0,2))
        str_bits = ''.join(str(x) for x in str_list)
        # print(str_bits)
        return str_bits

class PsyREG():
    def __init__(self):  
        #? Define path of DLL
        self.path_REG_dll = os.path.join(os.getcwd(), '.\Presentimiento\PsyREG.dll') # DLL file path
        # self.path_REG_dll = r'C:\Users\ramse\Python_ENVS\Presentimiento\PsyREG.dll' # DLL file path
        self.REG_dll = ctypes.CDLL(self.path_REG_dll) # load DLL
        #? Define variables
        PSYREG_API_VERSION = 1 # Version of the API that this header is indended for. Should be compared to PsyREGAPIVersion() */
        INVALID_DATASOURCE = -1 # Constant representing an invalid Datasource */
        BSS_GOOD = 0x0000 # no flags set. the device is ok and there are no problems */
        BSS_CONNECTING = 0x0001 # device connection is being established (in the process of opening) */
        BSS_WAITING = 0x0002 # waiting for device data (buffer empty) */
        BSS_BUSY = 0x0004 # device is in use by another application */
        BSS_NODEVICE = 0x0008 # there is no device by this name connected anymore */
        BSS_READERROR = 0x0010 # was there a read error during the last read */
        BSS_BADCFG = 0x0020 # was there a bad configuration for the device (e.g. conflicting values or unset values) */
        BSS_CANTPROCESS = 0x0040 # was there a processing error? [set at bitsource level] */
        BSS_INITERROR = 0x0080 # was there an initialization error / problem with the data structure [set at bitsource level] */
        BSS_TIMEOUT = 0x0100 # did the reader time out since the last device read [set at bitsource level] */
        BSS_GENERALERROR = 0x8000 # was there any error at all. set if any other error (busy, nodevice, readerror, cantprocess) [set at bitsource level] */
        BSS_INVALID = 0x0200 # is the DataSource invalid. This occurs when a DataSource was not created or has already been destroyed. */

    def get_name(self):
        #? Obtain the Type and ID of the Psyleron, and return in a formatted string
        self.invoke_RNG()
        source = self.get_source() 
        # Define all the types of results and arguments in the PsyREG dll functions
        self.REG_dll.PsyREGGetDeviceTypeBSTR.restype = ctypes.c_char_p
        self.REG_dll.PsyREGGetDeviceTypeBSTR.argtypes = [ctypes.c_int32]
        self.REG_dll.PsyREGGetDeviceIdBSTR.restype = ctypes.c_char_p
        self.REG_dll.PsyREGGetDeviceIdBSTR.argtypes = [ctypes.c_int32]
        PsyREG_ID = self.REG_dll.PsyREGGetDeviceIdBSTR(source)
        PsyREG_ID = PsyREG_ID.decode("utf-8") #Decode from byte to string
        PsyREG_Type = self.REG_dll.PsyREGGetDeviceTypeBSTR(source)
        PsyREG_Type = PsyREG_Type.decode("utf-8") #Decode from byte to string
        name_PsyREG = ("Psyleron %s: %s" % (PsyREG_Type, PsyREG_ID)) # Format string of the name
        # print(name_PsyREG)
        return name_PsyREG

    def get_bits(self, maxbts):
        #? Obtain 1 bit of random data; 1 or 0
        self.invoke_RNG() 
        source = self.get_source() 
        self.open_RNG()
        # Define all the types of results and arguments in the PsyREG dll functions
        self.REG_dll.PsyREGGetBit.restype = ctypes.c_int32
        self.REG_dll.PsyREGGetBit.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_ubyte)]
        # For loop for x number of MAXBTS stated
        str_list = []
        for bit_psyreg in range(maxbts):
            bit_psyreg = ctypes.c_ubyte()
            self.REG_dll.PsyREGGetBit(source, ctypes.byref(bit_psyreg))
            str_list.append(bit_psyreg.value)
        str_bits = ''.join(str(x) for x in str_list)
        # print(str_bits)
        return str_bits
        
    def get_bytes(self, maxbts):
        #? Obtain 1 byte (between 0 and 255) of random data
        self.invoke_RNG() 
        source = self.get_source() 
        self.open_RNG()
        # Define all the types of results and arguments in the PsyREG dll functions
        self.REG_dll.PsyREGGetByte.restype = ctypes.c_int32
        self.REG_dll.PsyREGGetByte.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_ubyte)]
        # For loop for x number of MAXBTS stated
        str_list = []
        for byte_psyreg in range(maxbts):
            byte_psyreg = ctypes.c_ubyte()
            self.REG_dll.PsyREGGetByte(source, ctypes.byref(byte_psyreg))
            str_list.append(byte_psyreg.value)
        str_bytes = ''.join(str(x) for x in str_list)
        # print(str_bytes)
        return str_bytes

    # def get_bits(self,max_bits):         ######! NOT WORKING YET
        # #? Obtain chunks of bits
        # self.invoke_RNG() 
        # source = self.get_source() 
        # self.open_RNG()
        # # Define all the types of results and arguments in the PsyREG dll functions
        # REG_dll.PsyREGGetBits.restype = ctypes.c_int32
        # REG_dll.PsyREGGetBits.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32,ctypes.c_int32]
        # bits_psyreg = ctypes.c_ubyte()
        # REG_dll.PsyREGGetBits(source, ctypes.byref(bits_psyreg), max_bits)
        # return bits_psyreg.value

    def invoke_RNG(self):
        #? Call Psyleron; if it's not called it won't know you're talking to him
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGEnumerateSources.restype = ctypes.c_int32
        self.REG_dll.PsyREGEnumerateSources.argtypes = []
        PsyREG_EnumerateSources = self.REG_dll.PsyREGEnumerateSources()
        return PsyREG_EnumerateSources
    
    def get_source(self):
        #? Get source from psyleron; if it's not stated, it won't get data, even if it's called
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGGetSource.restype = ctypes.c_int32
        self.REG_dll.PsyREGGetSource.argtypes = [ctypes.c_uint32]
        PsyREG_GetSource = self.REG_dll.PsyREGGetSource(0)
        return PsyREG_GetSource

    def open_RNG(self):
        #? Open the stream of data to obtain bits and bytes
        source = self.get_source() 
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGOpen.restype = ctypes.c_int32
        self.REG_dll.PsyREGOpen.argtypes = [ctypes.c_int32]
        PsyREG_Open = self.REG_dll.PsyREGOpen(source)
        return PsyREG_Open

    def close_RNG(self):
        #? Closes an open DataSource and prevents further interaction
        source = self.get_source() 
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGClose.restype = ctypes.c_void_p
        self.REG_dll.PsyREGClose.argtypes = [ctypes.c_int32]
        PsyREG_Close = self.REG_dll.PsyREGClose(source)
        return PsyREG_Close

    def release_RNG(self):
        #? Releases a given source back to the source manager
        source = self.get_source() 
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGReleaseSource.restype = ctypes.c_void_p
        self.REG_dll.PsyREGReleaseSource.argtypes = [ctypes.c_int32]
        PsyREG_Release = self.REG_dll.PsyREGReleaseSource(source)
        return PsyREG_Release

    def clear_RNG(self):
        #? Clears the entire list of sources built by one or more calls to EnumerateSources (invoke_RNG)
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGClearSources.restype = ctypes.c_void_p
        self.REG_dll.PsyREGClearSources.argtypes = []
        PsyREG_Clear = self.REG_dll.PsyREGClearSources()
        return PsyREG_Clear

    def reset_RNG(self):
        #? Signals that the data in the DataSource internal buffer is stale and performs a clear.
        source = self.get_source() 
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGReset.restype = ctypes.c_void_p
        self.REG_dll.PsyREGReset.argtypes = [ctypes.c_int32]
        PsyREG_Reset = self.REG_dll.PsyREGReset(source)
        return PsyREG_Reset

    def get_status(self):
        #? Obtain 0 if status is good, 512 if status is bad
        self.invoke_RNG() 
        source = self.get_source() 
        # Define all the types of results and arguments in the PsyREG dll functions
        self.REG_dll.PsyREGGetStatus.restype = ctypes.c_int32
        self.REG_dll.PsyREGGetStatus.argtypes = [ctypes.c_int32]
        # Pass functions from PsyREG dll
        PsyREG_Status = self.REG_dll.PsyREGGetStatus(source)
        return PsyREG_Status

    def count_PsyREGs(self):
        #? Count number of Psylerons connected
        self.invoke_RNG() 
        # Define all the types of results and arguments in the PsyREG dll function
        self.REG_dll.PsyREGGetSourceCount.restype = ctypes.c_uint32
        self.REG_dll.PsyREGGetSourceCount.argtypes = []
        PsyREG_GetSourceCount = self.REG_dll.PsyREGGetSourceCount(0)
        return PsyREG_GetSourceCount

class Neulog():
    #! Not implemented: "ResetSensor:[],[]", "SetPositiveDirection:[],[],[]" & "# SetRFID:[]"
    #! Can't support more than 20 samples per second for more than 5 minutes
    def __init__(self,host,*additional_sensors):  
        self.name = "Neulog"
        self.host = str(host)
        self.sensor_id = '1'
        self.set_sensors_id()
        self.parameters = ':'
        # Check if there's more than 1 sensor given as argument
        for sensors in additional_sensors:
            self.parameters += '[' + sensors + '],[' + self.sensor_id + '],'
        self.parameters = self.parameters[:-1]

    def get_url(self,command):
        # Construct url query
        url = 'http://localhost:'+self.host+'/NeuLogAPI?'+command
        return url

    def get_data_dict(self,url):
        # Obtain data_dict from url request from the url request
        data_dict = requests.get(url)
        # Convert to json object, so it can be used as dictionary
        json_data_dict = json.loads(data_dict.text)
        return json_data_dict

    def set_sensors_id(self):
        # Set the ID of the connected sensors
        command = 'SetSensorsID'
        parameters = ':['+  self.sensor_id +']'
        url = self.get_url(command+parameters)        
        data_dict = self.get_data_dict(url)
        return 'All sensors changed the ID to: ' + data_dict[command]

    def set_sensor_range(self, sensor_range):
        # Change the range of the sensor (GSR: 1 = Arb, 2 = mS; Pulse: 1 = BPM, 2 = Wave[Arb])
        command = 'SetSensorRange'
        parameters = self.parameters
        sensor_range = ',['+ sensor_range +']'
        url = self.get_url(command+parameters+sensor_range)
        data_dict = self.get_data_dict(url)
        return 'Sensor range changed: ' + data_dict[command]

    def get_version(self):
        # Obtain the version of the Neulog API
        command = 'GetServerVersion'
        url = self.get_url(command)
        data_dict = self.get_data_dict(url)
        return 'Neulog API version: ' + data_dict[command]
    
    def get_status(self):
        # Get the status of the server (it's wrongly written as 'sever' in the API)
        command = 'GetSeverStatus'
        url = self.get_url(command)
        data_dict = self.get_data_dict(url)
        return 'Neulog API status: ' + data_dict[command]

    def get_values(self):
        # Obtain values from the sensors
        command = 'GetSensorValue'
        parameters = self.parameters
        url = self.get_url(command+parameters)
        data_dict = self.get_data_dict(url)
        # Obtains the values from the data_dict
        data_list = data_dict[command]
        return data_list
        # print(data_dict[command])

    def exp_start(self,sample_rate,sample_size):
        # Start the experiment with the defined parameters; an experiment needs to be stopped before starting a new one
        command = 'StartExperiment'
        parameters = self.parameters + ',[' + sample_rate + '],[' + sample_size + ']'
        url = self.get_url(command+parameters)
        data_dict = self.get_data_dict(url)
        return 'Start Neulog experiment: ' + data_dict[command] + ' at ' + datetime.now().strftime('%H:%M:%S.%f')[:-3]

    def exp_stop(self):
        # Stops the experiment; an experiment needs to be stopped before starting a new one
        command = 'StopExperiment'
        url = self.get_url(command)
        data_dict = self.get_data_dict(url)
        return 'Stopped Neulog experiment: ' + data_dict[command] + ' at ' + datetime.now().strftime('%H:%M:%S.%f')[:-3]

    def get_exp_values(self):
        # Obtain values of the current or last ran experiment
        command = 'GetExperimentSamples'
        parameters = self.parameters
        url = self.get_url(command+parameters)
        data_dict = self.get_data_dict(url)
        num = 0
        # for each list of data within the dictionary, delete the first 2 elements (sensor_type and sensor_id)
        for lists in data_dict[command]:
            del data_dict[command][num][:2]
            num += 1
        # return list of lists of each sensor_type with only the values recorded
        return data_dict[command]

class Create_Window(QDialog):
    #& INIT
        def __init__(self):
            super().__init__()
            self.title = "Physiological Anticipatory Activity (PAA) 2.0"
            self.path_logo_UPIDE = os.path.join(os.getcwd(), '.\Presentimiento\Logo_UPIDE.png') # Logo UPIDE path
            self.setWindowIcon(QtGui.QIcon(self.path_logo_UPIDE))
            self.setWindowTitle(self.title)
            self.setFixedSize(1600, 800)
            # call functions:
            self.create_settings_layout()
            self.create_data_layout()
            self.create_phys_layout()
            self.create_stats_layout()
            self.create_buttons()
            # Create list of stimuli:
            self.image_list_neutral = []
            self.image_list_neutral_filenames = []
            self.image_list_excitatory = []
            self.image_list_excitatory_filenames = []
            self.image_list = []
            self.image_list_filenames = []
            # Create the layout in grid fromat for the groups (topleft,topright,etc.)
            Tab_Widget = QTabWidget()
            main_layout = QVBoxLayout()
            Tab_Widget.addTab(self.gb_settings, "Settings")
            Tab_Widget.addTab(self.gb_session_data, "Session Data")
            Tab_Widget.addTab(self.gb_phys_data, "Physiological Data")
            Tab_Widget.addTab(self.gb_stats_data, "Statistical Analysis")
            main_layout.addWidget(Tab_Widget)
            main_layout.addLayout(self.layout_buttons,2)
            self.setLayout(main_layout)

    #& LAYOUT
        def create_settings_layout(self):
        #& GROUP BOXES
            #& MAIN
            self.gb_settings = QGroupBox("Session settings:")
            #& 1. SOURCES & STIMULI
            #& 1.1. SOURCES & TESTING
            self.gb_sources_n_test = QGroupBox("RNG sources:")
            #& 1.2. STIMULI
            self.gb_stimuli = QGroupBox("Select stimuli:")
            #& 1.3. PHYSIOLOGICAL
            self.gb_physiological = QGroupBox("Select physiological data:")
            #& 2. EXP DESIGN
            self.gb_exp_design = QGroupBox("Experimental design:")
            #& 2.1 TRIALS & SESSION
            #& 2.1.1. SESSION ID
            self.gb_session_id = QGroupBox("Session ID:")
            #& 2.1.2. TRIAL TYPE
            self.gb_trial_type = QGroupBox("Type of trials:")
            #& 2.1.3. TRIALS NUM
            self.gb_num_trials = QGroupBox("Number of trials:")
            #& 2.2. TRIALS DURATION
            self.gb_trial_duration = QGroupBox("Duration of each part of a trial (seconds):")
            #& 2.2.1. TRIALS DURATION ELEMENTS
            self.gb_pre_screen = QGroupBox("Pre-stimulus screen duration:")
            self.gb_stimulus_duration = QGroupBox("Stimulus duration:")
            self.gb_post_screen = QGroupBox("Post-stimulus screen duration:")
            #& 2.3. DELAYS
            self.gb_delays = QGroupBox("Delays with white screen between trials (seconds):")
            #& 2.3.1. FIRST SCREEN
            self.gb_first_screen = QGroupBox("Only-once before first trial:")
            #& 2.3.2. DELAY BEFORE TRIAL
            self.gb_before_interval = QGroupBox("Interval before each trial:")
            #& 2.3.3. DELAY AFTER TRIAL
            self.gb_after_interval = QGroupBox("Interval after each trial:")
        #& SPIN BOXES
            #& 2.1.1. SESSION ID
            self.sb_session_id = QSpinBox()
            self.sb_session_id.setValue(1)
            #& 2.1.3. TRIALS NUM
            self.sb_num_trials = QSpinBox()
            self.sb_num_trials.setValue(3) #$ 45
            #& 2.2.1. TRIALS DURATION ELEMENTS
            self.sb_pre_screen = QSpinBox()
            self.sb_pre_screen.setValue(1) #$ 3
            self.sb_stim_duration = QSpinBox()
            self.sb_stim_duration.setValue(1) #$ 3
            self.sb_post_screen = QSpinBox()
            self.sb_post_screen.setValue(1) #$ 9
            #& 2.3.1. FIRST SCREEN
            self.sb_first_screen = QSpinBox()
            self.sb_first_screen.setValue(1) #$ 10
            #& 2.3.3. DELAY BEFORE TRIAL
            self.sb_before_min_interval = QSpinBox()
            self.sb_before_min_interval.setValue(0) #$ 0
            self.sb_before_max_interval = QSpinBox()
            self.sb_before_max_interval.setValue(0) #$ 0
            self.sb_before_min_interval.setEnabled(False)
            self.sb_before_max_interval.setEnabled(False)
            #& 2.3.3. DELAY AFTER TRIAL
            self.sb_after_min_interval = QSpinBox()
            self.sb_after_min_interval.setValue(0) #$ 0
            self.sb_after_max_interval = QSpinBox()
            self.sb_after_max_interval.setValue(1) #$ 5
        #& COMBO BOXES
            #& 1.1. SOURCES
            self.combo_rng_sources = QComboBox()
            self.combo_rng_sources.addItem("-")
            #& 1.3. PHYSIOLOGICAL
            self.combo_skin_conductance = QComboBox()
            self.combo_skin_conductance.addItem("-")
            self.combo_skin_conductance.setDisabled(True)
            self.combo_heart_rate = QComboBox()
            self.combo_heart_rate.addItem("-")
            self.combo_heart_rate.setDisabled(True)
            self.combo_brainwaves = QComboBox()
            self.combo_brainwaves.addItem("-")
            self.combo_brainwaves.setDisabled(True)
            self.combo_skin_conductance_sample = QComboBox()
            self.combo_heart_rate_sample = QComboBox()
            self.combo_brainwaves_sample = QComboBox()
            self.combo_skin_conductance_sample.addItems(["20 per second","10 per second","5 per second","2 per second","1 per second"])
            self.combo_heart_rate_sample.addItems(["20 per second","10 per second","5 per second","2 per second","1 per second"])
            self.combo_brainwaves_sample.addItems(["20 per second","10 per second","5 per second","2 per second","1 per second"])
            self.combo_skin_conductance_sample.setDisabled(True)
            self.combo_heart_rate_sample.setDisabled(True)
            self.combo_brainwaves_sample.setDisabled(True)
            #& 2.1.2. TRIAL TYPE
            self.combo_trial_type = QComboBox()
            self.combo_trial_type.addItem("Free-Running")
            self.combo_trial_type.addItem("On-Demand")
            self.combo_trial_type.currentIndexChanged.connect(self.click_trial_type)
        #& TEXT BOXES
            #& 1.1. TESTING & TESTING
            self.tb_gen_bits = QLineEdit("") #? Add color to background: gen_bits.setStyleSheet("QLineEdit { background-color: rgb(220,220,220) }")
            #& 1.3. PHYSIOLOGICAL
            self.tb_neulog_port = QLineEdit("22002") #$ Localhost Port (ej. '22002')
            self.tb_skin_conductance_test = QLineEdit("Test")
            self.tb_heart_rate_test = QLineEdit("Test")
            self.tb_brainwaves_test = QLineEdit("Test")
            self.tb_skin_conductance_test.setDisabled(True)
            self.tb_heart_rate_test.setDisabled(True)
            self.tb_brainwaves_test.setDisabled(True)
        #& BUTTONS
            #& 1.1. SOURCES & TESTING
            butt_refresh_sources = QPushButton('Refresh RNG sources')
            butt_refresh_sources.clicked.connect(self.click_refresh_sources)
            butt_generate_bits = QPushButton('Test: Generate bits')
            butt_generate_bits.clicked.connect(self.click_generate_bits)
            #& 1.2. STIMULI
            butt_neutral_stimuli = QPushButton("Select neutral stimuli library")
            butt_neutral_stimuli.clicked.connect(self.click_neutral_stimuli)
            butt_excitatory_stimuli = QPushButton('Select excitatory stimuli library')
            butt_excitatory_stimuli.clicked.connect(self.click_excitatory_stimuli)
            #& 1.3. PHYSIOLOGICAL
            butt_refresh_neulog = QPushButton('Refresh Neulog sources')
            butt_refresh_neulog.clicked.connect(self.click_refresh_neulog)
            butt_refresh_physiological = QPushButton('Refresh physiological sources')
            butt_refresh_physiological.clicked.connect(self.click_refresh_physiological)
            self.butt_skin_conductance_test = QPushButton('Test: Get values')
            self.butt_skin_conductance_test.clicked.connect(self.click_skin_conductance_test)
            self.butt_skin_conductance_test.setDisabled(True)
            self.butt_heart_rate_test = QPushButton('Test: Get values')
            self.butt_heart_rate_test.clicked.connect(self.click_heart_rate_test)
            self.butt_heart_rate_test.setDisabled(True)
            self.butt_brainwaves_test = QPushButton('Test: Get values')
            self.butt_brainwaves_test.clicked.connect(self.click_brainwaves_test)
            self.butt_brainwaves_test.setDisabled(True)
        #& CHECK BOXES
            #& 1.3. PHYSIOLOGICAL
            self.cb_skin_conductance = QCheckBox("Skin Conductance")
            self.cb_skin_conductance.toggled.connect(self.check_skin_conductance)
            self.cb_heart_rate = QCheckBox("Heart Rate")
            self.cb_heart_rate.toggled.connect(self.check_heart_rate)
            self.cb_brainwaves = QCheckBox("Brain Waves")
            self.cb_brainwaves.toggled.connect(self.check_brainwaves)
        #& SET LAYOUTS
            # declare layouts
            layout_main = QHBoxLayout() #MAIN
            layout_source_n_stimuli = QVBoxLayout() # 1. SOURCES & STIMULI
            layout_sources_n_test = QGridLayout() # 1.1. SOURCES & TESTING
            layout_stimuli = QHBoxLayout() # 1.2. STIMULI
            layout_physiological = QGridLayout() # 1.3. PHYSIOLOGICAL
            layout_exp_design = QHBoxLayout() # 2. EXP DESIGN
            layout_trial_and_screen = QVBoxLayout() # 2.1. TRIALS
            layout_session_id = QVBoxLayout() # 2.1.1. SESSION ID
            layout_trial_type = QVBoxLayout() # 2.1.2. TRIAL TYPE
            layout_trial = QVBoxLayout() # 2.1.3. TRIALS NUM
            layout_duration = QGridLayout() # 2.2. TRIALS DURATION 
            layout_dur_pre = QVBoxLayout() # 2.2.1. TRIALS DURATION ELEMENTS
            layout_dur_stimulus = QVBoxLayout() # 2.2.1. TRIALS DURATION ELEMENTS
            layout_dur_post = QVBoxLayout() # 2.2.1. TRIALS DURATION ELEMENTS
            layout_delays = QVBoxLayout() # 2.3. DELAYS
            layout_f_screen = QVBoxLayout()  #2.3.1. FIRST SCREEN
            layout_before_interval = QGridLayout()# 2.3.2. DELAY BEFORE TRIAL
            layout_after_interval = QGridLayout()# 2.3.3. DELAY AFTER TRIAL
            #& MAIN
            layout_main.addLayout(layout_source_n_stimuli,1)
            layout_main.addWidget(self.gb_exp_design,1)
            self.gb_settings.setLayout(layout_main)
            #& 1. SOURCES & STIMULI
            layout_source_n_stimuli.addWidget(self.gb_sources_n_test)
            layout_source_n_stimuli.addWidget(self.gb_stimuli)
            layout_source_n_stimuli.addWidget(self.gb_physiological)
            #& 1.1. SOURCES & TESTING
            layout_sources_n_test.addWidget(self.combo_rng_sources,0,0,1,3)
            layout_sources_n_test.addWidget(butt_refresh_sources,0,3,1,1)
            layout_sources_n_test.addWidget(self.tb_gen_bits,0,4,1,3)
            layout_sources_n_test.addWidget(butt_generate_bits,0,7,1,1)
            self.gb_sources_n_test.setLayout(layout_sources_n_test)
            #& 1.2. STIMULI
            layout_stimuli.addWidget(butt_neutral_stimuli)
            layout_stimuli.addWidget(butt_excitatory_stimuli)
            self.gb_stimuli.setLayout(layout_stimuli)
            #& 1.3. PHYSIOLOGICAL
            layout_physiological.addWidget(self.tb_neulog_port,0,0,1,1)
            layout_physiological.addWidget(butt_refresh_neulog,0,1,1,1)            
            layout_physiological.addWidget(butt_refresh_physiological,0,2,1,5)
            layout_physiological.addWidget(self.cb_skin_conductance,1,0,1,1)
            layout_physiological.addWidget(self.cb_heart_rate,2,0,1,1)
            layout_physiological.addWidget(self.cb_brainwaves,3,0,1,1)
            layout_physiological.addWidget(self.combo_skin_conductance,1,1,1,1)
            layout_physiological.addWidget(self.combo_heart_rate,2,1,1,1)
            layout_physiological.addWidget(self.combo_brainwaves,3,1,1,1)
            layout_physiological.addWidget(self.tb_skin_conductance_test,1,2,1,2)
            layout_physiological.addWidget(self.tb_heart_rate_test,2,2,1,2)
            layout_physiological.addWidget(self.tb_brainwaves_test,3,2,1,2)
            layout_physiological.addWidget(self.butt_skin_conductance_test,1,4,1,1)
            layout_physiological.addWidget(self.butt_heart_rate_test,2,4,1,1)
            layout_physiological.addWidget(self.butt_brainwaves_test,3,4,1,1)
            layout_physiological.addWidget(self.combo_skin_conductance_sample,1,5,1,2)
            layout_physiological.addWidget(self.combo_heart_rate_sample,2,5,1,2)
            layout_physiological.addWidget(self.combo_brainwaves_sample,3,5,1,2)
            self.gb_physiological.setLayout(layout_physiological)
            #& 2. EXP DESIGN
            layout_exp_design.addLayout(layout_trial_and_screen)
            layout_exp_design.addWidget(self.gb_trial_duration)
            layout_exp_design.addWidget(self.gb_delays,1)
            self.gb_exp_design.setLayout(layout_exp_design)
            #& 2.1 TRIALS & SESSION
            layout_trial_and_screen.addWidget(self.gb_session_id)
            layout_trial_and_screen.addWidget(self.gb_trial_type)
            layout_trial_and_screen.addWidget(self.gb_num_trials)
            #& 2.1.1. SESSION ID
            layout_session_id.addWidget(self.sb_session_id)
            self.gb_session_id.setLayout(layout_session_id)
            #& 2.1.2. TRIAL TYPE
            layout_trial_type.addWidget(self.combo_trial_type)
            self.gb_trial_type.setLayout(layout_trial_type)
            #& 2.1.3. TRIALS NUM
            layout_trial.addWidget(self.sb_num_trials)
            self.gb_num_trials.setLayout(layout_trial)
            #& 2.2. TRIALS DURATION 
            layout_duration.addWidget(self.gb_pre_screen,0,0)
            layout_duration.addWidget(self.gb_stimulus_duration,1,0)
            layout_duration.addWidget(self.gb_post_screen,2,0)
            self.gb_trial_duration.setLayout(layout_duration)
            #& 2.2.1. TRIALS DURATION ELEMENTS
            layout_dur_pre.addWidget(self.sb_pre_screen)
            self.gb_pre_screen.setLayout(layout_dur_pre)
            layout_dur_stimulus.addWidget(self.sb_stim_duration)
            self.gb_stimulus_duration.setLayout(layout_dur_stimulus)
            layout_dur_post.addWidget(self.sb_post_screen)
            self.gb_post_screen.setLayout(layout_dur_post)
            #& 2.3. DELAYS
            layout_delays.addWidget(self.gb_first_screen)
            layout_delays.addWidget(self.gb_before_interval)
            layout_delays.addWidget(self.gb_after_interval)
            self.gb_delays.setLayout(layout_delays)
            #& 2.3.1. FIRST SCREEN
            layout_f_screen.addWidget(self.sb_first_screen)
            self.gb_first_screen.setLayout(layout_f_screen)
            #& 2.3.1. BEFORE TRIAL
            layout_before_interval.addWidget(self.sb_before_min_interval,0,0)
            layout_before_interval.addWidget(self.sb_before_max_interval,0,1)
            self.gb_before_interval.setLayout(layout_before_interval)
            #& 2.3.1. AFTER TRIAL
            layout_after_interval.addWidget(self.sb_after_min_interval,0,0)
            layout_after_interval.addWidget(self.sb_after_max_interval,0,1)
            self.gb_after_interval.setLayout(layout_after_interval)

        def create_data_layout(self):
        #& GROUP BOXES
            self.gb_session_data = QGroupBox("Session Data:")
        #& TEXT BOX
            # Create text boxes
            self.tb_start_at = QLineEdit("Session started at:") #? Add color to background: tb_start_at.setStyleSheet("QLineEdit { background-color: rgb(220,220,220) }")
            self.tb_finish_at = QLineEdit("Session finished at:") 
            self.tb_onset_at = QLineEdit("First trial started at:")
            self.tb_stimulus_id = QTextEdit("Stimulus ID:")
            self.tb_trial_id = QTextEdit("Trial ID:")
            self.tb_time_start_trial = QTextEdit("Time at the start of trial:")
            self.tb_dur_before_interval = QTextEdit("Interval before each trial (s):")
            self.tb_onset_to_trial = QTextEdit("First trial to end of this trial (s):")
            self.tb_seconds_end_trial = QTextEdit("Duration of each trial (s):")
            self.tb_dur_after_interval = QTextEdit("Interval after each trial (s):")
            self.tb_time_end_trial = QTextEdit("Time at the end of trial:")
        #& SET LAYOUT     
            layout = QGridLayout()
            #top lane
            layout.addWidget(self.tb_start_at,0,0,1,3)
            layout.addWidget(self.tb_onset_at,0,3,1,2)
            layout.addWidget(self.tb_finish_at,0,5,1,3)
            # below lane
            layout.addWidget(self.tb_trial_id,1,0,5,1)
            layout.addWidget(self.tb_stimulus_id,1,1,5,1)
            layout.addWidget(self.tb_time_start_trial,1,2,5,1)
            layout.addWidget(self.tb_time_end_trial,1,3,5,1)
            layout.addWidget(self.tb_dur_before_interval,1,4,5,1) 
            layout.addWidget(self.tb_dur_after_interval,1,5,5,1) 
            layout.addWidget(self.tb_seconds_end_trial,1,6,5,1)    
            layout.addWidget(self.tb_onset_to_trial,1,7,5,1)
            self.gb_session_data.setLayout(layout)

        def create_phys_layout(self):
        #& GROUP BOXES
            self.gb_phys_data = QGroupBox("")
            self.gb_phys_time = QGroupBox("Physiologial Time Data:")
            self.gb_phys_trial_inst = QGroupBox("Trials and Instances:")
            self.gb_phys_skin_conductance = QGroupBox("Skin Conductance Data:")
            self.gb_phys_heart_rate = QGroupBox("Heart Rate Data:")
            self.gb_phys_brainwaves = QGroupBox("Brainwaves Data:")
        #& TEXT BOX
            # Create text boxes
            self.tb_phys_trial_id = QTextEdit("Trial ID [n]:")
            self.tb_phys_instance_id = QTextEdit("Instance [i]:")
            self.tb_phys_start_at = QLineEdit("Physiological data started at:") 
            self.tb_phys_finish_at = QLineEdit("Physiological data finished at:") 
            self.tb_skin_conductance_values = QTextEdit("Skin conductance values [xi]:")
            self.tb_skin_conductance_timestamp = QTextEdit("Skin conductance timestamps [t_xi]:")
            self.tb_heart_rate_values = QTextEdit("Heart rate values [yi]:")
            self.tb_heart_rate_timestamp = QTextEdit("Heart rate timestamps [t_yi]:")
            self.tb_brainwaves_values = QTextEdit("Brainwaves values [zi]:")
            self.tb_brainwaves_timestamp = QTextEdit("Brainwaves timestamps [t_zi]:")
            self.tb_skin_conductance_media = QTextEdit("Skin conductance media [mx_paa]:")
            self.tb_skin_conductance_sd = QTextEdit("Skin conductance sd [sx_paa]:")
            self.tb_skin_conductance_Z = QTextEdit("Skin conductance Z [Z_xi]:")
            self.tb_skin_conductance_f = QTextEdit("Skin conductance f [f_xi]:")
            self.tb_heart_rate_media = QTextEdit("Heart rate media [my_paa]:")
            self.tb_heart_rate_sd = QTextEdit("Heart rate sd [sy_paa]:")
            self.tb_heart_rate_Z = QTextEdit("Heart rate Z [Z_yi]:")
            self.tb_heart_rate_f = QTextEdit("Heart rate f [f_yi]:")
            self.tb_brainwaves_media = QTextEdit("Brainwaves media [mz_paa]:")
            self.tb_brainwaves_sd = QTextEdit("Brainwaves sd [sz_paa]:")
            self.tb_brainwaves_Z = QTextEdit("Brainwaves Z [Z_zi]:")
            self.tb_brainwaves_f = QTextEdit("Brainwaves f [f_zi]:")
        #& SET LAYOUT     
            main_layout = QGridLayout()
            time_layout = QGridLayout()
            trial_inst_layout = QGridLayout()
            skin_conductance_layout = QGridLayout()
            heart_rate_layout = QGridLayout()
            brainwaves_layout = QGridLayout()
            # time layout
            time_layout.addWidget(self.tb_phys_start_at,0,0,1,4)
            time_layout.addWidget(self.tb_phys_finish_at,0,4,1,4)
            # trial and instances layout
            trial_inst_layout.addWidget(self.tb_phys_trial_id,0,0,15,1) 
            trial_inst_layout.addWidget(self.tb_phys_instance_id,0,1,15,1) 
            # skin conductance layout
            skin_conductance_layout.addWidget(self.tb_skin_conductance_values,0,0,5,1)
            skin_conductance_layout.addWidget(self.tb_skin_conductance_timestamp,0,1,5,1)
            skin_conductance_layout.addWidget(self.tb_skin_conductance_media,5,0,5,1)
            skin_conductance_layout.addWidget(self.tb_skin_conductance_sd,5,1,5,1)
            skin_conductance_layout.addWidget(self.tb_skin_conductance_Z,10,0,5,1)
            skin_conductance_layout.addWidget(self.tb_skin_conductance_f,10,1,5,1)
            # heart rate layout
            heart_rate_layout.addWidget(self.tb_heart_rate_values,0,0,5,1)
            heart_rate_layout.addWidget(self.tb_heart_rate_timestamp,0,1,5,1) 
            heart_rate_layout.addWidget(self.tb_heart_rate_media,5,0,5,1)
            heart_rate_layout.addWidget(self.tb_heart_rate_sd,5,1,5,1)
            heart_rate_layout.addWidget(self.tb_heart_rate_Z,10,0,5,1)
            heart_rate_layout.addWidget(self.tb_heart_rate_f,10,1,5,1)
            # brainwaves layout
            brainwaves_layout.addWidget(self.tb_brainwaves_values,0,0,5,1) 
            brainwaves_layout.addWidget(self.tb_brainwaves_timestamp,0,1,5,1)
            brainwaves_layout.addWidget(self.tb_brainwaves_media,5,0,5,1)
            brainwaves_layout.addWidget(self.tb_brainwaves_sd,5,1,5,1)
            brainwaves_layout.addWidget(self.tb_brainwaves_Z,10,0,5,1)
            brainwaves_layout.addWidget(self.tb_brainwaves_f,10,1,5,1)
            # Apply layouts
            self.gb_phys_time.setLayout(time_layout)
            self.gb_phys_trial_inst.setLayout(trial_inst_layout)
            self.gb_phys_skin_conductance.setLayout(skin_conductance_layout)
            self.gb_phys_heart_rate.setLayout(heart_rate_layout)
            self.gb_phys_brainwaves.setLayout(brainwaves_layout)
            # Apply main layout
            main_layout.addWidget(self.gb_phys_time,0,0,1,8)
            main_layout.addWidget(self.gb_phys_trial_inst,1,0,15,2)
            main_layout.addWidget(self.gb_phys_skin_conductance,1,2,15,2)
            main_layout.addWidget(self.gb_phys_heart_rate,1,4,15,2)
            main_layout.addWidget(self.gb_phys_brainwaves,1,6,15,2)
            self.gb_phys_data.setLayout(main_layout)

        def create_stats_layout(self):
        #& GROUP BOXES
            self.gb_stats_data = QGroupBox("")
            self.gb_stats_permut = QGroupBox("Randomized Permutation Settings:")
            self.gb_stats_analysis = QGroupBox("Statistical Analysis Data:")            
            self.gb_stats_phys = QGroupBox("Include in analysis?:")            
            self.gb_stats_phys_D = QGroupBox("Physiological Difference D [D = Σ FnE - Σ FnN]:")
            self.gb_stats_results = QGroupBox("Physiological Standard Normal Deviate Z [Z = (D – μD’)/ σD’]:")
        #& TEXT BOX
            self.tb_stats_ratio_n = QLineEdit("")
            self.tb_stats_ratio_e = QLineEdit("")
            self.tb_stats_shuffle = QLineEdit("5000")
            self.tb_stats_session_id = QTextEdit("Session ID [S]:")
            self.tb_stats_trial_id = QTextEdit("Trial ID [n]:")
            self.tb_skin_conductance_ZD = QLineEdit("Skin conductance ZD:")
            self.tb_skin_conductance_D = QLineEdit("Skin conductance D:")
            self.tb_skin_conductance_Fn = QTextEdit("Skin conductance Fn [SUM_fx_paa]:")
            self.tb_heart_rate_ZD = QLineEdit("Heart rate ZD:")
            self.tb_heart_rate_D = QLineEdit("Heart rate D:")
            self.tb_heart_rate_Fn = QTextEdit("Heart rate Fn [SUM_fy_paa]:")
            self.tb_brainwaves_ZD = QLineEdit("Brainwaves ZD:")
            self.tb_brainwaves_D = QLineEdit("Brainwaves D:")
            self.tb_brainwaves_Fn = QTextEdit("Brainwaves Fn [SUM_fz_paa]:")
        #& LABELS
            self.lb_stats_ratio = QLabel("Ratio (E:N):")
            self.lb_stats_dotdot = QLabel(":")
            self.lb_stats_shuffle = QLabel('Randomized permutation cycles:')
        #& CHECKBOXES
            self.cb_stats_skin_conductance = QCheckBox("Skin Conductance")
            self.cb_stats_heart_rate = QCheckBox("Heart Rate")
            self.cb_stats_brainwaves = QCheckBox("Brainwaves")
        #& BUTTONS
            butt_shuffle = QPushButton('BEGIN ANALYSIS')
            butt_shuffle.clicked.connect(self.click_shuffle)
        #& SET LAYOUT     
            main_layout = QGridLayout()
            ratio_layout = QHBoxLayout()
            shuffle_layout = QHBoxLayout()
            permut_layout = QGridLayout()
            analysis_layout = QHBoxLayout()
            phys_layout = QHBoxLayout()
            phys_D_layout = QHBoxLayout()
            results_layout = QHBoxLayout()
            # permut layout
            ratio_layout.addWidget(self.lb_stats_ratio)
            ratio_layout.addWidget(self.tb_stats_ratio_e)
            ratio_layout.addWidget(self.lb_stats_dotdot)
            ratio_layout.addWidget(self.tb_stats_ratio_n)            
            shuffle_layout.addWidget(self.lb_stats_shuffle)
            shuffle_layout.addWidget(self.tb_stats_shuffle)
            phys_layout.addWidget(self.cb_stats_skin_conductance)
            phys_layout.addWidget(self.cb_stats_heart_rate)
            phys_layout.addWidget(self.cb_stats_brainwaves)
            self.gb_stats_phys.setLayout(phys_layout)
            phys_D_layout.addWidget(self.tb_skin_conductance_D)
            phys_D_layout.addWidget(self.tb_heart_rate_D)
            phys_D_layout.addWidget(self.tb_brainwaves_D)
            self.gb_stats_phys_D.setLayout(phys_D_layout)
            permut_layout.addLayout(ratio_layout,0,0,1,1)
            permut_layout.addLayout(shuffle_layout,1,0,1,1)
            permut_layout.addWidget(self.gb_stats_phys,0,1,2,2)
            permut_layout.addWidget(self.gb_stats_phys_D,0,3,2,2)
            # session and trials layout
            analysis_layout.addWidget(self.tb_stats_session_id)
            analysis_layout.addWidget(self.tb_stats_trial_id)
            analysis_layout.addWidget(self.tb_skin_conductance_Fn)
            analysis_layout.addWidget(self.tb_heart_rate_Fn)
            analysis_layout.addWidget(self.tb_brainwaves_Fn)
            # Results layout            
            results_layout.addWidget(self.tb_skin_conductance_ZD)
            results_layout.addWidget(self.tb_heart_rate_ZD)
            results_layout.addWidget(self.tb_brainwaves_ZD)
            # Apply layouts
            self.gb_stats_permut.setLayout(permut_layout)
            self.gb_stats_analysis.setLayout(analysis_layout)            
            self.gb_stats_results.setLayout(results_layout)
            # Apply main layout
            main_layout.addWidget(self.gb_stats_permut,0,0,4,5)    
            main_layout.addWidget(butt_shuffle,4,0,1,5)
            main_layout.addWidget(self.gb_stats_analysis,5,0,10,5)            
            main_layout.addWidget(self.gb_stats_results,15,2,1,3)
            self.gb_stats_data.setLayout(main_layout)

        def create_buttons(self):
        #& BUTTONS
            self.butt_start_session = QPushButton("START SESSION")
            self.butt_start_session.clicked.connect(self.click_start_session)
            self.butt_stop = QPushButton("STOP SESSION")
            self.butt_stop.clicked.connect(self.click_stop) 
            self.butt_clear_data = QPushButton("Clear All Data")
            self.butt_clear_data.clicked.connect(self.click_clear_data)  
            self.butt_export_CSV = QPushButton("Export Session Data to CSV")
            self.butt_export_CSV.clicked.connect(self.click_export_CSV)     
            self.butt_export_CSV_phys = QPushButton("Export Physiological Data to CSV")
            self.butt_export_CSV_phys.clicked.connect(self.click_export_CSV_phys)
        #& SET LAYOUT
            self.layout_buttons = QGridLayout()
            self.layout_buttons.addWidget(self.butt_start_session,0,0,1,4)
            self.layout_buttons.addWidget(self.butt_stop,1,0)
            self.layout_buttons.addWidget(self.butt_clear_data,1,1)
            self.layout_buttons.addWidget(self.butt_export_CSV,1,2)
            self.layout_buttons.addWidget(self.butt_export_CSV_phys,1,3)

    #& CLICK BUTTONS
        def click_start_session(self):
            # Call start_session with stated number of trials
            self.start_session(int(self.sb_num_trials.value()))

        def click_refresh_physiological(self): #!
            pass

        def click_refresh_neulog(self):
            # Create neulog class
            neu = Neulog(self.tb_neulog_port.text())
            # Check the status of the Neulog server
            status = neu.get_status()
            # If server is ready, clear combos, add "neulog" and message "Ready"
            if status == 'Neulog API status: Ready':
                self.combo_skin_conductance.clear()
                self.combo_heart_rate.clear()  
                self.combo_brainwaves.clear()  
                self.combo_skin_conductance.addItem(neu.name)
                self.combo_heart_rate.addItem(neu.name)
                self.combo_brainwaves.addItem(neu.name)
                QMessageBox.about(self, "Neulog", "Neulog API status: Ready")
            # If server is in experiment, stop experiment and message "stopping experiment"
            elif status == 'Neulog API status: Experiment':
                QMessageBox.about(self, "Neulog", "Stopping Neulog experiment, try again...")
                neu.exp_stop()
            else:
                QMessageBox.about(self, "Neulog", "Impossible to connect, check port number")
        
        def click_skin_conductance_test(self):
            # Create neulog class with GSR sensor
            neu = Neulog(self.tb_neulog_port.text(), 'GSR')
            # Set GSR sensor range to miliSiemens
            neu.set_sensor_range('2')
            # if neulog is selected...
            if neu.name == self.combo_skin_conductance.currentText():
                # Obtain values
                self.tb_skin_conductance_test.setText("GSR: " + str(neu.get_values()[0]))
            else:
                pass

        def click_heart_rate_test(self):
            # Create neulog class with Pulse sensor
            neu = Neulog(self.tb_neulog_port.text(), 'Pulse')
            neu.set_sensor_range('1')
            # if neulog is selected...
            if neu.name == self.combo_heart_rate.currentText():
                # Obtain values
                self.tb_heart_rate_test.setText("Pulse: " + str(neu.get_values()[0]))
            else:
                pass

        def click_brainwaves_test(self): #!
            pass

        def check_skin_conductance(self):
            if self.cb_skin_conductance.isChecked():
                self.combo_skin_conductance.setEnabled(True)
                self.tb_skin_conductance_test.setEnabled(True)
                self.butt_skin_conductance_test.setEnabled(True)
                self.combo_skin_conductance_sample.setEnabled(True)
            else:
                self.combo_skin_conductance.setEnabled(False)
                self.tb_skin_conductance_test.setEnabled(False)
                self.butt_skin_conductance_test.setEnabled(False)
                self.combo_skin_conductance_sample.setEnabled(False)

        def check_heart_rate(self):
            if self.cb_heart_rate.isChecked():
                self.combo_heart_rate.setEnabled(True)
                self.tb_heart_rate_test.setEnabled(True)
                self.butt_heart_rate_test.setEnabled(True)
                self.combo_heart_rate_sample.setEnabled(True)
            else:
                self.combo_heart_rate.setEnabled(False)
                self.tb_heart_rate_test.setEnabled(False)
                self.butt_heart_rate_test.setEnabled(False)
                self.combo_heart_rate_sample.setEnabled(False)

        def check_brainwaves(self):
            if self.cb_brainwaves.isChecked():
                self.combo_brainwaves.setEnabled(True)
                self.tb_brainwaves_test.setEnabled(True)
                self.butt_brainwaves_test.setEnabled(True)
                self.combo_brainwaves_sample.setEnabled(True)
            else:
                self.combo_brainwaves.setEnabled(False)
                self.tb_brainwaves_test.setEnabled(False)
                self.butt_brainwaves_test.setEnabled(False)
                self.combo_brainwaves_sample.setEnabled(False)

        def click_refresh_sources(self):
            self.combo_rng_sources.clear()    
            pseudo = Pseudo_RNG()
            self.combo_rng_sources.addItem(pseudo.name)
            psyleron = PsyREG()
            if psyleron.count_PsyREGs() >= 1:
                self.combo_rng_sources.addItem(str(psyleron.get_name()))
            else:
                pass

        def click_generate_bits(self):
            self.tb_gen_bits.clear()    
            # self.gen_bits.setText("00101")
            psyleron = PsyREG()
            pseudo = Pseudo_RNG()
            if str(psyleron.get_name()) == self.combo_rng_sources.currentText():
                if psyleron.count_PsyREGs() >= 1:
                    self.tb_gen_bits.setText("Psyleron:" + str(psyleron.get_bits(6)))
                    psyleron.clear_RNG()
                    psyleron.release_RNG()
                else:
                    QMessageBox.about(self, "ERROR", "Psyleron didn't send bits")
            else:
                if pseudo.name == self.combo_rng_sources.currentText():
                    self.tb_gen_bits.setText("Pseudo-RNG:" + str(pseudo.get_bits(6)))
                else:
                    QMessageBox.about(self, "ERROR", "Pseudo-RNG didn't send bits")

        def click_clear_data(self):
            # Establish again the normal texts
            self.tb_start_at.setText("Session started at:") 
            self.tb_finish_at.setText("Session finished at:") 
            self.tb_onset_at.setText("First trial started at:")
            self.tb_skin_conductance_D.setText("Skin conductance D:")
            self.tb_heart_rate_D.setText("Heart rate D:")
            self.tb_brainwaves_D.setText("Brainwaves D:")
            self.tb_trial_id.setText("Trial ID:")
            self.tb_stimulus_id.setText("Stimulus ID:")
            self.tb_time_start_trial.setText("Time at the start of trial:")
            self.tb_onset_to_trial.setText("First trial to end of this trial (s):")
            self.tb_seconds_end_trial.setText("Duration of each trial (s):")
            self.tb_dur_after_interval.setText("Interval after each trial (s):")
            self.tb_dur_before_interval.setText("Interval before trial (s):")
            self.tb_time_end_trial.setText("Time at the end of trial:")
            self.tb_skin_conductance_Fn.setText("Skin conductance Fn [Σf_xi_paa]:")
            self.tb_heart_rate_Fn.setText("Heart rate Fn [Σf_yi_paa]:")
            self.tb_brainwaves_Fn.setText("Brainwaves Fn [Σf_zi_paa]:")
            self.tb_phys_start_at.setText("Physiological data started at:")
            self.tb_phys_finish_at.setText("Physiological data finished at:")
            self.tb_phys_trial_id.setText("Trial ID [n]:")
            self.tb_phys_instance_id.setText("Instance [i]:")
            self.tb_skin_conductance_values.setText("Skin conductance values [xi]:")
            self.tb_skin_conductance_timestamp.setText("Skin conductance timestamps [t_xi]:")
            self.tb_skin_conductance_media.setText("Skin conductance media [mx_paa]:")
            self.tb_skin_conductance_sd.setText("Skin conductance sd [sx_paa]:")
            self.tb_skin_conductance_Z.setText("Skin conductance Z [Z_xi]:")
            self.tb_skin_conductance_f.setText("Skin conductance f [f_xi]:")
            self.tb_heart_rate_values.setText("Heart rate values [yi]:")
            self.tb_heart_rate_timestamp.setText("Heart rate timestamps [t_yi]:")
            self.tb_heart_rate_media.setText("Heart rate media [my_paa]:")
            self.tb_heart_rate_sd.setText("Heart rate sd [sy_paa]:")
            self.tb_heart_rate_Z.setText("Heart rate Z [Z_yi]:")
            self.tb_heart_rate_f.setText("Heart rate f [f_yi]:")
            self.tb_brainwaves_values.setText("Brainwaves values [zi]:")
            self.tb_brainwaves_timestamp.setText("Brainwaves timestamps [t_zi]:")
            self.tb_brainwaves_media.setText("Brainwaves media [mz_paa]:")
            self.tb_brainwaves_sd.setText("Brainwaves sd [sz_paa]:")
            self.tb_brainwaves_Z.setText("Brainwaves Z [Z_zi]:")
            self.tb_brainwaves_f.setText("Brainwaves f [f_zi]:")

        def click_export_CSV_phys(self):
            # Convert text in textbox to string
            str_session_id = "S" + self.sb_session_id.text()
            str_phys_trial_id = self.tb_phys_trial_id.toPlainText()
            str_phys_instance_id = self.tb_phys_instance_id.toPlainText()
            str_skin_conductance_values = self.tb_skin_conductance_values.toPlainText()
            str_skin_conductance_timestamp = self.tb_skin_conductance_timestamp.toPlainText()
            str_skin_conductance_media = self.tb_skin_conductance_media.toPlainText()
            str_skin_conductance_sd = self.tb_skin_conductance_sd.toPlainText()
            str_skin_conductance_Z = self.tb_skin_conductance_Z.toPlainText()
            str_skin_conductance_f = self.tb_skin_conductance_f.toPlainText()
            str_heart_rate_values = self.tb_heart_rate_values.toPlainText()
            str_heart_rate_timestamp = self.tb_heart_rate_timestamp.toPlainText()
            str_heart_rate_media = self.tb_heart_rate_media.toPlainText()
            str_heart_rate_sd = self.tb_heart_rate_sd.toPlainText()
            str_heart_rate_Z = self.tb_heart_rate_Z.toPlainText()
            str_heart_rate_f = self.tb_heart_rate_f.toPlainText()
            str_brainwaves_values = self.tb_brainwaves_values.toPlainText()
            str_brainwaves_timestamp = self.tb_brainwaves_timestamp.toPlainText()
            str_brainwaves_media = self.tb_brainwaves_media.toPlainText()
            str_brainwaves_sd = self.tb_brainwaves_sd.toPlainText()
            str_brainwaves_Z = self.tb_brainwaves_Z.toPlainText()
            str_brainwaves_f = self.tb_brainwaves_f.toPlainText()
            # Convert string to list
            list_session_id = str_session_id.split("\n")
            list_phys_trial_id = str_phys_trial_id.split("\n")
            list_phys_instance_id = str_phys_instance_id.split("\n")
            list_skin_conductance_values = str_skin_conductance_values.split("\n")
            list_skin_conductance_timestamp = str_skin_conductance_timestamp.split("\n")
            list_skin_conductance_media = str_skin_conductance_media.split("\n")
            list_skin_conductance_sd = str_skin_conductance_sd.split("\n")
            list_skin_conductance_Z = str_skin_conductance_Z.split("\n")
            list_skin_conductance_f = str_skin_conductance_f.split("\n")
            list_heart_rate_values = str_heart_rate_values.split("\n")
            list_heart_rate_timestamp = str_heart_rate_timestamp.split("\n")
            list_heart_rate_media = str_heart_rate_media.split("\n")
            list_heart_rate_sd = str_heart_rate_sd.split("\n")
            list_heart_rate_Z = str_heart_rate_Z.split("\n")            
            list_heart_rate_f = str_heart_rate_f.split("\n")
            list_brainwaves_values = str_brainwaves_values.split("\n")
            list_brainwaves_timestamp = str_brainwaves_timestamp.split("\n")
            list_brainwaves_media = str_brainwaves_media.split("\n")
            list_brainwaves_sd = str_brainwaves_sd.split("\n")
            list_brainwaves_Z = str_brainwaves_Z.split("\n")
            list_brainwaves_f = str_brainwaves_f.split("\n")
            # Remove first line in each of the session data lists
            del list_phys_trial_id[0]
            del list_phys_instance_id[0]
            del list_skin_conductance_values[0]
            del list_skin_conductance_timestamp[0]
            del list_skin_conductance_media[0]
            del list_skin_conductance_sd[0]
            del list_skin_conductance_Z[0]
            del list_skin_conductance_f[0]
            del list_heart_rate_values[0]
            del list_heart_rate_timestamp[0]
            del list_heart_rate_media[0]
            del list_heart_rate_sd[0]
            del list_heart_rate_Z[0]
            del list_heart_rate_f[0]
            del list_brainwaves_values[0]
            del list_brainwaves_timestamp[0]
            del list_brainwaves_media[0]
            del list_brainwaves_sd[0]
            del list_brainwaves_Z[0]
            del list_brainwaves_f[0]
            # Convert list to series
            ser_session_id = pandas.Series(list_session_id, name='Session ID [S]:')
            ser_phys_trial_id = pandas.Series(list_phys_trial_id, name='Trial ID [n]:')
            ser_phys_instance_id = pandas.Series(list_phys_instance_id, name='Instance ID [i]:')
            ser_skin_conductance_values = pandas.Series(list_skin_conductance_values, name='Skin Conductance Values[xi]:')
            ser_skin_conductance_timestamp = pandas.Series(list_skin_conductance_timestamp, name='Skin Conductance Timestamp[t_xi]:')
            ser_skin_conductance_media = pandas.Series(list_skin_conductance_media, name='Skin Conductance Media[mx_paa]:')
            ser_skin_conductance_sd = pandas.Series(list_skin_conductance_sd, name='Skin Conductance SD [sx_paa]:')
            ser_skin_conductance_Z = pandas.Series(list_skin_conductance_Z, name='Skin Conductance Z [Z_xi]:')
            ser_skin_conductance_f = pandas.Series(list_skin_conductance_f, name='Skin Conductance f [f_xi]:')
            ser_heart_rate_values = pandas.Series(list_heart_rate_values, name='Heart Rate Values [yi]:')
            ser_heart_rate_timestamp = pandas.Series(list_heart_rate_timestamp, name='Heart Rate Timestamp [t_yi]:')
            ser_heart_rate_media = pandas.Series(list_heart_rate_media, name='Heart Rate Media [my_paa]:')
            ser_heart_rate_sd = pandas.Series(list_heart_rate_sd, name='Heart Rate SD [sy_paa]:')
            ser_heart_rate_Z = pandas.Series(list_heart_rate_Z, name='Heart Rate Z [Z_yi]:')
            ser_heart_rate_f = pandas.Series(list_heart_rate_f, name='Heart Rate f [f_yi]:')
            ser_brainwaves_values = pandas.Series(list_brainwaves_values, name='Brainwaves Values [zi]:')
            ser_brainwaves_timestamp = pandas.Series(list_brainwaves_timestamp, name='Brainwaves Timestamp [t_zi]:')
            ser_brainwaves_media = pandas.Series(list_brainwaves_media, name='Brainwaves Media [mz_paa]:')
            ser_brainwaves_sd = pandas.Series(list_brainwaves_sd, name='Brainwaves SD [sz_paa]:')
            ser_brainwaves_Z = pandas.Series(list_brainwaves_Z, name='Brainwaves Z [Z_zi]:')
            ser_brainwaves_f = pandas.Series(list_brainwaves_f, name='Brainwaves f [f_zi]:')
            # Generate dataframe by concatenating the series
            df = pandas.concat([ser_session_id,
                ser_phys_trial_id,
                ser_phys_instance_id,
                ser_skin_conductance_values,
                ser_skin_conductance_timestamp,
                ser_skin_conductance_media,
                ser_skin_conductance_sd,
                ser_skin_conductance_Z,
                ser_skin_conductance_f,
                ser_heart_rate_values,
                ser_heart_rate_timestamp,
                ser_heart_rate_media,
                ser_heart_rate_sd,
                ser_heart_rate_Z,
                ser_heart_rate_f,
                ser_brainwaves_values,
                ser_brainwaves_timestamp,
                ser_brainwaves_media,
                ser_brainwaves_sd,
                ser_brainwaves_Z,
                ser_brainwaves_f], axis=1)
            # Obtain the path for the file to be saved
            save_path_name, _ = QFileDialog.getSaveFileName(self, 'Save File')
            df.to_csv(save_path_name, index=False, encoding='ANSI') # "header=False" if want to remove headers
            # print(df)
            print(save_path_name)

        def click_export_CSV(self):
            # Convert text in textbox to string
            str_start_at = self.tb_start_at.text()
            str_finish_at = self.tb_finish_at.text()
            str_onset_at = self.tb_onset_at.text()
            str_skin_conductance_D = self.tb_skin_conductance_D.text()
            str_heart_rate_D = self.tb_heart_rate_D.text()
            str_brainwaves_D = self.tb_brainwaves_D.text()
            str_trial_id = self.tb_trial_id.toPlainText()
            str_stimulus_id = self.tb_stimulus_id.toPlainText()
            str_time_start_trial = self.tb_time_start_trial.toPlainText()
            str_onset_to_trial = self.tb_onset_to_trial.toPlainText()
            str_seconds_end_trial = self.tb_seconds_end_trial.toPlainText()
            str_dur_after_interval = self.tb_dur_after_interval.toPlainText()
            str_dur_before_interval = self.tb_dur_before_interval.toPlainText()
            str_time_end_trial = self.tb_time_end_trial.toPlainText()
            str_skin_conductance_Fn = self.tb_skin_conductance_Fn.toPlainText()
            str_heart_rate_Fn = self.tb_heart_rate_Fn.toPlainText()
            str_brainwaves_Fn = self.tb_brainwaves_Fn.toPlainText()
            # Remove specific text from strings
            str_start_at = str_start_at.replace('Session started at: ', '')
            str_finish_at = str_finish_at.replace('Session finished at: ', '')
            str_onset_at = str_onset_at.replace('First trial started at: ', '')
            str_skin_conductance_D = str_skin_conductance_D.replace('Skin conductance D [SUM(FnE)-SUM(FnN)]: ', '')
            str_heart_rate_D = str_heart_rate_D.replace('Heart rate D [SUM(FnE)-SUM(FnN)]: ', '')
            str_brainwaves_D = str_brainwaves_D.replace('Brainwaves D [SUM(FnE)-SUM(FnN)]: ', '')
            # Convert string to list
            list_start_at = str_start_at.split("\n")
            list_finish_at = str_finish_at.split("\n")
            list_onset_at = str_onset_at.split("\n")
            list_skin_conductance_D = str_skin_conductance_D.split("\n")
            list_heart_rate_D = str_heart_rate_D.split("\n")
            list_brainwaves_D = str_brainwaves_D.split("\n")
            list_trial_id = str_trial_id.split("\n")
            list_stimulus_id = str_stimulus_id.split("\n")
            list_time_start_trial = str_time_start_trial.split("\n")
            list_onset_to_trial = str_onset_to_trial.split("\n")
            list_seconds_end_trial = str_seconds_end_trial.split("\n")
            list_dur_after_interval = str_dur_after_interval.split("\n")
            list_dur_before_interval = str_dur_before_interval.split("\n")
            list_time_end_trial = str_time_end_trial.split("\n")
            list_skin_conductance_Fn = str_skin_conductance_Fn.split("\n")
            list_heart_rate_Fn = str_heart_rate_Fn.split("\n")
            list_brainwaves_Fn = str_brainwaves_Fn.split("\n")
            # Remove first line in each of the session data lists
            del list_trial_id[0]
            del list_stimulus_id[0]
            del list_time_start_trial[0]
            del list_onset_to_trial[0]
            del list_seconds_end_trial[0]
            del list_dur_after_interval[0]
            del list_dur_before_interval[0]
            del list_time_end_trial[0]
            del list_skin_conductance_Fn[0]
            del list_heart_rate_Fn[0]
            del list_brainwaves_Fn[0]
            # Convert list to series
            ser_start_at = pandas.Series(list_start_at, name='Session started at:')
            ser_finish_at = pandas.Series(list_finish_at, name='Session finished at:')
            ser_onset_at = pandas.Series(list_onset_at, name='First trial started at:')
            ser_skin_conductance_D = pandas.Series(list_skin_conductance_D, name='Skin conductance D [SUM(FnE)-SUM(FnN)]:')
            ser_heart_rate_D = pandas.Series(list_heart_rate_D, name='Heart rate D [SUM(FnE)-SUM(FnN)]:')
            ser_brainwaves_D = pandas.Series(list_brainwaves_D, name='Brainwaves D [SUM(FnE)-SUM(FnN)]:')
            ser_trial_id = pandas.Series(list_trial_id, name='Trial ID:')
            ser_stimulus_id = pandas.Series(list_stimulus_id, name='Stimulus ID:')
            ser_time_start_trial = pandas.Series(list_time_start_trial, name='Time at the start of trial:')
            ser_onset_to_trial = pandas.Series(list_onset_to_trial, name='First trial to end of this trial (s):')
            ser_seconds_end_trial = pandas.Series(list_seconds_end_trial, name='Duration of each trial (s):')
            ser_dur_after_interval = pandas.Series(list_dur_after_interval, name='Interval after of each trial (s):')
            ser_dur_before_interval = pandas.Series(list_dur_before_interval, name='Interval before of each trial (s):')
            ser_time_end_trial = pandas.Series(list_time_end_trial, name='Time at the end of trial:')
            ser_skin_conductance_Fn = pandas.Series(list_skin_conductance_Fn, name='Skin conductance Fn [SUM_fx_paa]:')
            ser_heart_rate_Fn = pandas.Series(list_heart_rate_Fn, name='Heart rate Fn [SUM_fy_paa]:')
            ser_brainwaves_Fn = pandas.Series(list_brainwaves_Fn, name='Brainwaves Fn [SUM_fz_paa]:')
            # Generate dataframe by concatenating the series
            df = pandas.concat([ser_start_at,
                ser_finish_at,
                ser_onset_at,
                ser_skin_conductance_D,
                ser_heart_rate_D,
                ser_brainwaves_D,
                ser_trial_id,      
                ser_stimulus_id,
                ser_time_start_trial,
                ser_time_end_trial,
                ser_dur_before_interval,
                ser_dur_after_interval,
                ser_seconds_end_trial,
                ser_onset_to_trial,
                ser_skin_conductance_Fn,
                ser_heart_rate_Fn,
                ser_brainwaves_Fn], axis=1)
            # Obtain the path for the file to be saved
            save_path_name, _ = QFileDialog.getSaveFileName(self, 'Save File')
            df.to_csv(save_path_name, index=False, encoding='ANSI') # "header=False" if want to remove headers
            # print(df)
            print(save_path_name)

        def click_stop(self):
            self.CODE_REBOOT = 1
            # Close white screen
            self.white_w.close()
            # Add the datastamp for the end of the session
            t_ff = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self.tb_finish_at.setText("SESSION STOPPED AT: " + t_ff)  
            # Show message stating the end of the session
            QMessageBox.about(self, "STOPPING...", "Wait until TRIAL and SESSION are stopped...")

        def click_trial_type(self, index):
            self.sb_before_min_interval.setEnabled(index)
            self.sb_before_max_interval.setEnabled(index)

        def click_neutral_stimuli(self):
            # Obtain the path of the directory with the stimuli
            open_path_name = QFileDialog.getExistingDirectory(self, 'Select the folder that contains the neutral stimuli')
            # Convert obtained path to OS native syntaxis of path
            open_path_name = QDir.toNativeSeparators(open_path_name)
            # Add '/*' to obtain all stimuli
            open_path_name = open_path_name+'\*'
            self.gen_imgage_list(open_path_name,self.image_list_neutral,self.image_list_neutral_filenames)

        def click_excitatory_stimuli(self):
            # Obtain the path of the directory with the stimuli
            open_path_name = QFileDialog.getExistingDirectory(self, 'Select the folder that contains the excitatory stimuli')
            # Convert obtained path to OS native syntaxis of path
            open_path_name = QDir.toNativeSeparators(open_path_name)
            # Add '/*' to obtain all stimuli
            open_path_name = open_path_name+'\*'
            self.gen_imgage_list(open_path_name, self.image_list_excitatory,self.image_list_excitatory_filenames)
        
        def click_shuffle(self): #!
            pass
    
    #& RNG DO STUFF
        def rng_get_bits(self, rng, bits, min_interval, len_min_interval, max_interval, len_max_interval):
            while bits > max_interval or bits < min_interval:
                # Obtain specified max bits of RNG to generate interval
                str_bits = rng.get_bits(len_max_interval)
                bits = int(str_bits,2)
            if bits <= max_interval and bits >= min_interval:
                interval = bits
                # Convert interval to seconds for being used in the Qtimer
                interval1000 = interval * 1000
                return interval1000
            else:
                QMessageBox.about(self, "ERROR", "RNG bits are inconsistent. Report bug with this messsage 'Review rng_get_bits'")

        def rng_get_image(self, rng, bits, len_imglist, len_bin_imagelist):
            while bits >= len_imglist:
                # Obtain bits of RNG to generate index for imagelist
                str_bits = rng.get_bits(len_bin_imagelist)
                bits = int(str_bits,2)
            if bits < len_imglist:
                # Append with 'N' if neutral and 'E' if excotatory, and show image
                # Starts counting from 0, so adding + 1 to the string
                if bits < self.len_image_list_neutral:
                    self.tb_stimulus_id.append("N-" + str(bits + 1))
                else:
                    self.tb_stimulus_id.append("E-" + str(bits + 1))
                # Obtain image number in "image_list_filenames" array
                self.image_window(self.image_list_filenames[bits])
            else:
                QMessageBox.about(self, "ERROR", "RNG bits generated an index number out of the range of the image list. Report bug with this messsage 'Review rng_get_image'")

    #& DO STUFF
        def thread_neulog(self,neulog_class,num_sensors,total_secs):
            # Every (aprox) 10 seconds, get the values from Neulog and save as self.diction; also print length of the list in the dictionary
            for x in range(total_secs):
                time.sleep(9)
                self.diction = neulog_class.get_exp_values()
                print(datetime.now().strftime('%H:%M:%S.%f')[:-3])
                for y in range(num_sensors):
                    print(len(self.diction[y]))
        
        def delete_unused_phys_data(self, tb_time_versus_ant, tb_time_versus_post, tb_timestamps, tb_phys_vals):
            # Convert text in textboxes to string
            str_time_versus_ant = tb_time_versus_ant.text()
            str_time_versus_post = tb_time_versus_post.text()
            str_timestamps = tb_timestamps.toPlainText()
            str_phys_vals = tb_phys_vals.toPlainText()
            # Obtain only time from string
            str_time_versus_ant = str_time_versus_ant[-12:]
            str_time_versus_post = str_time_versus_post[-12:]
            # Convert string to list
            list_timestamps = str_timestamps.split("\n")
            list_phys_vals = str_phys_vals.split("\n")
            list_time_versus_ant = str_time_versus_ant.split("\n")
            list_time_versus_post = str_time_versus_post.split("\n")
            # Store and remove first line in each of the session data lists
            list_timestamps_0 = list_timestamps[0]
            del list_timestamps[0]
            list_phys_vals_0 = list_phys_vals[0]
            del list_phys_vals[0]
            # Format the string timestamps to time format
            list_timestamps_copy = list_timestamps.copy()
            t_first = datetime.strptime(list_time_versus_ant[0],'%H:%M:%S.%f')
            t_last = datetime.strptime(list_time_versus_post[0],'%H:%M:%S.%f')
            count = 0
            count_last = 0
            # For each timestamp, format to time and compare to first trial, and...
            for instance in list_timestamps_copy:
                t_instance = datetime.strptime(instance,'%H:%M:%S.%f')
                #remove the ones before the first trial
                if t_instance < t_first:
                    list_timestamps.remove(instance)
                    count += 1
                #remove the ones after the session ending
                if t_instance > t_last:
                    list_timestamps.remove(instance)
                    count_last += 1
            # Remove each value in the physical data corresponding to the deleted timestamps
            for value in range(count):
                del list_phys_vals[0]
            for value in range(count_last):
                del list_phys_vals[-1]
            # Set the stored text for each textbox
            tb_timestamps.setText(str(list_timestamps_0)) 
            tb_phys_vals.setText(str(list_phys_vals_0))
            # Append the good timestamps and values, corresponding to the start of the first trial
            for instance in list_timestamps:
                tb_timestamps.append(str(instance))
            for instance in list_phys_vals:
                tb_phys_vals.append(str(instance))
        
        def create_phys_ids(self, tb_trials, tb_start_trial, tb_end_trial, tb_timestamps, tb_trialids, tb_instanceids):
            # Convert text in textboxes to string
            str_trials = tb_trials.toPlainText()
            str_start_trial = tb_start_trial.toPlainText()
            str_end_trial= tb_end_trial.toPlainText()
            str_timestamps = tb_timestamps.toPlainText()
            # Convert string to list
            list_trials = str_trials.split("\n")
            list_start_trial = str_start_trial.split("\n")
            list_end_trial = str_end_trial.split("\n")
            list_timestamps = str_timestamps.split("\n")
            # Remove first line in each of the data in lists
            del list_timestamps[0]
            del list_trials[0]
            del list_start_trial[0]
            del list_end_trial[0]
            # Counts for each trial and instance
            count_trial = 0
            count_instance = 1
            # For each timestamp, format to time and compare to start of trial and end of trial
            for instance in list_timestamps:
                t_instance = datetime.strptime(instance,'%H:%M:%S.%f')
                t_start_instance = datetime.strptime(list_start_trial[count_trial],'%H:%M:%S.%f')
                t_end_instance = datetime.strptime(list_end_trial[count_trial],'%H:%M:%S.%f')
                # For each instance, add the trial ID and instance ID to the respective textboxes
                if t_instance >= t_start_instance:
                    if t_instance < t_end_instance:
                        tb_trialids.append(str(list_trials[count_trial]))
                        tb_instanceids.append(str(count_instance))
                        count_instance += 1
                    else:
                        count_trial += 1
                        count_instance = 1
                        tb_trialids.append(str(list_trials[count_trial]))
                        tb_instanceids.append(str(count_instance))
                        count_instance += 1

        def calculate_media_sd_Z_f_Fn(self,presentiment_instances,tb_no_trials,tb_phys_vals,tb_trialids,tb_instanceids,tb_phys_media,tb_phys_sd, tb_phys_Z, tb_phys_f,tb_Fn):
            # Convert text in textboxes to string
            str_no_trials = tb_no_trials.toPlainText()
            str_phys_vals = tb_phys_vals.toPlainText()
            str_trialids = tb_trialids.toPlainText()
            str_instanceids = tb_instanceids.toPlainText()
            # Convert string to list
            list_no_trials = str_no_trials.split("\n")
            list_phys_vals = str_phys_vals.split("\n")
            list_trialids = str_trialids.split("\n")
            list_instanceids = str_instanceids.split("\n")
            # Remove first line in each of the data in lists
            del list_no_trials[0]
            del list_phys_vals[0]
            del list_trialids[0]
            del list_instanceids[0]
            # Declare counts:
            count_presentiment_instances = 1
            count_trials = 0
            # Add the presentiment instances per trial to the corresponding presentiment_list
            presentiment_lists = []
            presentiment_lists_len = []
            for trial in list_no_trials:
                presentiment_lists.append([])
                count_instances = -1
                for value in list_phys_vals:
                    count_instances += 1
                    if trial == list_trialids[count_instances]:
                        if count_presentiment_instances <= presentiment_instances:
                            presentiment_lists[count_trials].append(float(value))
                            count_presentiment_instances += 1
                # Add the lenght of each presentiment list to presentiment_list_len and raise counters
                presentiment_lists_len.append(len(presentiment_lists[count_trials]))
                count_trials += 1
                count_presentiment_instances = 1
            # For each trial calculate media and sd of the presentiment timeframe
            count_trials = 0
            for trial in list_no_trials:
                phys_media = numpy.mean(presentiment_lists[count_trials])
                phys_sd = numpy.std(presentiment_lists[count_trials], ddof=1)
                # Define counts:
                count_instances = -1
                count_Z = -1
                count_Fn = -1
                Fn = 0
                # For each value calculate Z and f, and append media, sd, Z and f to the respective textboxes
                for value in list_phys_vals:
                    count_instances += 1
                    if trial == list_trialids[count_instances]:
                        phys_Z = (float(value)-phys_media)/phys_sd
                        count_Z += 1
                        count_Fn += 1
                        if count_Z == 0:
                            Z0 = phys_Z
                        phys_f = phys_Z - Z0
                        tb_phys_media.append(str(phys_media))
                        tb_phys_sd.append(str(phys_sd))
                        tb_phys_Z.append(str(phys_Z))
                        tb_phys_f.append(str(phys_f))
                        # Sum each f in the presentiment timeframe to generate Fn for each trial
                        if count_Fn < presentiment_lists_len[count_trials]:
                            Fn += phys_f
                tb_Fn.append(str(Fn))
                count_trials += 1
        
        def calculate_D_Z(self,stimulus_id,trial_Fn,tb_D,tb_ZD):
            # Store tb_D and tb_ZD text
            tb_D_text = tb_D.text()
            tb_ZD_text = tb_ZD.text()
            # Convert text in textboxes to string
            str_stimulus_id = stimulus_id.toPlainText()
            str_trial_Fn = trial_Fn.toPlainText()
            # Convert string to list
            list_stimulus_id = str_stimulus_id.split("\n")
            list_trial_Fn = str_trial_Fn.split("\n")
            # Remove first line in each of the data in lists
            del list_stimulus_id[0]
            del list_trial_Fn[0]
            # Declare number of stimuli and sums
            N_stimuli = 0
            E_stimuli = 0
            sum_N_stimuli = 0
            sum_E_stimuli = 0
            count_trials = 0
            # Count the number of neutral and excitatory stimuli in the stimulus_id textbox
            for stim_id in list_stimulus_id:
                if stim_id[:1] == 'N':
                    N_stimuli += 1
                    sum_N_stimuli += float(list_trial_Fn[count_trials])
                else:
                    E_stimuli += 1
                    sum_E_stimuli += float(list_trial_Fn[count_trials])
                count_trials += 1
            # Calculate D (Σ FE - Σ FN) and append it to tb_D
            calc_D = sum_E_stimuli - sum_N_stimuli
            tb_D.setText(str(tb_D_text) + " " + str(calc_D))
            # Create list of floats from list_trial_Fn
            list_trial_Fn_floats = [float(i) for i in list_trial_Fn]
            # Shuffle 5000 times the Fn values to generate D' to make a normal distribution
            list_D_prime = []
            for x in range (5000):
                numpy.random.shuffle(list_trial_Fn_floats)
                calc_D_prime = sum(list_trial_Fn_floats[:E_stimuli]) - sum(list_trial_Fn_floats[E_stimuli:])
                list_D_prime.append(calc_D_prime)
            calc_D_prime_media = numpy.mean(list_D_prime)
            calc_D_prime_sd = numpy.std(list_D_prime)
            calc_z = (calc_D - calc_D_prime_media) / calc_D_prime_sd
            tb_ZD.setText(str(tb_ZD_text) + " " + str(calc_z))

    #& DISPLAY IMAGES
        def gen_imgage_list(self,open_path,img_list,img_list_fnames):            
            # Create an list of images from the directory which contains the stimuli
            for filename in glob.glob(open_path):
                im = Image.open(filename)
                img_list.append(im)
                img_list_fnames.append(im.filename)

        def white_window(self):
            # Create a QWidget where the Qlabel containing the image will be stored
            self.white_w = QWidget()
            label = QLabel(self.white_w)
            # Obtain the image from route
            path_pixmap = os.path.join(os.getcwd(), '.\Presentimiento\White.png') # White Screen path
            pixmap = QtGui.QPixmap(path_pixmap)
            # Fix the possible size of the image
            pixmap = pixmap.scaled(2048, 1024, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            # Create the layout
            lay = QVBoxLayout()
            lay.addWidget(label)
            self.white_w.setLayout(lay)
            self.white_w.showFullScreen()

        def image_window(self, ruta):
            # Create a QWidget where the Qlabel containing the image will be stored
            self.image_w = QWidget()
            label = QLabel(self.image_w)
            # Obtain the image from route
            pixmap = QtGui.QPixmap(ruta)
            # Fix the possible size of the image
            pixmap = pixmap.scaled(2048, 1024, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            # Create the layout
            lay = QVBoxLayout()
            lay.addWidget(label)
            self.image_w.setLayout(lay)
            self.image_w.showFullScreen()

    #& START SESSION
        def start_session(self, trials):
        #& SET START TIMESTAMP
            # Print TimeStamp in the "Start at:" box.
            t_start = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self.tb_start_at.setText("Session started at: " + t_start)
        #& START RECORDING PHYSIOLOGICAL DATA
            # define physiological classes
            #& NEULOG
            # Define neulog class
            neu = Neulog(self.tb_neulog_port.text())
            neulog_used = False
            neulog_phys_params = ""
            neulog_num_sensors = 0
            # Obtain the max amount of time for each trial
            neulog_seconds = int(self.sb_first_screen.value()) + (int(self.sb_pre_screen.value()
                + self.sb_stim_duration.value() + self.sb_post_screen.value()
                + self.sb_before_max_interval.value() + self.sb_after_max_interval.value())
                * int(self.sb_num_trials.value()))
            if self.cb_skin_conductance.isChecked():
                neulog_num_sensors += 1
                if neu.name == self.combo_skin_conductance.currentText():
                    neulog_used = True
                    neulog_phys_params += ",GSR"
                    neulog_samples_mult = int(self.combo_skin_conductance_sample.currentText()[:-11])
                    # Translate the sample rate in main window to the Neulog API sample rate index
                    if self.combo_skin_conductance_sample.currentText() == "20 per second":
                        neulog_rate = '7'
                    elif self.combo_skin_conductance_sample.currentText() == "10 per second":
                        neulog_rate = '8'
                    elif self.combo_skin_conductance_sample.currentText() == "5 per second":
                        neulog_rate = '9'
                    elif self.combo_skin_conductance_sample.currentText() == "2 per second":
                        neulog_rate = '10'
                    elif self.combo_skin_conductance_sample.currentText() == "1 per second":
                        neulog_rate = '11'
                else:
                    pass
            if self.cb_heart_rate.isChecked():
                neulog_num_sensors += 1
                if neu.name == self.combo_heart_rate.currentText():
                    neulog_used = True
                    neulog_phys_params += ",Pulse"
                    neulog_samples_mult = int(self.combo_skin_conductance_sample.currentText()[:-11])
                    # Translate the sample rate in main window to the Neulog API sample rate index
                    if self.combo_heart_rate_sample.currentText() == "20 per second":
                        neulog_rate = '7'
                    elif self.combo_heart_rate_sample.currentText() == "10 per second":
                        neulog_rate = '8'
                    elif self.combo_heart_rate_sample.currentText() == "5 per second":
                        neulog_rate = '9'
                    elif self.combo_heart_rate_sample.currentText() == "2 per second":
                        neulog_rate = '10'
                    elif self.combo_heart_rate_sample.currentText() == "1 per second":
                        neulog_rate = '11'
                else:
                    pass
            if neulog_used == True:
                # Obtain neulog parameters
                exp_params = str(self.tb_neulog_port.text()) + neulog_phys_params
                exp_params_list = exp_params.split(',')
                neu = Neulog(* exp_params_list)
                neu.exp_stop()
                neulog_samples = str(neulog_seconds * neulog_samples_mult)
                neulog_seconds_threading = int(neulog_seconds / 10)
                # Start neulog experiment
                neu.exp_start(neulog_rate,neulog_samples)
                t_phys_start = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.tb_phys_start_at.setText("Physiological data started at: " + t_phys_start)
                # Start thread to recover samples every 10 seconds
                thread1 = threading.Thread(target=self.thread_neulog, args=(neu,neulog_num_sensors,neulog_seconds_threading,))
                thread1.start()
            else:
                pass
        #& RESTART CODE
            self.CODE_REBOOT = -1234
            # If CODE_REBOOT is changed with the "stop session" button, it will break the trails loop
        #& SHOW INITIAL WHITE SCREEN
            while self.CODE_REBOOT == -1234:
                # Show white screen for the first 10 seconds, only once
                self.white_window()
                # Define counter of trials
                counter_trial = 0
                onset_duration = 0
                # Timer of 10 seconds
                loop = QEventLoop()
                # Obtain the int value of the spin box of first_screen, and multiply it for 1000 (1000 is 1 second)
                QTimer.singleShot((int(self.sb_first_screen.value())*1000), loop.quit) 
                loop.exec_()
                t_onset = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.tb_onset_at.setText("First trial started at: " + t_onset)
        #& START TRIAL
                # The number of trials is stated in the "click_start_function"
                for x in range (0,trials,1):
                    # If CODE_REBOOT is changed with the "stop session" button, it will break the trails loop
                    while self.CODE_REBOOT == -1234:
                #& DEFINE USED VARIABLES
                        # RNGs
                        psyleron = PsyREG()
                        pseudo = Pseudo_RNG()
                        # intervals and duration at 0
                        after_interval = 0
                        before_interval = 0
                        counter_trial += 1
                        trial_duration = 0
                        # obtain length of the string of the binary of the string of the after stimuli max interval
                        int_after_max_interval = int(self.sb_after_max_interval.value())
                        len_bin_after_max_interval = len(str(f'{int_after_max_interval:01b}'))
                        # obtain length of the string of the binary of the string of the after stimuli min interval
                        int_after_min_interval = int(self.sb_after_min_interval.value())
                        len_bin_after_min_interval = len(str(f'{int_after_min_interval:01b}'))
                        # obtain length of the string of the binary of the string of the before stimuli max interval
                        int_before_max_interval = int(self.sb_before_max_interval.value())
                        len_bin_before_max_interval = len(str(f'{int_before_max_interval:01b}'))
                        # obtain length of the string of the binary of the string of the before stimuli min interval
                        int_before_min_interval = int(self.sb_before_min_interval.value())
                        len_bin_before_min_interval = len(str(f'{int_before_min_interval:01b}'))
                        # Add neutral and excitatory image lists
                        self.image_list = self.image_list_neutral + self.image_list_excitatory
                        self.image_list_filenames = self.image_list_neutral_filenames + self.image_list_excitatory_filenames
                        # obtain length of neutral, excitatory, and total image_list_filenames and obtain its binary length
                        self.len_image_list_neutral = len(self.image_list_neutral_filenames)
                        self.len_image_list_excitatory = len(self.image_list_excitatory_filenames)
                        len_image_list = len(self.image_list_filenames)
                        len_bin_image_list = len(str(f'{len_image_list:01b}'))
                        # establish variables that will force the first loop to obtain RNG bits from rng_get_image and rng_get_bits
                        int_after_bits = int_after_max_interval + 1
                        int_before_bits = int_before_max_interval + 1
                        image_bits = len_image_list + 1
                        # establish the constant duration of each trial adding the pre_stimuls screen duration, the stimulus duration, and post_stimulus screen duration
                        trial_dur_constant = int(self.sb_pre_screen.value() + self.sb_stim_duration.value() + self.sb_post_screen.value())
                        t_s = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                        self.tb_time_start_trial.append(t_s)
                        self.tb_trial_id.append("n" + str(counter_trial))
                #& ADDITIONAL ON DEMAND PROCEDURE
                        if counter_trial >= 2:
                            # Validate if session is On-demand or free-running
                            if self.combo_trial_type.currentText() == "On-Demand":
                                # Minimize main screen
                                self.showMinimized()
                                # Show button for starting the next trial
                                butt_demand = QMessageBox.question(self, "On-Demand: Trial Ended", "Please click 'Ok' to start the next trial.", QMessageBox.Ok | QMessageBox.Abort)
                                if butt_demand == QMessageBox.Abort:
                                    self.butt_stop.click()
                                    break
                                elif butt_demand == QMessageBox.Ok:
                                    pass
                                else:
                                    pass
                                    #& ADD BEFORE STIMULI INTERVAL
                                if str(psyleron.get_name()) == self.combo_rng_sources.currentText():
                                    if psyleron.count_PsyREGs() >= 1:
                                        # Gets random interval from RNG giving the input 1) type of RNG, 2) max interval + 1, 
                                            # 3)min interval, 4) length of binary min interval, 
                                            # 5) max interval, and 6) length of binary max interval
                                        before_interval_1000 = self.rng_get_bits(psyleron, int_before_bits, int_before_min_interval, len_bin_before_min_interval, int_before_max_interval, len_bin_before_max_interval)
                                        before_interval = before_interval_1000 / 1000
                                        # Clear and realease psyleron
                                        psyleron.clear_RNG()
                                        psyleron.release_RNG()
                                    else:
                                        QMessageBox.about(self, "ERROR", "Psyleron didn't send bits")
                            # Check if Pseudo-RNG is being used
                                elif pseudo.name == self.combo_rng_sources.currentText():
                                    # Gets random interval from RNG giving the input 1) type of RNG, 2) max interval + 1, 
                                        # 3)min interval, 4) length of binary min interval, 
                                        # 5) max interval, and 6) length of binary max interval
                                    before_interval_1000 = self.rng_get_bits(pseudo, int_before_bits, int_before_min_interval, len_bin_before_min_interval, int_before_max_interval, len_bin_before_max_interval)
                                    before_interval = before_interval_1000 / 1000
                                else:
                                    QMessageBox.about(self, "ERROR", "Unexpected RNG error.")
                            # Timer-wait according to random interval
                                loop = QEventLoop()
                                QTimer.singleShot(before_interval_1000, loop.quit)
                                loop.exec_()
                            else: #Free-Running
                                pass
                        else: # counter_trial <= 1
                            pass
                #& WHITE SCREEN FOR SB_PRE-SCREEN secs (default = 3)
                        # It doesn't show anything, as the white screen is still showing since SHOW WHITE SCREEN            
                        # Timer of 3 seconds
                        loop = QEventLoop()
                        # Obtain the int value of the spin box of pre_screen, and multiply it for 1000 (1000 is 1 second)
                        QTimer.singleShot((int(self.sb_pre_screen.value())*1000), loop.quit)
                        loop.exec_()
                #& SHOW IMAGE FOR SB_IMAGE secs (default = 3)
                        # Selects randomly the image to show, and displays it for 3 seconds
                        # Check if Psyleron is being used
                        if str(psyleron.get_name()) == self.combo_rng_sources.currentText():
                            if psyleron.count_PsyREGs() >= 1:
                                # Gets random image from RNG giving the input 1) type of RNG, 2) length of image list + 1, 
                                        # 3) length of image list, and 4) length of the binary length of image list
                                self.rng_get_image(psyleron, image_bits, len_image_list, len_bin_image_list)
                                # Clear and release Psyleron
                                psyleron.clear_RNG()
                                psyleron.release_RNG()
                            else:
                                QMessageBox.about(self, "ERROR", "Psyleron didn't send bits")
                            # Check if Pseudo-RNG is being used
                        elif pseudo.name == self.combo_rng_sources.currentText():
                                # Gets random image from RNG giving the input 1) type of RNG, 2) length of image list + 1, 
                                        # 3) length of image list, and 4) length of the binary length of image list
                                self.rng_get_image(pseudo, image_bits, len_image_list, len_bin_image_list)
                        else:
                            QMessageBox.about(self, "ERROR", "No RNG selected. Closing app...")
                        # Timer of 3 seconds
                        loop = QEventLoop()
                        # Obtain the int value of the spin box of img_duration, and multiply it for 1000 (1000 is 1 second)
                        QTimer.singleShot((int(self.sb_stim_duration.value())*1000), loop.quit)
                        loop.exec_()
                        # Close image
                        self.image_w.close()
                #& WHITE SCEEN FOR SB_POST-SCREEN secs (default = 9)
                        # Timer of 9 seconds
                        loop = QEventLoop()
                        # Obtain the int value of the spin box of post_screen, and multiply it for 1000 (1000 is 1 second)
                        QTimer.singleShot((int(self.sb_post_screen.value())*1000), loop.quit)
                        loop.exec_()
                #& SESSION FINISHED?
                        # Check if all trails have happened (session over)
                        if counter_trial >= trials:
                            # Close white screen
                            self.white_w.close()
                            # Add the before stimulus interval of last trial
                            self.tb_dur_before_interval.append(str(int(before_interval)))
                            # Add a "0" string to the intervals, as last trial doesn't have interval
                            self.tb_dur_after_interval.append("0")
                            # Add the final onset duration
                            onset_duration += (trial_dur_constant + before_interval)
                            self.tb_onset_to_trial.append(str(int(onset_duration)))
                            # Add the final onset duration
                            trial_duration += (trial_dur_constant + before_interval)
                            self.tb_seconds_end_trial.append(str(int(trial_duration)))
                            # Add the datastamp at the end of that trial
                            t_f = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                            self.tb_time_end_trial.append(t_f)
                            # Add the datastamp for the end of the session
                            t_ff = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                            self.tb_finish_at.setText("Session finished at: " + t_ff)
                            # stop code
                            self.CODE_REBOOT = 1
                        #& PHYSIOLOGICAL DATA
                            # Validate if neulog us being used
                            if neulog_used == True:
                                # Obtain experiment values from Neulog server
                                sensor_lists = neu.get_exp_values()
                                sensor_list_index = 0
                                # Obtain each list in the lists in the Neulog server
                                for sensor_list in sensor_lists:
                                    # Obtain the lapse of miliseconds between values of each sample
                                    neulog_samples_mils = (1000/int(neulog_samples_mult))
                                    t_phys_start_next = t_phys_start
                                    # Obatain the values for each list
                                    for sample in sensor_list:
                                        if sensor_list_index == 0:
                                            # Append the sensor value to the textbox
                                            self.tb_skin_conductance_values.append(str(float(sample)))
                                            # Obtain the timestamp corresponding to each value
                                            t_phys_start_next = datetime.strptime(t_phys_start_next,'%H:%M:%S.%f')
                                            t_phys_start_next = t_phys_start_next + timedelta(milliseconds = neulog_samples_mils)
                                            t_phys_start_next = t_phys_start_next.strftime('%H:%M:%S.%f')[:-3]
                                            self.tb_skin_conductance_timestamp.append(str(t_phys_start_next))
                                        elif sensor_list_index == 1:
                                            # Append the sensor value to the textbox
                                            self.tb_heart_rate_values.append(str(float(sample)))
                                            # Obtain the timestamp corresponding to each value
                                            t_phys_start_next = datetime.strptime(t_phys_start_next,'%H:%M:%S.%f')
                                            t_phys_start_next = t_phys_start_next + timedelta(milliseconds = neulog_samples_mils)
                                            t_phys_start_next = t_phys_start_next.strftime('%H:%M:%S.%f')[:-3]
                                            self.tb_heart_rate_timestamp.append(str(t_phys_start_next))
                                        sample += 1
                                    sensor_list_index += 1
                                # Stop neulog experiment in server
                                neu.exp_stop()
                                # Register physical data ending time
                                t_ff = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                                self.tb_phys_finish_at.setText("Physiological data finished at: " + t_ff)
                            # Validate if other physiological hardware is being used: #!
                            elif neulog_used == False:
                                pass
                        #& ERASE DATA PRE-FIRST TRIAL STARTED
                            if self.cb_skin_conductance.isChecked():
                                self.delete_unused_phys_data(self.tb_onset_at,self.tb_finish_at,self.tb_skin_conductance_timestamp,self.tb_skin_conductance_values)
                            if self.cb_heart_rate.isChecked():
                                self.delete_unused_phys_data(self.tb_onset_at,self.tb_finish_at,self.tb_heart_rate_timestamp,self.tb_heart_rate_values)
                            if self.cb_brainwaves.isChecked():
                                self.delete_unused_phys_data(self.tb_onset_at,self.tb_finish_at,self.tb_brainwaves_timestamp,self.tb_brainwaves_values)
                        #& ADD TRIAL ID
                            if self.cb_skin_conductance.isChecked():
                                self.create_phys_ids(self.tb_trial_id,self.tb_time_start_trial,self.tb_time_end_trial,self.tb_skin_conductance_timestamp,self.tb_phys_trial_id,self.tb_phys_instance_id)
                            elif self.cb_heart_rate.isChecked():
                                self.create_phys_ids(self.tb_trial_id,self.tb_time_start_trial,self.tb_time_end_trial,self.tb_heart_rate_timestamp,self.tb_phys_trial_id,self.tb_phys_instance_id)
                            elif self.cb_brainwaves.isChecked():
                                self.create_phys_ids(self.tb_trial_id,self.tb_time_start_trial,self.tb_time_end_trial,self.tb_brainwaves_timestamp,self.tb_phys_trial_id,self.tb_phys_instance_id)
                        #& CALCULATE MEDIA, SD, Z, f and Fn
                            if neulog_used == True:
                                phys_sample_rate = neulog_samples_mult
                                self.presentiment_instances = phys_sample_rate * int(self.sb_pre_screen.text())
                            elif neulog_used == False: #!
                                pass
                            if self.cb_skin_conductance.isChecked():
                                self.calculate_media_sd_Z_f_Fn(self.presentiment_instances,self.tb_trial_id,self.tb_skin_conductance_values,self.tb_phys_trial_id,self.tb_phys_instance_id,self.tb_skin_conductance_media,self.tb_skin_conductance_sd,self.tb_skin_conductance_Z,self.tb_skin_conductance_f,self.tb_skin_conductance_Fn)
                            if self.cb_heart_rate.isChecked():
                                self.calculate_media_sd_Z_f_Fn(self.presentiment_instances,self.tb_trial_id,self.tb_heart_rate_values,self.tb_phys_trial_id,self.tb_phys_instance_id,self.tb_heart_rate_media,self.tb_heart_rate_sd,self.tb_heart_rate_Z,self.tb_heart_rate_f,self.tb_heart_rate_Fn)
                            if self.cb_brainwaves.isChecked():
                                self.calculate_media_sd_Z_f_Fn(self.presentiment_instances,self.tb_trial_id,self.tb_brainwaves_values,self.tb_phys_trial_id,self.tb_phys_instance_id,self.tb_brainwaves_media,self.tb_brainwaves_sd,self.tb_brainwaves_Z,self.tb_brainwaves_f,self.tb_brainwaves_Fn)
                        #& CALCULATE D AND ZD
                            if self.cb_skin_conductance.isChecked():
                                self.calculate_D_Z(self.tb_stimulus_id,self.tb_skin_conductance_Fn, self.tb_skin_conductance_D,self.tb_skin_conductance_ZD)
                            if self.cb_heart_rate.isChecked():
                                self.calculate_D_Z(self.tb_stimulus_id,self.tb_heart_rate_Fn, self.tb_heart_rate_D,self.tb_heart_rate_ZD)
                            if self.cb_brainwaves.isChecked():
                                self.calculate_D_Z(self.tb_stimulus_id,self.tb_brainwaves_Fn, self.tb_brainwaves_D,self.tb_brainwaves_ZD)
                        #& ENDING MESSAGE
                            # Show message stating the end of the session
                            QMessageBox.about(self, "FINAL", "The session has finished. Thanks for your participation.")
                #& ADD EXTRA INTERVAL 0-5s 
                        else:
                        # Check if Psyerlon is being used
                            if str(psyleron.get_name()) == self.combo_rng_sources.currentText():
                                if psyleron.count_PsyREGs() >= 1:
                                    # Gets random interval from RNG giving the input 1) type of RNG, 2) max interval + 1, 
                                        # 3)min interval, 4) length of binary min interval, 
                                        # 5) max interval, and 6) length of binary max interval
                                    after_interval_1000 = self.rng_get_bits(psyleron, int_after_bits, int_after_min_interval, len_bin_after_min_interval, int_after_max_interval, len_bin_after_max_interval)
                                    after_interval = after_interval_1000 / 1000
                                    # Clear and realease psyleron
                                    psyleron.clear_RNG()
                                    psyleron.release_RNG()
                                else:
                                    QMessageBox.about(self, "ERROR", "Psyleron didn't send bits")
                        # Check if Pseudo-RNG is being used
                            elif pseudo.name == self.combo_rng_sources.currentText():
                                    # Gets random interval from RNG giving the input 1) type of RNG, 2) max interval + 1, 
                                        # 3)min interval, 4) length of binary min interval, 
                                        # 5) max interval, and 6) length of binary max interval
                                    after_interval_1000 = self.rng_get_bits(pseudo, int_after_bits, int_after_min_interval, len_bin_after_min_interval, int_after_max_interval, len_bin_after_max_interval)
                                    after_interval = after_interval_1000 / 1000
                            else:
                                QMessageBox.about(self, "ERROR", "Unexpected RNG error.")
                        # Timer-wait according to random interval
                            loop = QEventLoop()
                            QTimer.singleShot(after_interval_1000, loop.quit)
                            loop.exec_()
                #& ADD SESSION DATA
                        # Add the interval, duration, onset time, and end time of trial
                            self.tb_dur_before_interval.append(str(int(before_interval)))
                            self.tb_dur_after_interval.append(str(int(after_interval)))
                            onset_duration += (trial_dur_constant + before_interval + after_interval)
                            self.tb_onset_to_trial.append(str(int(onset_duration)))
                            trial_duration += (trial_dur_constant + before_interval + after_interval)
                            self.tb_seconds_end_trial.append(str(int(trial_duration)))
                            t_f = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                            self.tb_time_end_trial.append(t_f)
                    else: # Reboot
                        QMessageBox.about(self, "TRIAL STOPPED", "TRIAL stopped, wait until SESSION has stopped.")
                        break
            else: # Reboot
                QMessageBox.about(self, "SESSION STOPPED", "SESSION has stopped, wait for further instructions. Clear Session Data before next session.")

#########################

if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Create_Window()
        window.show()
        sys.exit(app.exec_())
        