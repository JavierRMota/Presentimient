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
import ctypes
#? Includes from this project
from .PsyREGFinder import PsyREGPath

class PsyREG():
    def __init__(self):  
        #? Define path of DLL
        self.path_REG_dll = PsyREGPath()
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

        