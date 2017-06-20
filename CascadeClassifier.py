# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 16:29:49 2017

@author: C.E
"""

class CascadeClassifier(object):
    
    def __init__(self):
        self.adaboostClassifiers = []
        self.falsePositiveRate = []
        self.detectionRate = []
        
        
    def addAdaboostClassifier(self, adaboostClassifier):
        self.adaboostClassifiers.append(adaboostClassifier)        
        self.falsePositiveRate.append(1.0)
        self.detectionRate.append(1.0)
        
    def currentFPR(self):
        return self.falsePositiveRate[-1]
        
    def currentDR(self):
        return self.detectionRate[-1]
        
    def overallFPR(self):
        res = 1.0
        for fpr in self.falsePositiveRate:
            res *= fpr
            
        return res
        
    def prevFPR(self):
        if len(self.falsePositiveRate) < 2 :
            return 1.0
        else:
            return self.falsePositiveRate[-2]
        
    def prevDR(self):
        if len(self.detectionRate) < 2 :
            return 1.0
        else :
            return self.detectionRate[-2]
        
    def predict(self,image):
        for ada in self.adaboostClassifiers:
            if ada.predict(image) == 0 :
                return 0
        return 1       
        
    def predict_with_scale(self,image,sub_window_top_left,scalar):
        for ada in self.adaboostClassifiers:
            if ada.predict_with_scale(image,sub_window_top_left,scalar) == 0:
                return 0
                
        return 1
        
        
    def evaluate(self, data):
        nPositive=0
        nNegative=0
        falseNegative=0
        falsePositive=0
        truePositive=0
        trueNegative=0
        for image in data:
            result = self.predict(image)
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
            
        fpr = float(falsePositive/nNegative)
        dr = 1-float(falseNegative/nPositive)
        
        #update current layer
        self.falsePositiveRate[-1] = fpr
        self.detectionRate[-1] = dr
            
        return fpr,dr