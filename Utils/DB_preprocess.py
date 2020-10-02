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

def NormTrans(voxel_value, max_value) :
    if max_value != 0 :
        return -1 + 2*(voxel_value/max_value)
    return -1

def convert_vct_to_npy(path_image_file, path_image_to_save, vct_image_name='imgabswood.vct', npy_image_name='imgabswood.npy'):
    '''
    :param path_image_file: Emplacement du fichier contenant l'image 3D
    :param vct_image_name: Nom du fichier contenant l'image 3D. (Par défaut le nom de ce fichier est 'imgabswood.vct')
    :param path_image_to_save: Emplacement où sauvegarder le fichier .npy contenant l'image 3D.
    :param npy_image_name: Nom du fichier .npy à sauvegarder. (Par défaut ce nom est 'imgabswood.npy')
    :return: Cette fonction charge, convertit et change la structure de l'image 3D contenue dans un fichier .vct,
    d'une liste de 27000 flottants à un tableau numpy de dimension 30*30*30, dont les coefficients sont compris
    entre -1 et 1. Elle sauvegarde ce tableau au format .npy à l'emplacement choisi.
    '''

    #Lecture du fichier .vct et conversion en liste
    path_to_file = os.path.join(path_image_file, vct_image_name)
    file = open(path_to_file, 'rb')

    s = struct.Struct("<ffffffffffffffffffffffffffffff")
    ls = []

    while True:
        record = file.read(120)
        if len(record) != 120:
            break;
        ls += list(s.unpack(record))

    # Normalisation de la liste, en séparant la liste_abs de la liste_bois
    # Puis transformation pour que la valeur de chaque voxel soit comprise entre -1 et 1

    max_abs=max(ls[0:13500]); max_bois=max(ls[13500:27000])
    l_abs = [NormTrans(x, max_abs) for x in ls[0:13500]]
    l_bois = [NormTrans(x, max_bois) for x in ls[13500:27000]]

    data = np.asarray(l_abs + l_bois)
    data = np.reshape(data, (30,30,30))
    path_to_npy = os.path.join(path_image_to_save, npy_image_name)
    np.save(path_to_npy, data)

def convert_csv_to_npy(path_target_file, path_npy_target, csv_target_name='targets.csv', npy_target_name='targets.npy'):
    '''
    :param path_target_file: Emplacement du fichier .csv contenant les paramètres de TOY
    :param csv_target_name: Nom du fichier .csv contenant les paramètres de TOY
    (par défaut ce nom est 'targets.csv')
    :param path_target_to_save: Emplacement où sauvegarder le fichier .npy contenant les paramètres de TOY
    :param npy_target_name: Nom sous lequel sauvegarder le fichier .npy contenant les paramètres de TOY
    (par défaut ce nom est 'targets.npy')
    :return: Cette fonction charge, et convertit un fichier .csv contenant les paramètres de TOY en fichier
    .npy puis sauvegarde ce fichier à l'emplacement choisi (généralement la base de données d'entrée du réseau)
    le fichier .npy résultant contient la liste des paramètres sous forme de tableau numpy à une dimension.
    '''

    l_output = []
    parameter_file = path_target_file + csv_target_name

    df_parameters = pd.read_csv(parameter_file, header=None, sep=' ').T

    # water paramter
    l_output.append(float(df_parameters[0][1]))
    # light parameter (normalisé, ie divisé par valeur max de 200)
    l_output.append(float(df_parameters[1][1]) / 200)
    
    paramenv = np.asarray([float(df_parameters[0][1]), float(df_parameters[1][1])])
    np.save(os.path.join(path_npy_target, 'targets_paramenv.npy'), paramenv)

    # shoot1 parameter Tronc
    l_output.append(float(df_parameters[2][1]))
    l_output.append(float(df_parameters[2][2]))
    l_output.append(float(df_parameters[2][3]))

    paramtrunk = np.asarray([float(df_parameters[2][1]),float(df_parameters[2][2]),float(df_parameters[2][3])])
    np.save(os.path.join(path_npy_target, 'targets_paramtrunk.npy'), paramtrunk)

    # shoot2 parameter Rameaux longs
    l_output.append(float(df_parameters[3][1]))
    l_output.append(float(df_parameters[3][2]))
    l_output.append(float(df_parameters[3][3]))

    parambranch = np.asarray([float(df_parameters[3][1]),float(df_parameters[3][2]),float(df_parameters[3][3])])
    np.save(os.path.join(path_npy_target, 'targets_parambranch.npy'), parambranch)

    # shoot3 parameter Rameaux courts (1 seul paramètre)
    l_output.append(float(df_parameters[4][1]))
    l_output.append(float(df_parameters[4][2]))
    l_output.append(float(df_parameters[4][3]))

    paramshortshoot = np.asarray([float(df_parameters[4][1]), float(df_parameters[4][2]), float(df_parameters[4][3])])
    np.save(os.path.join(path_npy_target, 'targets_paramshortshoot.npy'), paramshortshoot)

    # root1 parameter Racines structurantes
    l_output.append(float(df_parameters[5][1]))
    l_output.append(float(df_parameters[5][2]))
    l_output.append(float(df_parameters[5][3]))

    paramtaproot = np.asarray([float(df_parameters[5][1]), float(df_parameters[5][2]), float(df_parameters[5][3])])
    np.save(os.path.join(path_npy_target, 'targets_paramtaproot.npy'), paramtaproot)

    # root2 parameter Racines secondaires
    l_output.append(float(df_parameters[6][1]))
    l_output.append(float(df_parameters[6][2]))
    l_output.append(float(df_parameters[6][3]))

    paramlateralroot = np.asarray([float(df_parameters[6][1]), float(df_parameters[6][2]), float(df_parameters[6][3])])
    np.save(os.path.join(path_npy_target, 'targets_lateralroot.npy'), paramlateralroot)

    # root3 parameter Racines absorbantes (1 seul paramètre)
    l_output.append(float(df_parameters[7][1]))
    l_output.append(float(df_parameters[7][2]))
    l_output.append(float(df_parameters[7][3]))

    paramfineroot = np.asarray([float(df_parameters[7][1]), float(df_parameters[7][2]), float(df_parameters[7][3])])
    np.save(os.path.join(path_npy_target, 'targets_fineroot.npy'), paramfineroot)

    parameter_output = np.asarray(l_output)
    parameter_output_file = os.path.join(path_npy_target, npy_target_name)

    np.save(parameter_output_file, parameter_output)

def create_label_random(path_npy_target, npy_target_name, class_name='targets_env_class.npy'):

    parameters = np.load(os.path.join(path_npy_target, npy_target_name))
    water = float(parameters[0])
    light = float(parameters[1])

    if water > 0.75:
        if light > 0.75:
            class_file = 4
        if light <= 0.75:
            class_file = 3
    if water <= 0.75:
        if light > 0.75:
            class_file = 2
        if light <= 0.75:
            class_file = 1

    path_class_file = os.path.join(path_npy_target, class_name)

    np.save(path_class_file, class_file)

