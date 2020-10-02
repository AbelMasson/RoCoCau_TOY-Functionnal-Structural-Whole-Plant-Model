# -*- coding: utf-8 -*-import gc

import numpy as np
import tensorflow as tf
import os
import shutil
import matplotlib.pyplot as plt

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv3D, MaxPooling3D, Softmax
from tensorflow.keras.losses import mean_squared_error, mean_absolute_percentage_error
from tensorflow.keras.optimizers import Adam

from sklearn.metrics import mean_squared_error as mse

from Batch_Generator_Class import BatchGenerator
from Database_Class import Database

class Test(object) :
    def __init__(self, path_model, loss_function, optimizer, metrics, path_to_data, IDs_test, path_to_results, fig_name, ax_name):

        self.path_model = path_model
        self.loss_function = loss_function
        self.optimizer = optimizer
        self.metrics = metrics
        self.path_to_data = path_to_data
        self.IDs_test = IDs_test
        self.path_to_results = path_to_results
        self.fig_name = fig_name
        self.ax_name = ax_name

        self.batch_size = len(self.IDs_test)

    def predict(self):

        self.model = keras.models.load_model(self.path_model)
        self.model.compile(loss=self.loss_function,
                           optimizer=self.optimizer,
                           metrics=self.metrics)

        Batch = BatchGenerator(self.path_to_data, self.IDs_test, self.batch_size, self.ax_name, 3)
        X_test, y_test = Batch.get_Batch_raw_paramater()
        y_test_arr = Batch.get_y_test()

        y_pred = self.model.predict(X_test, verbose=1, steps=1)

        self.y_pred = y_pred
        self.y_test = y_test_arr

        score = self.model.evaluate(X_test, y_test, verbose=0, steps=1)

        self.loss = score[0]
        self.metrics = score[1]

    def split_param(self) :
        
        self.dict_test = {}
        
        self.dict_test['Sm'] = [self.y_test[i][0] for i in range(len(self.y_test))]
        self.dict_test['Sr'] = [self.y_test[i][1] for i in range(len(self.y_test))]
        self.dict_test['Al'] = [self.y_test[i][2] for i in range(len(self.y_test))]
        
        self.dict = {}
        
        self.dict['y_pred_Sm'] = [self.y_pred[i][0] for i in range(len(self.y_pred))]
        self.dict['y_pred_Sr'] = [self.y_pred[i][1] for i in range(len(self.y_pred))]
        self.dict['y_pred_Al'] = [self.y_pred[i][2] for i in range(len(self.y_pred))]
    

    def process(self, param) :
        
        y_pred_name = 'y_pred' + '_' + str(param)
        
        y_pred = list(np.copy(self.dict[y_pred_name]))
        y_test = list(np.copy(self.dict_test[param]))
        
        y_test_new = []; y_pred_new = []
        
        for i in range(len(y_test)) :
            
            index = y_test.index(min(y_test))
            
            y_test_new.append(y_test[index])
            y_pred_new.append(y_pred[index])
            
            y_test.remove(y_test[index])
            y_pred.remove(y_pred[index])
            #print(self.dict[y_pred_name])
        
        #print(y_test_new, y_pred_new)
        return y_test_new, y_pred_new
        
    def trace_pred(self, axes, title) :
        
        y_test_Sm, y_pred_Sm = self.process('Sm')
        #print(y_test_water, y_pred_water)
        y_test_Sr, y_pred_Sr = self.process('Sr')
        #print(y_test_light, y_pred_light)
        y_test_Al, y_pred_Al = self.process('Al')
        #print(y_test_light, y_pred_light)
        
        RMSE_Sm = np.square(np.subtract(y_test_Sm,y_pred_Sm)).mean() 
        RMSE_Sm = round(float(RMSE_Sm), 5)
        RMSE_Sr = np.square(np.subtract(y_test_Sr,y_pred_Sr)).mean() 
        RMSE_Sr = round(float(RMSE_Sr), 5)
        RMSE_Al = np.square(np.subtract(y_test_Al,y_pred_Al)).mean() 
        RMSE_Al = round(float(RMSE_Al), 5)

        #props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        #ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        #verticalalignment='top', bbox=props)
        x = [i for i in range(100)]
        axes[0].plot(y_test_Sm, label='y_test', c='darkblue')
        axes[0].scatter(x, y_pred_Sm, label='y_pred', c='darkred', s=8)
        axes[0].set_title('prediction Sm', fontstyle='italic')
        axes[0].text(60, 0.5, 'RMSE = '+str(RMSE_Sm), fontsize=8)
        axes[0].set_title(title)
        
        axes[1].plot(y_test_Sr, label='y_test', c='darkblue')
        axes[1].scatter(x, y_pred_Sr, label='y_pred', c='darkred', s=8)
        axes[1].set_title('prediction Sr', fontstyle='italic')
        axes[1].text(60, 0.5, 'RMSE = '+str(RMSE_Sr), fontsize=8)
        
        axes[2].plot(y_test_Al, label='y_test', c='darkblue')
        axes[2].scatter(x, y_pred_Al, label='y_pred', c='darkred', s=8)
        axes[2].set_title('prediction Al', fontstyle='italic')
        axes[2].text(60, 0.5, 'RMSE = '+str(RMSE_Al), fontsize=8)

        axes[2].legend()
    
