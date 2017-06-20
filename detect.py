# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:37:58 2017

@author: C.E
"""

import numpy as np
from IntegralImage import *
import time
from time import strftime
import os
import highlight
import sys
import utils

def debug(message):
    sys.stdout.write(message)
    sys.stdout.flush()
    
def scan():
    
    step = 1.5
    scale = 1.25
    width = 24
    height = 24
    
    cascade=utils.readFile('../result/20170616015311_/cascade.txt')
    faces=[]
    imagePath='../../BaoDataBase/myDataBase/1.jpg'
    iimage=IntegralImage(imagePath,1)
    iWidth=iimage.original.shape[1]
    iHeight=iimage.original.shape[0]
    curScale=1.0
    
    detect_folder='../result/'+strftime("%Y%m%d-%H%M%S", time.localtime()).replace('-','')+'/'
    os.makedirs(os.path.dirname(detect_folder), exist_ok=True)
    
    debug('{0} : {1}\n'.format(iWidth,iHeight))
    count =0
    while width < iWidth and height < iHeight:
         for x in range(0,np.int(iWidth-width),np.int(np.ceil(step*scale))):
             for y in range (0,np.int(iHeight-height),np.int(np.ceil(step*scale))):
                print('x : y = {0} : {1}'.format(x,y))
                #print('width : height = {0} : {1}'.format(width,height))
                pred = cascade.predict_with_scale(iimage,(x,y),curScale)
                
                
                '''
                #iimage.image.show()
                if count % 1 ==0:
                    copy=iimage.image.copy()
                    highlight.drawSquare(copy,[(x,y),(int(x+width),int(y+height))])
                    copy.save(os.path.join(detect_folder,str(count)+'.jpg'))
                count += 1
                '''
                '''
                pred = cascade.predict_with_scale(iimage,(x,y),curScale)
                if pred == 1:
                    sub = iimage.image.crop((x,y,int(x+width),int(y+height)))
                    sub.save(os.path.join(detect_folder,str(count)+'.jpg'))
                    count += 1
                '''
                
         width *= scale
         height *= scale
         curScale *=scale