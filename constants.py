# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:38:47 2017

@author: C.E
"""
import math


FACE_LABEL=1
NON_FACE_LABEL=0

F=0.5
D=0.99
Ftarget=math.pow(10,-6)


#FACES_PATH='../dataset/trainf'
#NON_FACES_PATH='../dataset/trainnf'
FACES_PATH='../dataset/train/face'
NON_FACES_PATH='../dataset/train/non-face'

IMAGE_SIDE=int(19)