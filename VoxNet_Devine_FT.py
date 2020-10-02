import os
import numpy as np

from Nets.VoxNet_Devine_Class_FT import VoxNet
from tensorflow.keras.losses import mean_squared_error
from tensorflow.keras.optimizers import Adam

def main(target_name, target_size, path_to_data, path_modelLH, path_model, path_to_metrics, path_to_weights, batch_size, n_batch_per_step, n_epochs):
    
    # On Charge le modèle
    VoxNet_ = VoxNet(target_name, target_size)

    # On le compile
    VoxNet_.Compile(loss_function=mean_squared_error, optimizer=Adam(), metrics=['mean_absolute_percentage_error'])

    # On regarde le sommaire
    VoxNet_.sommaire()

    # On va chercher les données d'entrées
    VoxNet_.get_db(DB_name='DB_tot', path_to_DB='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/')
    print(VoxNet_.db.size)
    
    # On split la DB en deux, pour validation et entrainement
    VoxNet_.split_db(val_size=800)

    # On l'entraine.

    VoxNet_.train_and_monitor(path_to_data=path_to_data,
                             path_modelLH=path_modelLH,
                             path_model=path_model,
                             path_to_metrics=path_to_metrics,
                             path_to_weights=path_to_weights,
                             batch_size=batch_size,
                             n_batch_per_step=n_batch_per_step,
                             n_epochs=n_epochs)
'''
main(target_name='targets_parambranch.npy', 
    target_size=3,
    path_to_data='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/',
    path_modelLH = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_parambranch_DB_tot_StressLH.h5',
    path_model='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_parambranch_DB_tot.h5',
    path_to_metrics='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
    path_to_weights='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/',
    batch_size=800,
    n_batch_per_step=1,
    n_epochs=20)

main(target_name='targets_paramshortshoot.npy', 
    target_size=3,
    path_to_data='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/',
    path_modelLH='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_paramshortshoot_DB_tot_StressLH.h5',
    path_model='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_paramshortshoot_DB_tot.h5',
    path_to_metrics='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
    path_to_weights='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/',
    batch_size=800,
    n_batch_per_step=1,
    n_epochs=20)

main(target_name='targets_lateralroot.npy', 
    target_size=3,
    path_to_data='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/',
    path_modelLH='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_lateralroot_DB_tot_StressLH.h5',
    path_model='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_lateralroot_DB_tot.h5',
    path_to_metrics='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
    path_to_weights='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/',
    batch_size=800,
    n_batch_per_step=1,
    n_epochs=20)

main(target_name='targets_fineroot.npy', 
    target_size=3,
    path_to_data='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/',
    path_modelLH='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_fineroot_DB_tot_StressLH.h5',
    path_model='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_fineroot_DB_tot.h5',
    path_to_metrics='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
    path_to_weights='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/',
    batch_size=800,
    n_batch_per_step=1,
    n_epochs=20)
'''

main(target_name='targets_paramtrunk.npy', 
    target_size=3,
    path_to_data='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/',
    path_modelLH='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_paramtrunk_DB_tot.h5',
    path_model='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_paramtrunk_DB_tot.h5',
    path_to_metrics='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
    path_to_weights='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/',
    batch_size=800,
    n_batch_per_step=1,
    n_epochs=10)

main(target_name='targets_paramtaproot.npy', 
    target_size=3,
    path_to_data='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_tot/',
    path_modelLH='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_paramtaproot_DB_tot_StressLH.h5',
    path_model='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Models/model_paramtaproot_DB_tot.h5',
    path_to_metrics='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
    path_to_weights='/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/',
    batch_size=800,
    n_batch_per_step=1,
    n_epochs=10)
