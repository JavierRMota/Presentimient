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
import random

class Pseudo_RNG():
    def __init__(self):  
        self.name = "Pseudo-RNG"

    # @params maxbts: Number of bits to generate
    # @returns Generated bits
    def get_bits(self, maxbts):
        str_list = []
        for _ in range(maxbts):
            str_list.append(random.randrange(0,2))
        str_bits = ''.join(str(x) for x in str_list)
        return str_bits