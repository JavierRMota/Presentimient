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

from . import Neulog
from . import PsyREG
from . import Pseudo_RNG

def refresh_neulog(port, onNeulogReady,onNeulogExperiment, onNeulogFailed):
    # Create neulog class
    neu = Neulog(port)
    # Check the status of the Neulog server
    status = neu.get_status()
    # If server is ready, clear combos, add "neulog" and message "Ready"
    if status == 'Neulog API status: Ready':
        onNeulogReady(neu.name)
    # If server is in experiment, stop experiment and message "stopping experiment"
    elif status == 'Neulog API status: Experiment':
        onNeulogExperiment()
        neu.exp_stop()
    else:
        onNeulogFailed()

def skin_conductance_test(port, name, onGetNeulogValue):
    # Create neulog class with GSR sensor
    neu = Neulog(port, 'GSR')
    # Set GSR sensor range to miliSiemens
    neu.set_sensor_range('2')
    # if neulog is selected...
    if neu.name == name:
        # Obtain values
        onGetNeulogValue(str(neu.get_values()[0]))
    else:
        pass

def heart_rate_test(port, name, onGetNeulogValue):
    # Create neulog class with Pulse sensor
    neu = Neulog(port, 'Pulse')
    neu.set_sensor_range('1')
     # if neulog is selected...
    if neu.name == name:
        # Obtain values
        onGetNeulogValue(str(neu.get_values()[0]))
    else:
        pass

# @returns True if Psyleron matches the name, False otherwise
def maybe_generate_psyleron_bits(name, onSuccess,onFailure):
    psyleron = PsyREG()
    if str(psyleron.get_name()) == name:
        if psyleron.count_PsyREGs() >= 1:
            onSuccess(psyleron.get_bits(6))
            psyleron.clear_RNG()
            psyleron.release_RNG()
        else:
            onFailure()
        return True
    return False

#? Function behaves different than the one above, in this case failure is when it is not selected
def maybe_generate_pseudo_RNG_bits(name, onSuccess, onFailure):
    pseudo = Pseudo_RNG()
    if pseudo.name == name:
        onSuccess(pseudo.get_bits(6))
    else:
        onFailure()