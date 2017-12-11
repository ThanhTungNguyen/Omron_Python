#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:59:52 2017

@author: icce
"""

from pylibftdi.device import Device
from pylibftdi.serial_device import SerialDevice

d = Device()
d.open()

d.write('S')
for i in range(100):
  try:
      ret = d.read(65536)
      print(i, ret)
  except ValueError:
      print('Error')
      continue

d.write('P')
d.close()