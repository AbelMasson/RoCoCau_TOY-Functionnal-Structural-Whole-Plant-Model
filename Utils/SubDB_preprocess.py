#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:23:09 2020

@author: abel

Description : Ce script définit les fonctions nécessaires aux conversions des fichiers .vct d'images 3D et .csv de paramètres en
fichiers .npy.
"""
import os
import struct
import numpy as np
import pandas as pd
import shutil


def create_label_DB(path_npy_target, npy_target_name, label_name='DB_label.npy'):
    parameters = np.load(os.path.join(path_npy_target, npy_target_name), allow_pickle=True)
    water = float(parameters[0])
    light = float(parameters[1])
    

    if water > 0.75:
        if light > 0.75:
            DB_file = 4
        if light <= 0.75:
            DB_file = 3
    if water <= 0.75:
        if light > 0.75:
            DB_file = 2
        if light <= 0.75:
            DB_file = 1
    
    path_DB_file = os.path.join(path_npy_target, label_name)
    np.save(path_DB_file, DB_file)

def fill_one_example(example_path, subDB_name, path_to_subDB, ID_example) :

    subdirID = os.path.join(path_to_subDB, subDB_name) + '/{}/'.format(ID_example)
    shutil.copytree(example_path, subdirID)

