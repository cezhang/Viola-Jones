# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 11:23:02 2017

@author: C.E
"""

import numpy as np
import trainAdaboost
#import utils
from AdaboostClassifier import AdaboostClassifier
from CascadeClassifier import CascadeClassifier
import logging

logger = logging.getLogger(__name__)

def updateDataset(data,cascade):
    pos = []
    neg = []
    for image in data:
        if image.label == 0:
            if cascade.predict(image) == 1:
                neg.append(image)
        if image.label == 1 :
            if cascade.predict(image) ==1 :
                pos.append(image)
                
    return pos,neg
  
def initial_normalize_weight(posData, negData):
    pos_weight = 1. / (2 * len(posData))
    neg_weight = 1. / (2 * len(negData))
    for p in posData:
        p.set_weight(pos_weight)
    for n in negData:
        n.set_weight(neg_weight)
        
def train(F,D, Ftarget,posData, negData,features):
    
    cascade = CascadeClassifier()
    
    initial_normalize_weight(posData,negData)
    
    while cascade.overallFPR() > Ftarget :
        
        images=np.hstack((posData,negData))
        np.random.shuffle(images)        
        
        '''
        sizeP=posData.shape[0]
        sizeN=negData.shape[0]
        trainP=posData[:np.ceil(0.7*sizeP)]
        testP=posData[np.ceil(0.7*sizeP):]
        trainN=negData[:np.ceil(0.7*sizeN)]
        testN=negData[np.ceil(0.7*sizeN):]
        '''
        
        ada=AdaboostClassifier()
        cascade.addAdaboostClassifier(ada)
        
        logger.info("< Start training {0}th layer ... >".format(len(cascade.adaboostClassifiers)))
        
        while cascade.currentFPR() > F * cascade.prevFPR() :
            weakClassifier=trainAdaboost.trainAdaboostClassifier(images,features)
            ada.addWeakClassifier(weakClassifier)          
            cascade.evaluate(images)
            
            ########
            logger.info("< Fnish training a weak classifier ({0}) ... >".format(len(ada.weakClassifiers)))
            logger.info("< alpha : {0} ,\n feature : {1} ".format(weakClassifier[0],weakClassifier[1]))
            logger.info("< overallFPR : {0} , currentFPR : {1} , currentDR : {2} , prevFPR : {3} >".format(cascade.overallFPR(),cascade.currentFPR(),cascade.currentDR(),cascade.prevFPR()))            
            ########      
            
            while cascade.currentDR() < D * cascade.prevDR():
                ada.decreaseThreshold()
                cascade.evaluate(images)
                ########
                logger.info("< Ajusting detection rate ... >")
                logger.info("< overallFPR : {0} , currentFPR : {1} , currentDR : {2} , prevFPR : {3} , threshold : {4} >".format(cascade.overallFPR(),cascade.currentFPR(),cascade.currentDR(),cascade.prevDR(),ada.threshold))  
                ########
        
        ########
        logger.info("< Finish taining {0}th layer , up to {1} weak classifiers . >".format(len(cascade.adaboostClassifiers),len(ada.weakClassifiers)))
        logger.info("< overallFPR : {0} , currentFPR : {1} , currentDR : {2} >".format(cascade.overallFPR(),cascade.currentFPR(),cascade.currentDR()))  
        ########
        
        posData,negData = updateDataset(images,cascade)
        logger.info('< postive dataset : {0} , negative dataset : {1} >'.format(len(posData),len(negData)))
    return cascade