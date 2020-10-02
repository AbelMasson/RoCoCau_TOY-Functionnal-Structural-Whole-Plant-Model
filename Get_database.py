#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on Thu Jul 23 10:23:09 2020
@author: abel

Description : Procédure à suivre à partir de la base de données brutes pour obtenir la base d'entrée du réseau.
'''

import os
import numpy as np
import glob
from Database_Class import Database, Database_Raw

'''
PARAMETRES A MODIFIER EN FONCTION DE LA BASE DE DONNEES A CONSTRUIRE
ATTENTION : Si l'on souhaite constituer une base de test, il faut découper 
en amont la base de données brutes en base de test et base d'entrainement 
puis lancez ce programme sur chacune des deux.

Pour lancer ce programme, ouvrez un terminal de commande, 
placez vous dans le dossier contenant ce script ( cd Path/To/Script )
puis tapez la commande : python ./Get_database.py
'''
#-----------------------------------------------------------------------------------------------------------------------

#Nom de la base de données brutes
Raw_DB_name = 'databasewholepl'
#Emplacement de la base de données brutes
path_to_Raw_DB = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/'
#Nom de la base de données d'entrée à construire A CHOISIR
DB_v1_name = 'DB_tot'
#Emplacement de la base de données d'entrée A CHOSIR
path_to_DB = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/'

#-----------------------------------------------------------------------------------------------------------------------

'''
A PARTIR D'ICI NE RIEN TOUCHER
'''

'''
Instanciation des deux classes pour nos bases de données,
Creation physique de la base de données en entrée du réseau
'''
#Creation d'une instance de la classe Database pour notre base à construire
#Creation d'une instance de la classe Database_Raw pour notre base de données brutes
DB_v1 = Database(DB_v1_name, path_to_DB)
DB_Raw = Database_Raw(Raw_DB_name, path_to_Raw_DB, path_to_copy=path_to_DB)

'''
#Creation physique de la base de données
sub_path = ''.join([DB_v1.path_to_DB, DB_v1_name])
if not os.path.exists(sub_path):
    DB_v1.Create()
else :
    print('La base de données est déjà créée')

'''
#Test du contenu des deux bases
'''

print('Contenu de la base de données créée : ')
DB_v1.Content()
print('Contenu de la base de données brutes : ')
DB_Raw.Content()

'''
#Tri sur la qualité des données de DB_raw.
'''


sub_path = ''.join([path_to_DB, Raw_DB_name])
if not os.path.exists(sub_path):
    DB_Raw.Tri2(['imgabswood.vct', 'targets.csv'])
else :
    print('La base de données brutes est déjà triée')
'''
'''
Traitement des données brutes et remplissage de la base de donnnées d'entrée
'''

DB_v1.Fill_and_Preprocess(Raw_DB_name, path_to_DB)
if DB_v1.size == 0 :
    DB_v1.Fill_and_Preprocess(Raw_DB_name, path_to_DB)
else :
    print("La base de données d'entrée est déjà remplie")

'''
Vérification du traitement et du remplissage
'''
print('Contenu de la base de données remplie : ')
DB_v1.Content()

'''
Ajout des labels pour l'environnement dans la base de données d'entrée
'''
sub_path = ''.join([DB_v1.path, '/100000/targets_class.npy'])
if not os.path.exists(sub_path):
    DB_v1.Labelize_DB()
else :
    print('Les données sont déjà labelisées')

sub_path = ''.join([DB_v1.path, '/569/targets_paramenv.npy'])
if not os.path.exists(sub_path):
    DB_v1.get_paramenv()
else :
    print('Les paramètres environnement sont déjà isolés dans un fichier')

'''
On vérifie que les fichiers de classe ont bien été chargés
'''
print("Contenu final d'un exemple de la base de données")
DB_v1.Content()

'''
On construit les sous-bases de données correspondant aux différentes conditions environnementales
'''
if not os.path.exists(os.path.join(path_to_subDB, 'DB_StressH')) :
    DB_v1.subdivise(subDB_name=DB_StressH, subDB_label=(1 or 2))
if not os.path.exists(os.path.join(path_to_subDB, 'DB_StressL')) :
    DB_v1.subdivise(subDB_name=DB_StressL, subDB_label=(3 or 1))
if not os.path.exists(os.path.join(path_to_subDB, 'DB_StressLH')) :
    DB_v1.subdivise(subDB_name=DB_StressLH, subDB_label=1)
if not os.path.exists(os.path.join(path_to_subDB, 'DB_NoStress')) :
    DB_v1.subdivise(subDB_name=DB_NoStress, subDB_label=4)






