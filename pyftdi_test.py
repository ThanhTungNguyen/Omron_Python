#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:42:44 2017

@author: nagoyacoi
"""

from pyftdi.ftdi import Ftdi
import numpy as np
import cv2
import pygame
import time

# Pygame init
pygame.init()

size = width, height = 752, 480
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ls = [(0x0403, 0x6014)]

datasize = 16+752*480+752+16
ret = Ftdi()
print(ret.find_all(ls))

ret.open(1027, 24596)
ret.set_bitmode(0xff, 0)
time.sleep(1)

ret.set_bitmode(0xff, 0x40)
ret.set_latency_timer(2)
ret.read_data_set_chunksize(65536)
ret.write_data_set_chunksize(65536)
ret.set_flowctrl('hw')
try:
    ret.write_data(b'S')
except ValueError:
    print('Cannot write')


stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                stop = True
        
    result = b''
    frame_ = False
    while not frame_:
        res = ret.read_data(65536)
        if res!=b'':
            result += res
            print(res)
            if len(result) >= datasize:
                frame_ = True
        
    result = result[:361744]
    #print(len(result))
    result = result[16:-(16+752)]
    #print(len(result))
    np_im = np.fromstring(result, dtype=np.uint8).reshape((752, 480))

    img = cv2.cvtColor(np_im, cv2.COLOR_GRAY2BGR)
    img = np.rot90(img)

    pyimg = pygame.surfarray.make_surface(img)
    screen.blit(pyimg, (0, 0))
    pygame.display.flip()
    
ret.write_data(b'P')
ret.close()

#pygame.quit()

#print(len(result))