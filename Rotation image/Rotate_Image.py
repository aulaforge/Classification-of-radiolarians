from __future__ import print_function
from scipy.ndimage.interpolation import rotate
import matplotlib.pyplot as plt
from skimage.transform import resize
import cv2 as cv
import numpy as np
from skimage.morphology import reconstruction
import math
from math import pi
import os
from PIL import Image

import random as rng
rng.seed(12345)

directory_name = "Radiolarian images"
dirName = directory_name + " rotated"
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")


subdirectories = next(os.walk('./' + directory_name))[1]
for sub in subdirectories:
    name = dirName + "/" + sub
    try:
        # Create target Directory
        os.mkdir(name)
        print("Directory " , name ,  " Created ") 
    except FileExistsError:
        print("Directory " , name ,  " already exists")


#First, we list all the subdirectories of the "Radiolarian images" directory, in order to rotate all the images in all the subdirectories
subdirectories = next(os.walk('./' + directory_name))[1]
for sub in subdirectories:
    x = os.listdir("./" + directory_name + "/" + sub)  #We list all the files in the current subdirectory
    
    #We check all the files in order to use the script on it
    for file in x:
    
        image = cv.imread(cv.samples.findFile("./" + directory_name + "/" + sub + "/" + file))
    
        
        
        seed = np.copy(image)
        seed[1:-1, 1:-1] = image.max()
            
                
        mask = image
                
        filled = reconstruction(seed, mask, method='erosion')
                
        filled = np.uint8(filled)
                
                
        im = filled
        imgray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        ret,thresh = cv.threshold(imgray,1,255,cv.THRESH_BINARY)
        contours,hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
        for x in contours:
            if x.shape[0]>1000:
                cnt = x
                break
                
                
                
        rows,cols = im.shape[:2]  
        [vx,vy,x,y] = cv.fitLine(cnt,cv.DIST_L2,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((cols-x)*vy/vx)+y)
        im = cv.line(im,(cols-1,righty),(0,lefty),(0,255,0),2)
                
                
        slope = vy/vx
        theta = math.atan(slope)
                
                
                
        if theta>0:
            rotated_img = rotate(image,theta/pi*180-45)
        else:
            rotated_img = rotate(image,theta/pi*180+135)
        
        
        seed = np.copy(rotated_img)
        seed[1:-1, 1:-1] = rotated_img.max()
            
                
        mask = rotated_img
                
        filled = reconstruction(seed, mask, method='erosion')
                
        filled = np.uint8(filled)
                
                
        im = filled
        imgray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        ret,thresh = cv.threshold(imgray,1,255,cv.THRESH_BINARY)
        contours,hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
        for x in contours:
            if x.shape[0]>1000:
                cnt = x
                break
        
        
        x,y,w,h = cv.boundingRect(cnt)
        
        size = max(w, h)
        
        
        cut_img = rotated_img[y:y+h, x:x+w, :]
        
        
        
        image_resized = resize (cut_img, (256,256))
        image_gray = Image.fromarray((image_resized*255)    .astype('uint8'), 'RGB')
        
        plt.imshow(image_gray)
        plt.show()


        name=os.path.splitext(file)[0]+"_rotated.jpg"
        image_gray.save("./" + directory_name + " rotated/" + sub + "/" + name)