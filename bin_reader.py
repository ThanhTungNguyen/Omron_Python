# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 14:39:11 2017

@author: Nguyen Thanh Tung
"""

import cv2
import pygame
import numpy as np
import time

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
    f.seek(15000*pakage)
    
    for i in range(10000):
        # Extract data
        byte = f.read(head_size+base_size+info_size+foot_size)
        if len(byte) == 0:
            break
        frame = byte[head_size:-(info_size+foot_size)]
        #print(len(frame))
        info = byte[head_size+base_size:-foot_size]
        
        # Parameters
        frameid = convert_uint(info[:7])
        soft_ver = info[8:129]
        face_w = convert_uint(info[130:131])
        face_h = convert_uint(info[132:133])
        face_x = convert_uint(info[140:141])
        face_y = convert_uint(info[142:143])
        
        # Update Screen        
        screen.fill([0,0,0])
        np_im = np.fromstring(frame, np.uint8).reshape((480, 752))
        img = cv2.cvtColor(np_im, cv2.COLOR_GRAY2BGR)
        
        #print(img.shape)
        #img = cv2.flip(img, 0)
        #img = cv2.flip(img, 0)
        cv2.putText(img, str(frameid), (20, 470), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if ((face_w!=0)&(face_h!=0)):
            cv2.putText(img, str(face_x), (20, 30), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img, str(face_y), (20, 60), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            #cv2.rectangle(img, (752-(face_y-int(face_h/2)), (face_x-int(face_w/2))), (752-(face_y+int(face_h/2)), (face_x+int(face_w/2))), (0, 0, 255), 2)
            cv2.circle(img, (face_y, face_x), 10, (0,0,255), 2)
        img = np.rot90(img)
        img = cv2.flip(img, 0)
        #img = flip_frame
        pyframe = pygame.surfarray.make_surface(img)
        
        screen.blit(pyframe, (0,0))
        pygame.display.update()
        #time.sleep(1)
    f.close()
    
pygame.quit()

        
    