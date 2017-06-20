# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 14:19:32 2017

@author: C.E
"""

import os 
import IntegralImage
import sys

def load_images(path, label):
    images = []
    for _file in os.listdir(path):
        if _file.endswith('.jpg') or _file.endswith('.pgm'):
            #print(_file)
            images.append(IntegralImage.IntegralImage(os.path.join(path, _file), label))
            
    return images
    
def writeOut(cascade,file):
    
    os.makedirs(os.path.dirname(file), exist_ok=True)
    #import json
    with open(file,'wb') as f:
        import pickle
        pickle.dump(cascade,f)
    '''    
    for c in classifiers:
        file.write(str(c[1])+'\n')
        file.write(json.dumps(c[0].__dict__)+"\n")
    file.close()
    '''
        

def readFile(file):
    import pickle
    with open(file,'rb') as f:
        obj=pickle.load(f)  

    return obj
    
def debug(message):
    sys.stdout.write(message)
    sys.stdout.flush()
    
def log(message,context):
    pass