from PIL import Image
import numpy as np
#import Image
'''
In an integral image each pixel is the sum of all pixels in the original image 
that are 'left and above' the pixel.

Original    Integral
+--------   +------------
| 1 2 3 .   | 0  0  0  0 .
| 4 5 6 .   | 0  1  3  6 .
| . . . .   | 0  5 12 21 .
            | . . . . . .

'''
class IntegralImage:

    def __init__(self, imageSrc, label):
        temp=Image.open(imageSrc)
        if temp.mode != 'L':
            temp=temp.convert('L')
        keep=temp.copy()
        self.original = np.array(keep)
        self.image=keep
        self.sum = 0
        self.label = label
        self.calculate_integral()
        self.weight = 0
        #temp.close()
        
        
    def calculate_integral(self):
        # an index of -1 refers to the last row/column
        # since rowSum is calculated starting from (0,0),
        # rowSum(x, -1) == 0 holds for all x
        
        '''
        if len(self.original.shape)>2:
            rowSum = np.zeros((self.original.shape[0],self.original.shape[1]))
            # we need an additional column and row
            self.integral = np.zeros((self.original.shape[0]+1, self.original.shape[1]+1))
            for x in range(self.original.shape[1]):
                for y in range(self.original.shape[0]):
                    rowSum[y, x] = rowSum[y-1, x] + self.original[y, x,0]
                    self.integral[y+1, x+1] = self.integral[y+1, x-1+1] + rowSum[y, x]
        else:
        '''
        rowSum = np.zeros(self.original.shape)
        # we need an additional column and row
        self.integral = np.zeros((self.original.shape[0]+1, self.original.shape[1]+1))
        for x in range(self.original.shape[1]):
            for y in range(self.original.shape[0]):
                rowSum[y, x] = rowSum[y-1, x] + self.original[y, x]
                self.integral[y+1, x+1] = self.integral[y+1, x-1+1] + rowSum[y, x]
    
    def get_area_sum(self, topLeft, bottomRight):
        '''
        if topLeft[0] >= self.integral.shape[0]:
            print('shape[0] : tl {0} VS {1}'.format(topLeft,self.integral.shape))
        if  bottomRight[0]>= self.integral.shape[0]:
            print('shape[0] : br {0} VS {1}'.format(bottomRight,self.integral.shape))
        if topLeft[1] >= self.integral.shape[1]:
            print('shape[1] : tl {0}'.format(topLeft))
        if  bottomRight[1]>=self.integral.shape[1]:
            print('shape[1] : br {0}'.format(bottomRight))   
        '''
        '''
        Calculates the sum in the rectangle specified by the given tuples.
        @param topLeft: (x,y) of the rectangle's top left corner
        @param bottomRight: (x,y) of the rectangle's bottom right corner 
        '''
        #print('get_area_sum: {0} , {1}'.format(topLeft,bottomRight))
        # swap tuples
        
        topLeft = (topLeft[1], topLeft[0])
        bottomRight = (bottomRight[1], bottomRight[0])
        if topLeft == bottomRight:
            return self.integral[topLeft]
        topRight = (bottomRight[0], topLeft[1])
        bottomLeft = (topLeft[0], bottomRight[1])
        
        return self.integral[bottomRight] - self.integral[topRight] - self.integral[bottomLeft] + self.integral[topLeft] 
    
    def set_label(self, label):
        self.label = label
    
    def set_weight(self, weight):
        self.weight = weight
        