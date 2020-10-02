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

################################################################################
# Construction des .csv contenant les infos de GRR, GRB, C et H2O
################################################################################

def get_Result_csv(path_to_file, file_name) :
    
    list_df = []
    file = ''.join([path_to_file, file_name])
    file1 = open(file, 'r')
    
    for line in file1.readlines():
        list_line = line.split(' ')
        if len(list_line) >=8 :
            list_df.append([int(list_line[1]), float(list_line[3]), float(list_line[5]), float(list_line[7]), float(list_line[9])])
        df = pd.DataFrame(list_df, columns=['t', 'H2O', 'C', 'grb', 'grr'])
    df.to_csv(file+'.csv')

################################################################################
# Construction de la figure de Transition
################################################################################


class Visu_Transition(object) :
        
        def __init__(self, path_to_csv, csv_name, path_to_image, image_name) :
            self.path_to_csv = path_to_csv
            self.csv_name = csv_name 
            self.df_GF = pd.read_csv(''.join([self.path_to_csv, self.csv_name]))
            self.df_GF = self.df_GF.fillna(0)
            self.list_GFR = self.df_GF.grr
            self.list_GFB = self.df_GF.grb
            self.list_t = self.df_GF.t
            self.dict_param = {'Racinaire' : [[0.1,0.2,0.9],[0.1,0.5,0.9],[0.5,0.6,0.2]], 'Caulinaire' : [[0.1,0.2,0.9],[0.1,0.5,0.9],[0.5,0.6,0.2]]}
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
        
        def trace_point(self, ax_, x, y, text, size) :
            ax_.scatter(x, y, s=size, facecolor='grey', edgecolor='k', alpha=1)
            ax_.text(x, y, text, fontsize = 6)
            ax_.axis('off')

        def trace(self, ax_, Sm, Sr, Al, axe_type, system_type) :

            n_points = 200
            
            #ax_.axvline(x=Sm, ymin=0, ymax=1, linestyle='--', color='grey')
            #ax_.axvline(x=Sr, ymin=0, ymax=1, linestyle='--', color='grey')
            #ax_.axhline(y=Al, xmin=0, xmax=Sr, linestyle='--', color='grey')
            
            line1 = [0]*int(Sm*n_points)
            line2 = [i*(Al/((Sr-Sm)*n_points)) for i in range(int((Sr-Sm)*n_points))]
            line3 = [Al + i*((1-Al)/((1-Sr)*n_points)) for i in range(int((1-Sr)*n_points))]
            
            xline1 = np.linspace(0, Sm, len(line1))
            xline2 = np.linspace(Sm, Sr, len(line2))
            xline3 = np.linspace(Sr, 1, len(line3))
            
            ax_.fill_between(xline1[3:-3], y1=1, y2=0, alpha=0.2, color='red')
            ax_.fill_between(xline2[3:-3], y1=1, y2=0, alpha=0.2, color='orange')
            ax_.fill_between(xline3[3:-3], y1=1, y2=0, alpha=0.2, color='green')
            
            line = line1 + line2 + line3
            
            if system_type == 'Racinaire' :
                self.dict_Att[axe_type] = [line[int(i*200)] for i in self.list_GFR]
            elif system_type == 'Caulinaire' : 
                self.dict_Att[axe_type] = [line[int(i*200)] for i in self.list_GFB]
            
            ax_.plot(np.linspace(0, 1, len(line)), line, color='red', linewidth=2, zorder=2)
            
            if system_type == 'Caulinaire' :
                #ax_.set_xticks([self.list_GFB[i] for i in [2,7]])
                ax_.set_xticks([0,1])
            elif system_type == 'Racinaire' :
                ax.set_xticks(self.list_GFR)
            #ax_.set_xticklabels(['GF(t=3)','GF(t=8)'])
            ax_.set_xticklabels([0,1], fontsize=8)
            ax_.set_xlabel('Facteur de Croissance', fontsize=8, fontstyle='italic')
            ax_.set_ylabel('Attenuation', fontsize=8, fontstyle='italic')

            
            #ax_.set_yticks([0, self.dict_Att[axe_type][2], round(self.dict_Att[axe_type][7],3), 1])
            #ax_.set_yticklabels([0, 'Att(t=3)', 'Att(t=8)', 1])
            ax_.set_yticks([0, 1])
            ax_.set_yticklabels([0, 1], fontsize=8)
            
            ax_.axvline(x=self.list_GFB[2], ymin=0, ymax=round(self.dict_Att[axe_type][2],1), linestyle='--', color='k', zorder=1)
            ax_.axvline(x=self.list_GFB[7], ymin=0, ymax=round(self.dict_Att[axe_type][7],5), linestyle='--', color='k', zorder=1)
            ax_.axvline(x=self.list_GFB[9], ymin=0, ymax=round(self.dict_Att[axe_type][9],5), linestyle='--', color='k', zorder=1)
            
            ax_.axhline(y=self.dict_Att[axe_type][2], xmin=0, xmax=round(self.list_GFB[2], 1), linestyle='--', color='k', zorder=1)
            ax_.axhline(y=self.dict_Att[axe_type][7], xmin=0, xmax=round(self.list_GFB[7], 1), linestyle='--', color='k', zorder=1)
            ax_.axhline(y=self.dict_Att[axe_type][9], xmin=0, xmax=round(self.list_GFB[9], 1), linestyle='--', color='k', zorder=1)
            
            #plt.setp(ax_.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor", fontsize=8, fontweight='bold')
            #plt.setp(ax_.get_yticklabels(),rotation=45, ha="right", rotation_mode="anchor", fontsize=8, fontweight='bold')
            ax_.set_title('Parameter Curve ' + axe_type, fontsize=8, fontstyle='italic')
            
            #self.trace_point(ax_, x=round(self.list_GFB[2], 2), y=self.dict_Att[axe_type][2], text='t=3', size=200)
            #self.trace_point(ax_, x=round(self.list_GFB[7], 2), y=self.dict_Att[axe_type][7], text='t=8', size=200)
            ax_.scatter(x=round(self.list_GFB[2], 2), y=self.dict_Att[axe_type][2], s=220, facecolor='white', edgecolor='k', alpha=1, zorder=3)
            ax_.text(x=round(self.list_GFB[2], 2)-0.02, y=self.dict_Att[axe_type][2]-0.01, s='t=3', fontsize = 5, fontweight='bold')
            ax_.scatter(x=round(self.list_GFB[7], 2), y=self.dict_Att[axe_type][7], s=220, facecolor='white', edgecolor='k', alpha=1, zorder=3)
            ax_.text(x=round(self.list_GFB[7], 2)-0.02, y=self.dict_Att[axe_type][7]-0.01, s='t=8', fontsize = 5, fontweight='bold')
            ax_.scatter(x=round(self.list_GFB[9], 2), y=self.dict_Att[axe_type][9], s=240, facecolor='white', edgecolor='k', alpha=1, zorder=3)
            ax_.text(x=round(self.list_GFB[9], 2)-0.03, y=self.dict_Att[axe_type][9]-0.015, s='t=10', fontsize = 5, fontweight='bold')
        
        def trace_Att(self, ax_, Sm, Sr, Al, axe_type) :
            ax_.axhline(y=Al, xmin = min(self.list_t), xmax = max(self.list_t), linestyle='--', color='k', zorder=1)
            ax_.fill_between(x=self.list_t, y1=Al, y2=0, alpha= 0.2, color='orange')
            ax_.fill_between(x=self.list_t, y1=1, y2=Al, alpha= 0.2, color='green')
            
            ax_.scatter(self.list_t, self.dict_Att[axe_type], s=10, c='k', zorder=2)
            ax_.plot(self.list_t, self.dict_Att[axe_type], color='k', zorder=2)
            #ax_.set_xticks([0,2,7,9])
            #ax_.set_xticklabels([1,3,8,10], fontsize=8)
            #ax_.set_yticks([0,round(self.dict_Att[axe_type][2],1),round(self.dict_Att[axe_type][7],1),1])
            #ax_.set_yticklabels([0,'Att(t=3)', 'Att(t=8)', 1], fontsize=8, fontweight='bold')
            ax_.set_xticks([1,10])
            ax_.set_xticklabels([1,10], fontsize=8)
            ax_.set_yticks([0,1])
            ax_.set_yticklabels([0,1], fontsize=8)
            ax_.set_xlabel('temps', fontsize=8, fontstyle='italic')
            ax_.set_ylabel('Attenuation', fontsize=8, fontstyle='italic')
            
            #self.trace_point(ax_, x=3, y=self.dict_Att[axe_type][2], text='t=3', size=80)
            #self.trace_point(ax_, x=8, y=self.dict_Att[axe_type][7], text='t=8', size=80)
            ax_.scatter(x=3, y=self.dict_Att[axe_type][2], s=220, facecolor='white', edgecolor='k', alpha=1, zorder=3)
            ax_.text(x=3-0.2, y=self.dict_Att[axe_type][2]-0.01, s='t=3', fontsize = 5, fontweight='bold')
            ax_.scatter(x=8, y=self.dict_Att[axe_type][7], s=220, facecolor='white', edgecolor='k', alpha=1, zorder=3)
            ax_.text(x=8-0.2, y=self.dict_Att[axe_type][7]-0.01, s='t=8', fontsize = 5, fontweight='bold')
            ax_.scatter(x=10, y=self.dict_Att[axe_type][9], s=240, facecolor='white', edgecolor='k', alpha=1, zorder=3)
            ax_.text(x=10-0.25, y=self.dict_Att[axe_type][9]-0.01, s='t=10', fontsize = 5, fontweight='bold')
            
            ax_.set_title('Attenuation ' + axe_type, fontsize=8, fontweight='bold')
            
        def get_col(self, GF, Sm, Sr) :
            if GF > Sr :
                return 'green'
            elif GF > Sm :
                return 'orange'
            elif GF < Sm :
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
            
        def drawPieMarker(self, ax_, xs, ys, colors, ratios = [.33,.33,.33], sizes = [200], labels=['Trunk', 'Branch', 'Shortshoot']):
            assert sum(ratios) <= 1, 'sum of ratios needs to be < 1'

            markers = []
            previous = 0
            for color, ratio, label in zip(colors, ratios, labels):
                this = 2 * np.pi * ratio + previous
                x  = [0] + np.cos(np.linspace(previous, this, 10)).tolist() + [0]
                y  = [0] + np.sin(np.linspace(previous, this, 10)).tolist() + [0]
                xy = np.column_stack([x, y])
                previous = this
                markers.append({'marker':xy, 's':np.abs(xy).max()**2*np.array(sizes), 'facecolor':color, 'label':label})

            # scatter each of the pie pieces to create pies
            for marker in markers:
                ax_.scatter(xs, ys, **marker)
            if ys == 1 :
                ax_.legend(fontsize=8, loc=4)
            
        def drawPieMarkerlegend(self, ax_, xs, ys, colors, ratios = [.33,.33,.33], sizes = [200], labels=['Trunk', 'Branch', 'Shortshoot']):
            assert sum(ratios) <= 1, 'sum of ratios needs to be < 1'

            markers = []
            previous = 0
            for color, ratio, label in zip(colors, ratios, labels):
                this = 2 * np.pi * ratio + previous
                x  = [0] + np.cos(np.linspace(previous, this, 10)).tolist() + [0]
                y  = [0] + np.sin(np.linspace(previous, this, 10)).tolist() + [0]
                xy = np.column_stack([x, y])
                previous = this
                markers.append({'marker':xy, 's':np.abs(xy).max()**2*np.array(sizes), 'facecolor':color, 'label':label})

            # scatter each of the pie pieces to create pies
            for marker in markers:
                ax_.scatter(xs, ys, **marker)
                ax_.legend(fontsize=8, loc = 4)

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
	    
            #self.drawPieMarker(ax_, xs=GFB, ys=1, colors=['grey', 'grey', 'grey'])
            ax_.set_xlabel('Facteur de Croissance', fontsize=8)
            #ax_.set_title('Facteurs de Croissance', fontsize=8, fontstyle='italic')
            
            
            ax_.set_yticks(np.asarray([1,3,8,10]))
            ax_.set_yticklabels([1,3,8,10], fontsize = 8, fontweight='bold')
            ax_.set_ylabel('temps', fontsize=8)
            
            #ax_.set_xticks(np.asarray([0, round(self.list_GFB[2],3), round(self.list_GFB[5],3), 1]))
            #ax_.set_xticklabels([0, 'GF(t=3) = ' + '\n' + str(round(self.list_GFB[2],3)), 'GF(t=8) = ' + '\n' + str(round(self.list_GFB[7],3)), 1], 
                                 #fontsize=6, fontweight='bold', rotation=45)
            ax_.set_xticks(np.asarray([0, 1]))
            ax_.set_xticklabels([0, 1], fontsize=6, fontweight='bold')
            ax_.set_title('Evolution du facteur de croissance caulinaire ' + '\n' + 'au cours du temps', fontsize=8, fontweight='bold')
        
        def trace_main(self, path_to_save) :
            fig = plt.figure(constrained_layout=True, figsize=(15, 6))
            gs = fig.add_gridspec(2, 4)
            
            f_ax1 = fig.add_subplot(gs[0, 1])
            self.trace(f_ax1, Sm=0.1, Sr=0.2, Al=0.9, axe_type='Trunk', system_type='Caulinaire')
            
            f_ax2 = fig.add_subplot(gs[0, 2])
            self.trace(f_ax2, Sm=0.1, Sr=0.5, Al=0.9, axe_type='Branch', system_type='Caulinaire')

            f_ax3 = fig.add_subplot(gs[0, 3])
            self.trace(f_ax3, Sm=0.5, Sr=0.6, Al=0.2, axe_type='Shortshoot', system_type='Caulinaire')

            f_ax4 = fig.add_subplot(gs[1, 1])
            self.trace_Att(f_ax4, Sm=0.1, Sr=0.2, Al=0.9, axe_type='Trunk')

            f_ax5 = fig.add_subplot(gs[1, 2])
            self.trace_Att(f_ax5, Sm=0.1, Sr=0.5, Al=0.9, axe_type='Branch')

            f_ax6 = fig.add_subplot(gs[1, 3])
            self.trace_Att(f_ax6, Sm=0.5, Sr=0.6, Al=0.2, axe_type='Shortshoot')

            f_ax7 = fig.add_subplot(gs[0:2, 0])
            self.trace_Caul_Growth_Factor(f_ax7)
            #f_ax8 = fig.add_subplot(gs[0, 0])
            #self.trace_PE(f_ax8)
            
            #fig.suptitle("Determination des attenuations de croissance des axes caulinaires en fonction" + '\n' + "de l'environnement (facteur de croissance) et du génotype (courbes d'attenuation)", fontweight='bold', fontsize=11)
            fig_name='fig_Transition3_sans_titre.png'
            path_fig = ''.join([path_to_save, fig_name])
            fig.show()
            fig.savefig(path_fig)

if __name__ == '__main__' :
    #get_Result_csv('/home/abel/Desktop/Fig_Transition/', 'GR_W3_L2_Caul')
    visu = Visu_Transition('/home/abel/Desktop/Fig_Transition/', 'GR_W3_L2_Caul.csv', '/home/abel/Desktop/Fig_Transition/', 'PE_Caul_10.png')
    visu.trace_main('/home/abel/Desktop/Fig_Transition/')
        


