# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 15:25:32 2017

@author: C.E
"""

class AdaboostClassifier(object):
    
    def __init__(self):
        self.threshold = 0.0
        self.weakClassifiers = []
        
        
    def increaseThreshold(self, alpha):
        self.threshold += (0.5 * alpha)
        
    def decreaseThreshold(self, step=0.01):
        self.threshold -= step
    
    def addWeakClassifier(self, weakClassifier) :
        self.weakClassifiers.append(weakClassifier)
        self.increaseThreshold(weakClassifier[0])        
        
    def predict(self, image):
         return 1 if sum([c[1].get_vote(image) * c[0] for c in self.weakClassifiers]) >= self.threshold else 0
    
    def predict_with_scale(self, image,sub_window_top_left,scalar):
        return 1 if sum([c[1].get_vote_with_scale(image,sub_window_top_left,scalar) * c[0] for c in self.weakClassifiers]) >= self.threshold else 0
        
    '''
    def evaluate(self, data):
        nPositive=0
        nNegative=0
        falseNegative=0
        falsePositive=0
        truePositive=0
        trueNegative=0
        for image in data:
            result = self.predict(image)
            #print(result)
            if image.label == 1:
                nPositive+=1
                if result == 1:
                    truePositive += 1
                else:
                    falseNegative+=1
            else:
                nNegative+=1
                if result == 0:
                    trueNegative += 1
                else:
                    falsePositive+=1
                    
        return float(falsePositive/nNegative),1-float(falseNegative/nPositive)
       '''
   