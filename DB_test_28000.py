#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 17:37:54 2020

@author: lenovo
"""
import os
import shutil

directory = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/DB_test/'
if not os.path.exists(directory):
    os.makedirs(directory)
else:
    print('Il y a déjà une base de données à cet emplacement')

ID = 0
for i in range(387045-20000, 387045) :

    shutil.move('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/{}'.format(i),
                '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_test/{}'.format(ID))
    ID += 1