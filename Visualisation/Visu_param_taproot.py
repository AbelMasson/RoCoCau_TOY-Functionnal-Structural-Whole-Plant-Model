#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:22:40 2020

@author: abel
"""
import numpy as np
import matplotlib.pyplot as plt
import os

def Visu_param_taproot(DB_name='DB_tot_StressLH', path_to_DB='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/') :
    
    path_to_paramfile = os.path.join(path_to_DB, DB_name)
    Sm = []; Sr = []; Al=[]
    
    for i in range(100) :
        path_param_file = ''.join([path_to_paramfile, '/{}/targets_paramtaproot.npy'.format(i)])
        param_file = np.load(path_param_file)
        Sm.append(param_file[0]); Sr.append(param_file[1]); Al.append(param_file[2])
    
    Sm_new = []; Sr_new = []; Al_new = []; 
    for i in range(len(Sm)) :
        
        index_Sm = Sm.index(min(Sm))
        index_Sr = Sr.index(min(Sr))
        index_Al = Al.index(min(Al))
        
        Sm_new.append(Sm[index_Sm])
        Sr_new.append(Sr[index_Sr])
        Al_new.append(Al[index_Al])
        
        Sm.remove(Sm[index_Sm])
        Sr.remove(Sr[index_Sr])
        Al.remove(Al[index_Al])
    
    fig, axes =  plt.subplots(nrows=1, ncols=3)
    axes[0].plot(Sm_new)
    axes[0].set_title('Sm')
    axes[1].plot(Sr_new)
    axes[1].set_title('Sr')
    axes[2].plot(Al_new)
    axes[2].set_title('Al')
    fig.suptitle('Paramètres Taproot')
    fig.savefig('/home/abel/Desktop/Visuparamtaproot.png')
    #fig.show()


if __name__ == '__main__' :
    Visu_param_taproot(DB_name='DB_tot_StressLH', path_to_DB='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/')
