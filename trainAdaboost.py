# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:40:01 2017

@author: C.E
"""

import numpy as np
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures  
import logging
from multiprocessing import Pool

logger = logging.getLogger(__name__)

def trainAdaboostClassifier(images,features):
        
    #(1)normalize the weight
    normalizeWeight(images)
    
    #(2)select he best weak classifier with respect to the weighted error
    error, best=bestStump_multithread(features,images)
    features.remove(best)
    logger.info('<< error : {0} >>'.format(error))
    
    #(3)update weights
    for image in images:
        if image.label == best.get_vote(image):
            image.set_weight(image.weight * np.sqrt(error/(1-error)))
        else:
            image.set_weight(image.weight * np.sqrt((1-error)/error))
            
    #(4)final storng classifiers
    alpha=np.log((1-error)/error)
     
    return (alpha,best)
         
def normalizeWeight(images):
    norm_factor=1./sum(map(lambda image:image.weight,images))
    for image in images:
        image.set_weight(image.weight * norm_factor)
    
    
def bestStump(features, images):
    
    error=float('inf')
    bestFeautre=None
    
    count=1
    for f in features:
        count+=1
        
        e=decisionStump(f,images)
        if e < error:
            bestFeautre=f
            error=e
    
    if error >= 0.5:
        logger.error('< Decision stump failed : best error ({0}) >= 0.5 >'.format(error))
    
    return error,bestFeautre 
 
def bestStump_multithread(features, images):
    
    error=float('inf')
    bestFeautre=None
    '''
    with ThreadPoolExecutor(max_workers=10) as executor:
        for f,e in zip(features,executor.map(decisionStump,features,images,chunksize=100)):
            if e < error:
                bestFeautre=f
                error=e
    
    with Pool(processes=4) as pool:
        results={pool.apply_async(decisionStump,f,images) : f for f in features}
        for result in results:
            f = results[result]
            try:
                e = result.get()
                if e < error:
                    bestFeautre=f
                    error=e
            except Exception as exc:
                print(exc)
    '''
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures={executor.submit(decisionStump,f,images) : f for f in features}
        for future in concurrent.futures.as_completed(futures):
            f = futures[future]
            try:
                e = future.result()
                if e < error:
                    bestFeautre=f
                    error=e
            except Exception as exc:
                print(exc)
                
    if error >= 0.5:
        logger.error('< Decision stump failed : best error ({0}) >= 0.5 >'.format(error))
    
    return error,bestFeautre 
    
    
def decisionStump(feature, images):
        
    #logger.info(feature)
    
    featureScore=[]
    for image in images:
        # turple (score, image)
        featureScore.append((feature.get_score(image),image))
        
    featureScore=np.array(featureScore)
    #sorted featureScore according feature score
    
    #import pdb
    #pdb.set_trace()
    featureScore=featureScore[featureScore[:,0].argsort()]
    
    #total sum of positive weight
    tpw=0.0
    #total sum of negative weight
    tnw=0.0
    #sum of positive weight below current example
    pw=[]
    #sum of negative weight below current example
    nw=[]
    
    n=0
    for f in featureScore:
        if f[1].label > 0 :
            tpw += f[1].weight
        else:
            tnw += f[1].weight
        pw.append(tpw)
        nw.append(tnw)
        n+=1
        
    error=float("inf")
    polarity=1
    threshold=featureScore[0][0]
    
    #  1 | 2 3 4 5 6 6 
    #  ^
    #  ^
    #  pw[i] or nw[i] includes this weight, need to subtract it
    #  my rule is -->  p* f(x) < p * threshold, 1
    #                  otherwise, 0
   
    for i in range(n):
        
        #import pdb
        #pdb.set_trace()
        pos=0.0
        neg=0.0
        if featureScore[i][1].label > 0:
            pos = (pw[i]-featureScore[i][1].weight) + (tnw-nw[i])
            neg = nw[i] + (tpw-pw[i]+featureScore[i][1].weight)
        else:
            pos = pw[i] + (tnw-nw[i]+featureScore[i][1].weight)
            neg = (nw[i]-featureScore[i][1].weight) + (tpw-pw[i])
         
        '''
        pos = pw[i] + (tnw-nw[i])
        neg = nw[i] + (tpw-pw[i])
        '''
        
         # e = min (S+  + (T- - S-), S- + (T+ - S+))
        #labelling all example below current negative and labeling  above positive
        # or the converse
        curError=0.0
        curPolarity=0
        if pos < neg:  #  negative | threshold | postive
            curPolarity=-1
            curError=pos
        else:         # positive | threshold | negative
            curPolarity = 1
            curError=neg
        
        if error > curError:
            threshold=featureScore[i][0]
            error=curError
            polarity=curPolarity
     
    #  negative | threshold
    if tpw < error:
        error=tpw
        polarity=-1
        threshold=featureScore[0][0]
    # positive | threshold
    if tnw < error:
        error=tnw
        polarity=1
        threshold=featureScore[0][0]
      
     
    feature.setThreshold(threshold)
    feature.setPolarity(polarity)
    
    return error
    
'''    
def debug(message):
    sys.stdout.write(message)
    sys.stdout.flush()
    
def writeOut(file,images):
    
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file,'a') as f:
        for image in images:
            f.write('weight : {0}, label : {1} \n'.format(image.weight,image.label))
            
        f.write('==============================================\n\n')
        
def writeOut1(file,message):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file,'a') as f:
        f.write(message)
        
'''