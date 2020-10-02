#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import os
from Database_Class import Database

def get_portion_of_database(portion_size, path_to_DB, DB_name, path_to_portion, portion_name) :

    path_DB = os.path.join(path_to_DB, DB_name)
    path_portion = os.path.join(path_to_portion, portion_name)

    if not os.path.exists(path_portion):
        os.makedirs(path_portion)
    else:
        print('Il y a déjà une base de données à cet emplacement')

    for i in range(portion_size) :

        path_example_src = '/'.join([path_DB, str(i)])
        path_example_dst = '/'.join([path_portion, str(i)])
        shutil.copytree(path_example_src, path_example_dst)

def subdivise_portion(path_to_portion, portion_name) :

    portion = Database(portion_name, path_to_portion)

    portion.Labelize_DB()

    portion.subdivise(subDB_name='DB_28000_StressH', subDB_label=(1 or 2))
    portion.subdivise(subDB_name='DB_28000_StressL', subDB_label=(3 or 1))
    portion.subdivise(subDB_name='DB_28000_StressLH', subDB_label=1)
    portion.subdivise(subDB_name='DB_28000_NoStress', subDB_label=4)

if __name__ == '__main__' :

    get_portion_of_database(portion_size=28000, 
                            path_to_DB='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/', 
                            DB_name='DB_40000', 
                            path_to_portion='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/', 
                            portion_name='DB_28000')
    
    subdivise_portion(path_to_portion = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/',
                      portion_name = 'DB_28000')
