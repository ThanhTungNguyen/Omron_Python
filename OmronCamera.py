# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 21:45:01 2017

@author: ThanhTung
"""

class OmronCameraFrame:
    def __init__(self, datain):
        self.datain = datain
        # Frame structure
        self._header_size = 16
        self._footer_size = 16
        self._data_size = 752*480
        self._info_size = 752
        self._frame_size = self._header_size + self._data_size + self._info_size + self._footer_size
    
    # Convert byte to integer
    def convert_uint(self, byte):
        return int.from_bytes(byte, byteorder='little')

    # Read & Extract frame
    def FrameInfo(self):
        try:
            if len(self.datain)!= self._frame_size:
                raise ValueError('Data size not right! Return none...')
        except ValueError:
            return -1
        
        # Extract data & info
        self.data = self.datain[self._header_size:(self._header_size+self._data_size)]
        self.info = self.datain[(self._header_size+self._data_size):(-self._footer_size)]
        
        # Extract information from frame
        self.frameId = self.convert_uint(self.info[:7])
        self.softVer = self.convert_uint(self.info[8:129])
        self.dtWidth = self.convert_uint(self.info[130:131])
        self.dtHeight = self.convert_uint(self.info[132:133])
        self.dtPx = self.convert_uint(self.info[140:141])
        self.dtPy = self.convert_uint(self.info[142:143])
        self.ptRoll = self.convert_uint(self.info[232:233])
        self.ptYaw = self.convert_uint(self.info[234:235])
        self.ptPitch = self.convert_uint(self.info[236:237])
        self.gbYaw = self.convert_uint(self.info[256:257])
        self.gbPitch = self.convert_uint(self.info[258:259])
        self.gbOpenL = self.convert_uint(self.info[260:261])
        self.gbOpenR = self.convert_uint(self.info[262:263])
        self.model = 3
        
        return 0
        
        