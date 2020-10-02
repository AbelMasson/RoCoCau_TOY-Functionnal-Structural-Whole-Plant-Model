#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 17:37:54 2020

@author: lenovo
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import glob
import imageio
from pathlib import Path
from sklearn.metrics import mean_squared_error
import seaborn as sns

class Visualisation_VoxNet_Devine(object):
    
    def __init__(self, path_to_results, y_pred_name, y_test_name, loss_name, n_epochs, train_loss_name) :
        
        self.path_to_results = path_to_results
        self.y_pred_name = y_pred_name
        self.y_test_name = y_test_name
        self.loss_name = loss_name
        self.n_epochs = n_epochs
        self.loss_val = np.load(os.path.join(path_to_results, loss_name))
        self.loss_train = np.load(os.path.join(path_to_results, train_loss_name))
        self.train_loss_name = train_loss_name
        
        self.dict = {}
        self.y_test = np.load(os.path.join(self.path_to_results, self.y_test_name))[0:100]
        print(len(self.y_test))
        self.loss = np.load(os.path.join(self.path_to_results, self.loss_name))
        for i in range(n_epochs) :
            self.dict['y_pred_epoch{}'.format(i)] = np.load(os.path.join(self.path_to_results, self.y_pred_name.format(i)))[0:100]
            #print(len(np.load(os.path.join(self.path_to_results, self.y_pred_name.format(i)))))
            
    def trace_loss_val(self):
        fig = plt.figure()
        plt.plot(self.loss_val)
        plt.title("Evolution de la loss de validation (RMSE) en fonction du nombre d'epochs d'apprentissage")
        #fig.show()
        fig_name = ''.join([self.loss_name[0:-4], '.png'])
        plt.savefig(os.path.join(self.path_to_results, fig_name))
    
    def trace_loss_train(self):
        fig = plt.figure()
        plt.plot(self.loss_train)
        plt.title("Evolution de la loss d'entrainement (RMSE) en fonction du nombre d'epochs d'apprentissage")
        #fig.show()
        fig_name = ''.join([self.train_loss_name[0:-4], '.png'])
        plt.savefig(os.path.join(self.path_to_results, fig_name))
    
    def split_water_light(self) :
        
        self.dict_test = {}
        
        self.dict_test['Sm'] = [self.y_test[i][0] for i in range(len(self.y_test))]
        self.dict_test['Sr'] = [self.y_test[i][1] for i in range(len(self.y_test))]
        self.dict_test['Al'] = [self.y_test[i][2] for i in range(len(self.y_test))]

        
        for epoch in range(self.n_epochs) :
        
            y_pred = self.dict['y_pred_epoch{}'.format(epoch)]
            
            self.dict['y_pred_epoch{}_Sm'.format(epoch)] = [y_pred[i][0] for i in range(len(y_pred))]
            self.dict['y_pred_epoch{}_Sr'.format(epoch)] = [y_pred[i][1] for i in range(len(y_pred))]
            self.dict['y_pred_epoch{}_Al'.format(epoch)] = [y_pred[i][2] for i in range(len(y_pred))]
        
    def process(self, epoch, param) :
        
        y_pred_name = 'y_pred_epoch{}'.format(epoch) + '_' + str(param)
        
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
        
    def trace_pred(self, axes, ax_i, epoch) :
        
        y_test_Sm, y_pred_Sm = self.process(epoch, 'Sm')
        #print(y_test_water, y_pred_water)
        y_test_Sr, y_pred_Sr = self.process(epoch, 'Sr')
        #print(y_test_light, y_pred_light)
        y_test_Al, y_pred_Al = self.process(epoch, 'Al')
        #print(y_test_light, y_pred_light)
        
        RMSE_Sm = mean_squared_error(y_test_Sm, y_pred_Sm)
        RMSE_Sm = round(RMSE_Sm, 5)
        RMSE_Sr = mean_squared_error(y_test_Sr, y_pred_Sr)
        RMSE_Sr = round(RMSE_Sr, 5)
        RMSE_Al = mean_squared_error(y_test_Al, y_pred_Al)
        RMSE_Al = round(RMSE_Al, 5)

        #props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        #ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        #verticalalignment='top', bbox=props)
        x = [i for i in range(100)]
        
        axes[ax_i, 0].plot(y_test_Sm, label='y_test')
        axes[ax_i, 0].scatter(x, y_pred_Sm, s=8, c='darkred', label='y_pred')
        axes[ax_i, 0].set_title('prediction Sm', fontstyle='italic', fontsize=8)
        axes[ax_i, 0].set_yticks([0,0.1,0.2,0.3,0.4,0.5])
        axes[ax_i, 0].set_yticklabels([0,0.1,0.2,0.3,0.4,0.5], fontsize=7)
        axes[ax_i, 0].set_xticks([0,len(y_test_Sm)])
        axes[ax_i, 0].set_xticklabels([0,len(y_test_Sm)], fontsize=8)
        #axes[ax_i, 0].text(20, 0.05, 'RMSE = '+str(RMSE_Sm), fontsize=8, fontweight='bold')
        
        axes[ax_i, 1].plot(y_test_Sr, label='y_test')
        axes[ax_i, 1].scatter(x, y_pred_Sr, s=8, c='darkred', label='y_pred')
        axes[ax_i, 1].set_title('prediction Sr', fontstyle='italic', fontsize=8)
        axes[ax_i, 1].set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8])
        axes[ax_i, 1].set_yticklabels([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8], fontsize=7)
        axes[ax_i, 1].set_xticks([0,len(y_test_Sr)])
        axes[ax_i, 1].set_xticklabels([0,len(y_test_Sr)], fontsize=8)
        #axes[ax_i, 1].text(20, 0.075, 'RMSE = '+str(RMSE_Sr), fontsize=8, fontweight='bold')
        
        axes[ax_i, 2].plot(y_test_Al, label='y_test')
        axes[ax_i, 2].scatter(x, y_pred_Al, s=8, c='darkred', label='y_pred')
        axes[ax_i, 2].set_title('prediction Al', fontstyle='italic', fontsize=8)
        axes[ax_i, 2].set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
        axes[ax_i, 2].set_yticklabels([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], fontsize=7)
        axes[ax_i, 2].set_xticks([0,len(y_test_Al)])
        axes[ax_i, 2].set_xticklabels([0,len(y_test_Al)], fontsize=8)
        #axes[ax_i, 2].text(20, 0.1, 'RMSE = '+str(RMSE_Al), fontsize=8, fontweight='bold')

        axes[ax_i, 2].legend(fontsize=8)
    
    def trace_hist(self, axes, ax_i, epoch) :
        y_test_Sm, y_pred_Sm = self.process(epoch, 'Sm')
        #print(y_test_water, y_pred_water)
        y_test_Sr, y_pred_Sr = self.process(epoch, 'Sr')
        #print(y_test_light, y_pred_light)
        y_test_Al, y_pred_Al = self.process(epoch, 'Al')
        #print(y_test_light, y_pred_light)
        
        d_Sm = [abs(y_test_Sm[i] - y_pred_Sm[i])*100/y_test_Sm[i] for i in range(len(y_test_Sm))]
        d_Sm2 = [(y_test_Sm[i] - y_pred_Sm[i])*100/y_test_Sm[i] for i in range(len(y_test_Sm))]
        mu_Sm = np.mean(d_Sm)
        med_Sm = np.median(d_Sm)
        s_Sm = np.asarray(d_Sm2).std()
        d_Sr = [abs(y_test_Sr[i] - y_pred_Sr[i])*100/y_test_Sr[i] for i in range(len(y_test_Sr))]
        d_Sr2 = [(y_test_Sr[i] - y_pred_Sr[i])*100/y_test_Sr[i] for i in range(len(y_test_Sr))]
        mu_Sr = np.mean(d_Sr)
        s_Sr = np.asarray(d_Sr).std()
        med_Sr = np.median(d_Sr)
        d_Al = [abs(y_test_Al[i] - y_pred_Al[i])*100/y_test_Al[i] for i in range(len(y_test_Al))]
        d_Al2 = [(y_test_Al[i] - y_pred_Al[i])*100/y_test_Al[i] for i in range(len(y_test_Al))]
        mu_Al = np.mean(d_Al)
        s_Al = np.asarray(d_Al2).std()
        med_Al = np.median(d_Al)
        
        #sns.distplot(d_Sm, ax = axes[ax_i, 0])
        axes[ax_i, 0].hist(d_Sm, bins=[i for i in range(0,100,2)])
        axes[ax_i, 0].axvline(x=med_Sm, ymin=0, ymax=20, color='darkred')
        axes[ax_i, 0].set_xticks([med_Sm])
        axes[ax_i, 0].set_xticklabels([round(med_Sm,1)], fontsize=8, fontweight='bold', color='darkred')
        axes[ax_i, 0].set_yticks([0,10,20])
        axes[ax_i, 0].set_yticklabels([0,10,20], fontsize=8)
        textstr =  '\n'.join((r'$\mu=%.2f$'%(mu_Sm, ), r'$\sigma=%.2f$'%(s_Sm, )))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        axes[ax_i, 0].text(mu_Sm+20, 15, textstr, fontsize=6, fontweight='bold', bbox=props)
        axes[ax_i, 0].set_title('RApE Sm', fontstyle='italic', fontsize=8)
        
        #sns.distplot(d_Sr, ax = axes[ax_i, 1])
        axes[ax_i, 1].hist(d_Sr, bins=[i for i in range(0,100,2)])
        axes[ax_i, 1].axvline(x=med_Sr, ymin=0, ymax=30, color='darkred')
        axes[ax_i, 1].set_xticks([med_Sr])
        axes[ax_i, 1].set_xticklabels([round(med_Sr,1)], fontsize=8, fontweight='bold',  color='darkred')
        axes[ax_i, 1].set_yticks([0,10,20,30])
        axes[ax_i, 1].set_yticklabels([0,10,20,30], fontsize=8)
        textstr =  '\n'.join((r'$\mu=%.2f$'%(mu_Sr, ), r'$\sigma=%.2f$'%(s_Sr, )))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        axes[ax_i, 1].text(mu_Sr+20, 20, textstr, fontsize=6, fontweight='bold', bbox=props)
        axes[ax_i, 1].set_title('RApE Sr', fontstyle='italic', fontsize=8)
        
        #sns.distplot(d_Al, ax = axes[ax_i, 2])
        axes[ax_i, 2].hist(d_Al, bins=[i for i in range(0,100,2)])
        axes[ax_i, 2].set_xticks([med_Al])
        axes[ax_i, 2].axvline(x=med_Al, ymin=0, ymax=40, color='darkred')
        axes[ax_i, 2].set_xticklabels([round(med_Al, 1)], fontsize=8, fontweight='bold', color='darkred')
        axes[ax_i, 2].set_yticks([0,10,20,30,40])
        axes[ax_i, 2].set_yticklabels([0,10,20,30,40], fontsize=8)
        textstr =  '\n'.join((r'$\mu=%.2f$'%(mu_Al, ), r'$\sigma=%.2f$'%(s_Al, )))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        axes[ax_i, 2].text(mu_Al+20, 30, textstr, fontsize=6, fontweight='bold', bbox=props)
        axes[ax_i, 2].set_title('RApE Al', fontstyle='italic', fontsize=8)
        
    def trace_main(self, epoch) :
        
        fig, axes = plt.subplots(nrows=2, ncols=3)
        self.trace_pred(axes, 0, epoch)
        self.trace_hist(axes, 1, epoch)
        plt.suptitle('Prediction epoch {}'.format(epoch), fontsize='large', fontweight='bold')
        fig_name = ''.join([self.y_pred_name[0:-4].format(epoch), '.png'])
        plt.savefig(os.path.join(self.path_to_results, fig_name))
        
    def animate_pred(self) :
        
        image_list = []
        for epoch in range(self.n_epochs) :
            
            image_name = ''.join([self.y_pred_name[0:-4].format(epoch), '.png'])
            image_path = os.path.join(self.path_to_results, image_name)
            image_list.append(imageio.imread(image_path))
            
        imageio.mimwrite(''.join([self.y_pred_name[0:-4].format(epoch), '.gif']), image_list, loop=1, fps=5)
    
    def trace_all_pred(self) :
        
        for epoch in range(self.n_epochs) :
            self.trace_main(epoch)
        
        self.animate_pred()

#Attention, taproot on a perdu le fichier contenant les valeurs des paramètres attendus pour la base de validation.. C'est bête oui.
#Je comprends surtout pas comment c'est possible qu'il n'ait pas écraser le fichier précédent, comme il l'a fait avec les autres.
if __name__ == '__main__' :
    
    Visu = Visualisation_VoxNet_Devine(path_to_results = '/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Metrics', 
                                       y_pred_name = 'y_val_targets_paramtaproot_predFT_epoch_{}.npy',
                                       y_test_name = 'y_val_targets_paramtaproot.npy',
                                       loss_name = 'val_lossFT_targets_paramtaproot_per_epoch.npy',
                                       n_epochs = 10,
                                       train_loss_name = 'train_lossFTtargets_paramtaproot.npy')
    
    Visu.trace_loss_val()
    Visu.trace_loss_train()
    Visu.split_water_light()
    #Visu.trace_all_pred()
        
        
        
