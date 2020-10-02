#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 17:37:54 2020

@author: lenovo
"""

import os
import numpy as np
import shutil
import subprocess


def search_empty_examples() :
    for i in range(367049) :
        l = []
        path1='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}/imgabswood.npy'.format(i)
        path2='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}/targets_paramtrunk.npy'.format(i)
        if os.path.getsize(path1) == 0 or os.path.getsize(path2) == 0 :
            l.append(i)
            print(i)
        if i%1000 == 0 :
            print('search completed {} %'.format((i/367049)*100))

def empty_examples_gicle() :
    ID = 366908
    for i in range(86533, 86601) :
        shutil.rmtree('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(i), ignore_errors=True)
        #path = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(i)
        #subprocess.run(["rm", "-rf", path])
        shutil.move('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(ID), '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(i))
        ID -= 1


shutil.rmtree('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(86601), ignore_errors=True)
shutil.move('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(366840), '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(86601))
