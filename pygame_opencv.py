# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 21:51:05 2017

@author: ThanhTung
"""

import cv2
import pygame
import numpy as np
import socket
from datetime import datetime

# Get IP
'''
try:
    IPaddr = socket.gethostbyname(socket.gethostname())
except ValueError:
    IPaddr = 'None'
'''
IPaddr = 'None'
print(IPaddr)

# Pygame init
pygame.init()

size = width, height = 1024, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("IMG.jpg")

# Get camera
cap = cv2.VideoCapture(0)

# Get Font
font = cv2.FONT_HERSHEY_DUPLEX

exit_ = False
while not exit_:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_ = True

    ret, frame = cap.read()
    now = str(datetime.now())
    #print(now)
    #screen.fill(black)
    screen.fill([0,0,0])
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (1024, 600))
    flip_frame = cv2.flip(frame, 1)
    
    cv2.putText(flip_frame, IPaddr, (20, 30), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(flip_frame, now, (20, 60), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    frame = cv2.flip(flip_frame, 1)
    
    frame = np.rot90(frame)    
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    pygame.display.flip()
    
pygame.quit()
cap.release()
cv2.destroyAllWindows()