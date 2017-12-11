# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 14:39:11 2017

@author: Nguyen Thanh Tung
"""

import cv2
import pygame
import numpy as np
import time
from OmronCamera import OmronCameraFrame

filename = 'F:\\20171115_162615.bin'

# Pygame init
pygame.init()

size = width, height = 752, 480

head_size = 16
foot_size = 16
base_size = 752*480
info_size = 752
pakage = head_size + base_size + info_size + foot_size

screen = pygame.display.set_mode(size)

font = cv2.FONT_HERSHEY_DUPLEX

def convert_uint(byte):
    return int.from_bytes(byte, byteorder='little')

with open(filename, 'rb') as f:
    #f.seek(15000*pakage)
    for i in range(10000):
        # Extract data
        event = pygame.event.get() # Call event for preventing pygame not responding
        
        byte = f.read(pakage)
        if len(byte) == 0:
            break
        
        # Extract data with OmronCameraFrame module
        OmronFrame = OmronCameraFrame(byte)
        OmronFrame.FrameInfo()
        
        frame = OmronFrame.data
        frameid = OmronFrame.frameId
        face_w = OmronFrame.dtWidth
        face_h = OmronFrame.dtHeight
        face_x = OmronFrame.dtPx
        face_y = OmronFrame.dtPy
        
        # Update Screen        
        screen.fill([0,0,0])
        np_im = np.fromstring(frame, np.uint8).reshape((480, 752))
        img = cv2.cvtColor(np_im, cv2.COLOR_GRAY2BGR)
        
        cv2.putText(img, str(frameid), (20, 470), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if ((face_w!=0)&(face_h!=0)):
            cv2.putText(img, str(face_x), (20, 30), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img, str(face_y), (20, 60), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.rectangle(img, (752-(face_y-int(face_h/2)), (face_x-int(face_w/2))), (752-(face_y+int(face_h/2)), (face_x+int(face_w/2))), (0, 0, 255), 2)
            #cv2.circle(img, (face_y, face_x), 10, (0,0,255), 2)
        img = np.rot90(img)
        img = cv2.flip(img, 0)
        #img = flip_frame
        pyframe = pygame.surfarray.make_surface(img)
        
        screen.blit(pyframe, (0,0))
        pygame.display.update()
        img = None
        
        pygame.time.delay(30) # Pause for 30 ms ~ 30 fps
    f.close()
    
pygame.quit()