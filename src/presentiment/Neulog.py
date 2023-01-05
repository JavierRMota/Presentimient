# -*- coding: utf-8 -*-
"""
Copyright (c) 2022-2023 Alejandro Ramsés D'León.

This file is part of Presentiment Project.
See https://github.com/Ramses-Dleon/Presentimiento for further info.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

#? Includes from built in Python
import json
import datetime

#? Includes from external modules in Pipfile
import requests


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