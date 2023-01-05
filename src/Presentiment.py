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
import sys

#? Includes from external modules in Pipfile
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication

#? Includes from this project
from UI import Create_Window

#$ List of missing features
# TODO: Design - Add image from experimental design
# TODO: Design - Add Z0 a Phys Data on the side of Trial e Instances
# TODO: Design - Add info
# TODO: Design - Add manual
# TODO: Design - Adapt exports
#! TODO: Fatal errors - Don't close if RNG is not selected
#! TODO: Fatal errors - Don't close if error at exporting
#! TODO: Fatal errors - Don't close if statistical analysis can't be realized
#! TODO: Fatal errors - Don't close if no library is selected
#! TODO: Fatal errors - Alert if no image has been chosen
#! TODO: Fatal errors - Don't close if there is no port for Neulog
#! TODO: Fatal errors - Fully test for other cases
# TODO: Avoid different sample rates between Neulogs (it breaks)
# TODO: Solve ondemand procedure, will break sample calculated for neulog
# TODO: Compile using auto-py-to-exe
#& Low Priority
# TODO: Add Opened, GetBits, GetBytes and APIVersion to PsyREG class
# TODO: Include FOR loop for each psyleron connected on "click_refresh_sources"
# TODO: Add dimensions of analysis (ex. Fear[Dead-Danger, Animals-Injuries, etc.])
#& Wishlist
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

if __name__ == '__main__':
        load_dotenv()
        app = QApplication(sys.argv)
        window = Create_Window()
        window.show()
        sys.exit(app.exec_())