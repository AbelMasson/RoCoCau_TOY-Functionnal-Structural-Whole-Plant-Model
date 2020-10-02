#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:51:17 2020

@author: lenovo
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import imageio
from pathlib import Path
#import cv2
from PIL import Image
import numpy as np


def Visualisation_CM(path_to_CM, CM_name) :
    path_CM = os.path.join(path_to_CM, CM_name)
    CM = np.load(path_CM)
    
    fig = plt.figure()
    sns.heatmap(CM)
    
    fig.show()
    fig.savefig('/home/lenovo/Bureau/')
    
def gif_HM(path_to_images) :
    
    
    images = list(Path(path_to_images).glob('*.png'))
    image_list = []
    for file_name in images:
        image_list.append(imageio.imread(file_name))
        
    imageio.mimwrite('animated_from_images.gif', image_list, loop=2, fps=3)
    
def gif_RoCoCau(path_to_images, images_name, anim_name, n_img, loop, fps) :
    '''
    Attention images name avec un {} pour pouvoir rajouter l'index de l'image
    anim_name se termine par .gif
    '''
    image_list = []
    for i in range(1,n_img) :
        img_name = ''.join([path_to_images, images_name.format(i)])
        image_list.append(imageio.imread(img_name))
    
    anim_path = ''.join([path_to_images, anim_name])
    imageio.mimwrite(anim_name, image_list, loop=loop, fps=fps)
    
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def anim_stratH(path_to_images1, images_name1, path_to_images2, images_name2,
               anim_name, n_img, loop, fps):
    
    image_list = []
    for i in range(n_img) :
        im1_path = os.path.join(path_to_images1, images_name1.format(i))
        im1 = Image.open(im1_path)
        im1 = im1.resize((round(im1.size[0]*0.9), round(im1.size[1]*0.9)))
        im2_path = os.path.join(path_to_images2, images_name2.format(i))
        im2 = Image.open(im2_path)
        im2 = im2.resize((round(im2.size[0]*1.8), round(im2.size[1]*1.8)))
        
        im_v = get_concat_h(im2, im1)
        image_list.append(im_v)
    
    anim_path = ''.join([path_to_images1, anim_name])
    imageio.mimwrite(anim_path, image_list, loop=loop, fps=fps)   

def anim_stratV(path_to_images1, images_name1, path_to_images2, images_name2,
               anim_name, n_img, loop, fps):
    
    image_list = []
    for i in range(n_img) :
        im1_path = os.path.join(path_to_images1, images_name1.format(i))
        im1 = Image.open(im1_path)
        im1 = im1.resize((round(im1.size[0]*1), round(im1.size[1]*1)))
        im2_path = os.path.join(path_to_images2, images_name2.format(i))
        im2 = Image.open(im2_path)
        im2 = im2.resize((round(im2.size[0]*1.5), round(im2.size[1]*2)))
        
        im_v = get_concat_v(im1, im2)
        image_list.append(im_v)
    
    anim_path = ''.join([path_to_images1, anim_name])
    imageio.mimwrite(anim_path, image_list, loop=loop, fps=fps)  

if __name__ == '__main__' :
    anim_stratV(path_to_images1 = '/home/lenovo/Bureau/AnimStratAleatoire/',
               images_name1 = 'Strat{}.png',
               path_to_images2 = '/home/lenovo/Bureau/AnimParamAleatoire',
               images_name2 = 'Param_aleatoire_{}.png',
               anim_name = 'Anim_Strat_TOYV.gif',
               n_img = 20,
               loop = 1,
               fps = 1
               )     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
