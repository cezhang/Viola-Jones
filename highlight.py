# -*- coding: utf-8 -*-
"""
Created on Sun May 28 14:57:41 2017

@author: C.E
"""

#import PIL
from PIL import ImageDraw
#import ImageDraw
from HaarLikeFeature import FeatureType
#from time import strftime
#import time


def highlight(feature, image):
    draw=ImageDraw.Draw(image)
    if feature.type == FeatureType.TWO_VERTICAL:
        first = [feature.top_left, (feature.top_left[0] + feature.width, feature.top_left[1] + feature.height/2)]
        drawRectWhite(draw,first)
        second = [(feature.top_left[0], feature.top_left[1] + feature.height/2), feature.bottom_right]
        drawRectBlack(draw,second)
    elif feature.type == FeatureType.TWO_HORIZONTAL:
        first = [feature.top_left, (feature.top_left[0] + feature.width/2, feature.top_left[1] + feature.height)]
        drawRectWhite(draw,first)   
        second = [(feature.top_left[0] + feature.width/2, feature.top_left[1]), feature.bottom_right]
        drawRectBlack(draw,second)
    elif feature.type == FeatureType.THREE_HORIZONTAL:
        first = [feature.top_left, (feature.top_left[0] + feature.width/3, feature.top_left[1] + feature.height)]
        drawRectWhite(draw,first)  
        second = [(feature.top_left[0] + feature.width/3, feature.top_left[1]), (feature.top_left[0] + 2*feature.width/3, feature.top_left[1] + feature.height)]
        drawRectBlack(draw,second)
        third = [(feature.top_left[0] + 2*feature.width/3, feature.top_left[1]), feature.bottom_right]
        drawRectWhite(draw,third)
    elif feature.type == FeatureType.THREE_VERTICAL:
        first = [feature.top_left, (feature.bottom_right[0], feature.top_left[1] + feature.height/3)]
        drawRectWhite(draw,first) 
        second = [(feature.top_left[0], feature.top_left[1]+ feature.height/3), (feature.bottom_right[0], feature.top_left[1] + 2*feature.height/3)]
        drawRectBlack(draw,second)         
        third = [(feature.top_left[0], feature.top_left[1] + 2*feature.height/3), feature.bottom_right]
        drawRectWhite(draw,third)
    elif feature.type == FeatureType.FOUR:
        first = [feature.top_left, (feature.top_left[0] + feature.width/2, feature.top_left[1] + feature.height/2)]
        drawRectWhite(draw,first)       
        second = [(feature.top_left[0] + feature.width/2, feature.top_left[1]), (feature.bottom_right[0], feature.top_left[1] + feature.height/2)]
        drawRectBlack(draw,second)          
        third = [(feature.top_left[0], feature.top_left[1] + feature.height/2), (feature.top_left[0] + feature.width/2, feature.bottom_right[1])]
        drawRectBlack(draw,third)        
        fourth = [(feature.top_left[0] + feature.width/2, feature.top_left[1] + feature.height/2), feature.bottom_right]
        drawRectWhite(draw,fourth)  
    
    del draw
    
def drawRectWhite(draw,coordiantes):
    draw.rectangle(coordiantes,fill=255)

def drawRectBlack(draw,coordinates):
    draw.rectangle(coordinates,fill=0)
    
def drawSquare(image,cor):
    draw=ImageDraw.Draw(image)
    draw.rectangle(cor,fill=255)