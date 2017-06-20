
import numpy as np

def enum(**enums):
    return type('Enum', (), enums)

FeatureType = enum(TWO_VERTICAL = (1,2), TWO_HORIZONTAL = (2,1), THREE_HORIZONTAL = (3,1), THREE_VERTICAL = (1,3), FOUR = (2,2))
FeatureTypes = [FeatureType.TWO_VERTICAL, FeatureType.TWO_HORIZONTAL, FeatureType.THREE_VERTICAL, FeatureType.THREE_HORIZONTAL, FeatureType.FOUR]

class HaarLikeFeature(object):

    def __init__(self, feature_type, position, width, height, threshold, polarity):
        '''
        @param feature_type: see FeatureType enum
        @param position: top left corner where the feature begins (tuple)
        @param width: width of the feature
        @param height: height of the feature
        @param threshold: feature threshold
        @param polarity: polarity of the feature (-1, 1)
        '''
        self.type = feature_type
        self.top_left = position
        self.bottom_right = (position[0] + width, position[1] + height)
        self.width = width
        self.height = height
        self.threshold = threshold
        self.polarity = polarity
    
    def get_score(self, intImage):
        score = 0
        if self.type == FeatureType.TWO_VERTICAL:
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width, self.top_left[1] + self.height//2))
            second = intImage.get_area_sum((self.top_left[0], self.top_left[1] + self.height//2), self.bottom_right)
            score = first - second
        elif self.type== FeatureType.TWO_HORIZONTAL:
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width//2, self.top_left[1] + self.height))
            second = intImage.get_area_sum((self.top_left[0] + self.width//2, self.top_left[1]), self.bottom_right)
            score = first - second
        elif self.type == FeatureType.THREE_HORIZONTAL:
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width//3, self.top_left[1] + self.height))
            second = intImage.get_area_sum((self.top_left[0] + self.width//3, self.top_left[1]), (self.top_left[0] + 2*self.width//3, self.top_left[1] + self.height))
            third = intImage.get_area_sum((self.top_left[0] + 2*self.width//3, self.top_left[1]), self.bottom_right)
            score = first - second + third
        elif self.type == FeatureType.THREE_VERTICAL:
            first = intImage.get_area_sum(self.top_left, (self.bottom_right[0], self.top_left[1] + self.height//3))
            second = intImage.get_area_sum((self.top_left[0], self.top_left[1]+ self.height//3), (self.bottom_right[0], self.top_left[1] + 2*self.height//3))
            third = intImage.get_area_sum((self.top_left[0], self.top_left[1] + 2*self.height//3), self.bottom_right)
            score = first - second + third
        elif self.type == FeatureType.FOUR:
            # top left area
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width//2, self.top_left[1] + self.height//2))
            # top right area
            second = intImage.get_area_sum((self.top_left[0] + self.width//2, self.top_left[1]), (self.bottom_right[0], self.top_left[1] + self.height//2))
            # bottom left area
            third = intImage.get_area_sum((self.top_left[0], self.top_left[1] + self.height//2), (self.top_left[0] + self.width//2, self.bottom_right[1]))
            # bottom right area
            fourth = intImage.get_area_sum((self.top_left[0] + self.width//2, self.top_left[1] + self.height//2), self.bottom_right)
            score = first - second - third + fourth
        return score
    
    def get_vote(self, intImage):
        score = self.get_score(intImage)
        #print(score)
        #return 1 if score < self.polarity*self.threshold else -1\
        return 1 if score * self.polarity < self.polarity*self.threshold else 0
    
    def __str__(self):
        return ' FeatureType: {0} \n Position:{1} \n Width:{2} \n Height:{3} \n Threshold :{4} \n Polarity:{5}'.format(self.type,self.top_left,self.width,self.height,self.threshold,self.polarity)
        
    __repr__ = __str__
    
    
    def setThreshold(self, threshold):
        self.threshold=threshold
        
    def setPolarity(self, polarity):
        self.polarity=polarity
        
    
    def get_vote_with_scale(self, intImage,sub_window_top_left,scalar):
        score = self.get_score_with_scale(intImage,sub_window_top_left,scalar)
        return 1 if score * self.polarity < self.polarity * self.threshold  else 0
        
    def get_score_with_scale(self, intImage,sub_window_top_left,scalar):
        score = 0
        tl = (np.int(np.ceil(self.top_left[0] * scalar) + sub_window_top_left[0]) , np.int(np.ceil(self.top_left[1] * scalar) + sub_window_top_left[1]))
        br = (np.int(np.ceil(self.bottom_right[0] * scalar) + sub_window_top_left[0]),np.int(np.ceil(self.bottom_right[1] * scalar) + sub_window_top_left[1]))
        w = np.int(np.ceil(self.width * scalar)) 
        w2 = np.int(np.ceil(self.width * scalar / 2)) 
        w3 = np.int(np.ceil(self.width * scalar / 3))
        h = np.int(np.ceil(self.height * scalar)) 
        h2 = np.int(np.ceil(self.height * scalar / 2)) 
        h3 = np.int(np.ceil(self.height * scalar / 3)) 
        
        if self.type == FeatureType.TWO_VERTICAL:
            '''
                -----------
                |         |
                -----------
                |#########|
                -----------
            '''
            first = intImage.get_area_sum(tl, (tl[0] + w, tl[1] + h2))
            second = intImage.get_area_sum((tl[0], tl[1] + h2), br)
            score = first - second
        elif self.type== FeatureType.TWO_HORIZONTAL:
            '''
                  -------------
                  |     |#####|
                  |     |#####|
                  |     |#####|
                  -------------
            '''
            first = intImage.get_area_sum(tl, (tl[0] + w2, tl[1] + h))
            second = intImage.get_area_sum((tl[0] + w2, tl[1]), br)
            score = first - second
        elif self.type == FeatureType.THREE_HORIZONTAL:
            '''
                  -------------------
                  |     |#####|     |
                  |     |#####|     |
                  |     |#####|     |
                  -------------------
            '''
            first = intImage.get_area_sum(tl, (tl[0] + w3, tl[1] + h))
            second = intImage.get_area_sum((tl[0] + w3, tl[1]), (tl[0] + 2 * w3, tl[1] + h))
            third = intImage.get_area_sum((tl[0] + 2 * w3, tl[1]), br)
            score = first - second + third
        elif self.type == FeatureType.THREE_VERTICAL:
            '''
                -----------
                |         |
                -----------
                |#########|
                -----------
                |         |
                -----------
            '''
            first = intImage.get_area_sum(tl, (br[0], tl[1] + h3))
            second = intImage.get_area_sum((tl[0], tl[1]+ h3), (br[0], tl[1] + 2 * h3))
            third = intImage.get_area_sum((tl[0], tl[1] + 2 * h3), br)
            score = first - second + third
        elif self.type == FeatureType.FOUR:
            '''
                ----------------------
                |         |##########|
                |         |##########|
                ----------------------
                |#########|          |
                |#########|          |
                ----------------------
            '''
            # top left area
            first = intImage.get_area_sum(tl, (tl[0] + w2, tl[1] + h2))
            # top right area
            second = intImage.get_area_sum((tl[0] + w2, tl[1]), (br[0], tl[1] + h2))
            # bottom left area
            '''
            print('self.bottomR : {0}'.format(self.bottom_right))
            print('sub_window_top_left : {0}'.format(sub_window_top_left))
            print('br : {0}'.format(br))
            print('scalar : {0}'.format(scalar))
            print((tl[0], tl[1] + h2), (tl[0] + w2, br[1]))
            '''
            third = intImage.get_area_sum((tl[0], tl[1] + h2), (tl[0] + w2, br[1]))
            # bottom right area
            fourth = intImage.get_area_sum((tl[0] + w2, tl[1] + h2), br)
            score = first - second - third + fourth
        return score / scalar