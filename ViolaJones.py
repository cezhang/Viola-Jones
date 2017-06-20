import utils
import time
import trainCascade
from HaarLikeFeature import HaarLikeFeature
from HaarLikeFeature import FeatureTypes
import logging
import logging.config
import constants
from time import strftime


if __name__ == "__main__":
    
    start=time.time()
    logging.config.fileConfig('logconfig.ini',disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    
    logger.info('************************************')
    logger.info('************************************')
    logger.info('************************************')
    logger.info('******                      ********')
    logger.info('****** Viola-Jones Training ********')
    logger.info('*******                     ********')
    logger.info('************************************')
    logger.info('************************************')    
    logger.info('************************************')  
    
    ##################
    ##### 
    ##################
    logger.info('<Loading data ...>')
    faces = utils.load_images(constants.FACES_PATH, 1)
    logger.info('< '+str(len(faces)) + ' faces loaded. >')
    non_faces = utils.load_images(constants.NON_FACES_PATH, 0)
    logger.info('< '+str(len(non_faces)) + ' non_faces loaded. >')
    logger.info('< Finish loading data ... >')
    
    logger.info('< Building Haar-like features ... >')
    features=[]
    for f in FeatureTypes:
        for width in range(f[0],constants.IMAGE_SIDE+1,f[0]):
            for height in range(f[1],constants.IMAGE_SIDE+1,f[1]):
                for x  in range(constants.IMAGE_SIDE+1-width):
                    for y in range(constants.IMAGE_SIDE+1-height):
                        features.append(HaarLikeFeature(f,(x,y),width,height,0,1))
    logger.info('< '+str(len(features))+' Haar-like features created. >')
    logger.info(' Finish building Haar-like features ... >')
    
    ##################
    ##### 
    ##################
    logger.info('< F : {0} , D : {1} , Ftarget : {2} >'.format(constants.F,constants.D,constants.Ftarget))
    logger.info('< Start training cascade classifer ... >')
    cascade=trainCascade.train(constants.F,constants.D,constants.Ftarget,faces,non_faces,features)
    logger.info('< Finish training cascade classifer ... >')
    
    ##################
    ##### 
    ##################
    logger.info('< Exporting final model ... >')    
    run_name=strftime("%Y%m%d-%H%M%S", time.localtime()).replace('-','')
    filename='../result/'+run_name+'/cascade.txt'
    utils.writeOut(cascade,filename)
    logger.info('< Finish exporting final model ... >')   
    
    ##################
    ##### 
    ##################
    end=time.time()
    m, s = divmod((end-start),60)
    h, m = divmod(m, 60)
    logger.info('< Elasped {0} hour(s) : {1} minute(s) : {2} second(s) >'.format(h,m,s))
    
    