def test_axes(path_model, ax_name, fig_name) :
    
    fig, axes = plt.subplots(nrows = 4, ncols = 3, figsize=(15,20))

    test_NoStress = Test(path_model = path_model,
		        loss_function = mean_squared_error,
		        optimizer = Adam(),
		        metrics = ['mean_absolute_percentage_error'],
		        path_to_data = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_Test_NoStress/',
		        IDs_test = [i for i in np.random.randint(0, 3900, 100)],
		        path_to_results = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
		        fig_name = 'Pred_'+fig_name+'_DB_Test.png',
                        ax_name=ax_name)

    test_NoStress.predict()
    test_NoStress.split_param()
    test_NoStress.trace_pred(axes[0], 'Prediction Sans Stress')

    test_StressL = Test(path_model = path_model,
		        loss_function = mean_squared_error,
		        optimizer = Adam(),
		        metrics = ['mean_absolute_percentage_error'],
		        path_to_data = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_Test_StressL/',
		        IDs_test = [i for i in np.random.randint(0, 3900, 100)],
		        path_to_results = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
		        fig_name = 'Pred_'+fig_name+'_DB_Test.png',
                        ax_name=ax_name)

    test_StressL.predict()
    test_StressL.split_param()
    test_StressL.trace_pred(axes[1], 'Prediction Stress Lumineux')

    test_StressH = Test(path_model = path_model,
		        loss_function = mean_squared_error,
		        optimizer = Adam(),
		        metrics = ['mean_absolute_percentage_error'],
		        path_to_data = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_Test_StressH/',
		        IDs_test = [i for i in np.random.randint(0, 3900, 100)],
		        path_to_results = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
		        fig_name = 'Pred_'+fig_name+'_DB_Test.png',
                        ax_name=ax_name)

    test_StressH.predict()
    test_StressH.split_param()
    test_StressH.trace_pred(axes[2], 'Prediction Stress Hydrique')
        
    test_StressLH = Test(path_model = path_model,
 		        loss_function = mean_squared_error,
		        optimizer = Adam(),
		        metrics = ['mean_absolute_percentage_error'],
		        path_to_data = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Data/DB_Test_StressLH/',
		        IDs_test = [i for i in np.random.randint(0, 3900, 100)],
		        path_to_results = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics/',
		        fig_name = 'Pred_'+fig_name+'_DB_Test.png',
                        ax_name=ax_name)

    test_StressLH.predict()
    test_StressLH.split_param()
    test_StressLH.trace_pred(axes[3], 'Prediction Stress Lumineux&Hydrique')
    
    fig.savefig('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Visualisation/Prediction_'+fig_name+'_par_SubDBTest.png')
    
if __name__ == '__main__' :
    
    test_axes(path_model = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/model_devine_targets_fineroot_epoch_39.h5', ax_name='targets_fineroot.npy', fig_name='fineroot')
    test_axes(path_model = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/model_devine_targets_lateralroot_epoch_39.h5', ax_name='targets_lateralroot.npy', fig_name='lateralroot')
    test_axes(path_model = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/model_devine_targets_paramtrunk_epoch_39.h5', ax_name='targets_paramtrunk.npy', fig_name='trunk')
    test_axes(path_model = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/model_devine_targets_parambranch_epoch_39.h5', ax_name='targets_parambranch.npy', fig_name='branch')
    test_axes(path_model = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/model_devine_targets_paramshortshoot_epoch_39.h5', ax_name='targets_paramshortshoot.npy', fig_name='shortshoot')
    #test_axes(path_model = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Weights/model_devine_targets_paramtaproot_epoch_39.h5', ax_name='targets_paramtaproot.npy', fig_name='taproot')
