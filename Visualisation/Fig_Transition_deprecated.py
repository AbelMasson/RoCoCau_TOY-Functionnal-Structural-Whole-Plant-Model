#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 17:37:54 2020

@author: lenovo
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.image as mpimg
import os

class Visu_Transition_Caul(object) :
        
        def __init__(self, path_to_csv, csv_name, path_to_image, image_name) :
            self.path_to_csv = path_to_csv
            self.csv_name = csv_name 
            self.df_GF = pd.read_csv(''.join([self.path_to_csv, self.csv_name]))
            self.df_GF = self.df_GF.fillna(0)
            self.list_GFR = self.df_GF.grr
            self.list_GFB = self.df_GF.grb
            self.list_t = self.df_GF.t
            self.dict_param = {'Racinaire' : [[0.1,0.2,1],[0.1,0.2,0],[0.1,0.2,1]], 'Caulinaire' : [[0.1,0.2,0],[0.1,0.2,1],[0.3,0.4,1]]}
            self.dict_Att = {}
            self.path_to_image = path_to_image
            self.image_name = image_name
        
        def trace_PE(self, ax_) :

            img = mpimg.imread(os.path.join(self.path_to_image, self.image_name))
            ax_.imshow(img)
            ax_.get_xaxis().set_visible(False)
            ax_.get_yaxis().set_visible(False)
            ax_.axis('off')
            #ax_.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

        def trace(self, ax_, Sm, Sr, Al, axe_type, system_type) :

            n_points = 200
            
            ax_.axvline(x=Sm, ymin=0, ymax=1, linestyle='--', color='grey')
            ax_.axvline(x=Sr, ymin=0, ymax=1, linestyle='--', color='grey')
            ax_.axhline(y=Al, xmin=0, xmax=Sr, linestyle='--', color='grey')
            
            line1 = [0]*int(Sm*n_points)
            line2 = [i*(Al/((Sr-Sm)*n_points)) for i in range(int((Sr-Sm)*n_points))]
            line3 = [Al + i*((1-Al)/((1-Sr)*n_points)) for i in range(int((1-Sr)*n_points))]
            
            xline1 = np.linspace(0, Sm, len(line1))
            xline2 = np.linspace(Sm, Sr, len(line2))
            xline3 = np.linspace(Sr, 1, len(line3))
            
            ax_.fill_between(xline1[3:-3], y1=0.1, y2=0, alpha=0.2, color='red')
            ax_.fill_between(xline2[3:-3], y1=0.1, y2=0, alpha=0.2, color='orange')
            ax_.fill_between(xline3[3:-3], y1=0.1, y2=0, alpha=0.2, color='green')
            
            line = line1 + line2 + line3
            
            if system_type == 'Racinaire' :
                self.dict_Att[axe_type] = [line[int(i*200)] for i in self.list_GFR]
            elif system_type == 'Caulinaire' : 
                self.dict_Att[axe_type] = [line[int(i*200)] for i in self.list_GFB]
            
            ax_.plot(np.linspace(0, 1, len(line)), line, color='red', linewidth=2)
            if system_type == 'Caulinaire' :
                ax_.set_xticks(self.list_GFB)
            elif system_type == 'Racinaire' :
                ax.set_xticks(self.list_GFR)
            ax_.set_yticks(np.asarray([0, Al, 1]))
            ax_.set_xticklabels(self.list_t)
            ax_.set_yticklabels(['0', 'Al = '+str(Al), '1'])
            
            plt.setp(ax_.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor", fontsize=8, fontweight='bold')
            plt.setp(ax_.get_yticklabels(),rotation=45, ha="right", rotation_mode="anchor", fontsize=8, fontweight='bold')
            ax_.set_title('Parameter Curve ' + axe_type, fontsize=8, fontstyle='italic')
        
        def trace_Att(self, ax_, Sm, Sr, Al, axe_type) :
            ax_.axhline(y=Al, xmin = min(self.list_t), xmax = max(self.list_t), linestyle='--', color='k')
            ax_.fill_between(x=self.list_t, y1=Al, y2=0, alpha= 0.2, color='orange')
            ax_.fill_between(x=self.list_t, y1=1, y2=Al, alpha= 0.2, color='green')
            
            ax_.scatter(self.list_t, self.dict_Att[axe_type], s=10, c='k')
            ax_.plot(self.list_t, self.dict_Att[axe_type], color='k')
            
            ax_.set_title('Attenuation ' + axe_type, fontsize=8, fontstyle='italic')
            
        def get_col(self, GF, Sm, Sr) :
            if GF > Sr :
                return 'green'
            elif GF > Sm :
                return 'orange'
            else :
                return 'red'
        
        def get_PieColors(self, t, system_type) :
            if system_type == 'Racinaire' :
                GF = self.list_GFR[t]
            elif system_type == 'Caulinaire' :
                GF = self.list_GFB[t]
            
            list_colcomp = self.dict_param[system_type]
            colors = []
            for colcomp in list_colcomp :
                colors.append(self.get_col(GF, colcomp[0], colcomp[1]))
            return colors
            
        def drawPieMarker(self, ax_, xs, ys, colors, ratios = [.33,.33,.33], sizes = [200]):
            assert sum(ratios) <= 1, 'sum of ratios needs to be < 1'

            markers = []
            previous = 0
            for color, ratio in zip(colors, ratios):
                this = 2 * np.pi * ratio + previous
                x  = [0] + np.cos(np.linspace(previous, this, 10)).tolist() + [0]
                y  = [0] + np.sin(np.linspace(previous, this, 10)).tolist() + [0]
                xy = np.column_stack([x, y])
                previous = this
                markers.append({'marker':xy, 's':np.abs(xy).max()**2*np.array(sizes), 'facecolor':color})

            # scatter each of the pie pieces to create pies
            for marker in markers:
                ax_.scatter(xs, ys, **marker)

        def trace_Both_Growth_Factor(self, ax_):
	    
            for t in self.list_t :
               
                GFB = self.list_GFB[t-1]
                colors = self.get_PieColors(t-1, 'Caulinaire')
                self.drawPieMarker(ax_, xs=GFB, ys=t, colors=colors)
               
                GFR = self.list_GFR[t-1]
                colors = self.get_PieColors(t-1, 'Racinaire')
                self.drawPieMarker(ax_, xs=GFR, ys=t, colors=colors)
	    
            ax_.set_xlabel('Facteurs de Croissance', fontsize=8)
            #ax_.set_title('Facteurs de Croissance', fontsize=8, fontstyle='italic')
            
            #ax_.set_xticks(np.asarray([0, round(min(list_GFR),3), round(max(list_GFR),3), round(min(list_GFB),3), round(max(list_GFB),3), 1]))
            #ax_.set_yticks(np.asarray([0,5,10]))
            #ax_.set_yticklabels([0,5,10], fontsize = 8)
            #ax_.set_xticklabels([0, round(min(list_GFR),3), round(max(list_GFR),3), round(min(list_GFB),3), round(max(list_GFB),3), 1], fontsize=6, fontweight='bold', rotation=45)
        
        def trace_Caul_Growth_Factor(self, ax_):
	    
            for t in self.list_t :
               
                GFB = self.list_GFB[t-1]
                colors = self.get_PieColors(t-1, 'Caulinaire')
                self.drawPieMarker(ax_, xs=GFB, ys=t, colors=colors)
	    
            ax_.set_xlabel('Facteurs de Croissance', fontsize=8)
            #ax_.set_title('Facteurs de Croissance', fontsize=8, fontstyle='italic')
            
            #ax_.set_xticks(np.asarray([0, round(min(list_GFR),3), round(max(list_GFR),3), round(min(list_GFB),3), round(max(list_GFB),3), 1]))
            #ax_.set_yticks(np.asarray([0,5,10]))
            #ax_.set_yticklabels([0,5,10], fontsize = 8)
            #ax_.set_xticklabels([0, round(min(list_GFR),3), round(max(list_GFR),3), round(min(list_GFB),3), round(max(list_GFB),3), 1], fontsize=6, fontweight='bold', rotation=45)
        
        def trace_main(self, path_to_save) :
            fig = plt.figure(constrained_layout=True, figsize=(15, 6))
            gs = fig.add_gridspec(2, 4)
            
            f_ax1 = fig.add_subplot(gs[0, 1])
            self.trace(f_ax1, Sm=0.1, Sr=0.2, Al=1, axe_type='Trunk', system_type='Caulinaire')
            f_ax2 = fig.add_subplot(gs[0, 2])
            self.trace(f_ax2, Sm=0.1, Sr=0.2, Al=0, axe_type='Branch', system_type='Caulinaire')
            f_ax3 = fig.add_subplot(gs[0, 3])
            self.trace(f_ax3, Sm=0.1, Sr=0.2, Al=1, axe_type='Shortshoot', system_type='Caulinaire')
            f_ax4 = fig.add_subplot(gs[1, 1])
            self.trace_Att(f_ax4, Sm=0.1, Sr=0.2, Al=1, axe_type='Trunk')
            f_ax5 = fig.add_subplot(gs[1, 2])
            self.trace_Att(f_ax5, Sm=0.1, Sr=0.2, Al=0, axe_type='Branch')
            f_ax6 = fig.add_subplot(gs[1, 3])
            self.trace_Att(f_ax6, Sm=0.1, Sr=0.2, Al=1, axe_type='Shortshoot')
            
            f_ax7 = fig.add_subplot(gs[1, 0])
            self.trace_Caul_Growth_Factor(f_ax7)
            f_ax8 = fig.add_subplot(gs[0, 0])
            self.trace_PE(f_ax8)
            
            fig_name='fig_Transition2.png'
            path_fig = ''.join([path_to_save, fig_name])
            fig.show()
            fig.savefig(path_fig)

if __name__ == '__main__' :
    visu = Visu_Transition('/home/abel/Desktop/Fig_OPT/', 'GR_W2_L3.csv', '/home/abel/Desktop/Fig_OPT/', 'SC_W2_L3.png')
    visu.trace_main('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Visualisation/')
