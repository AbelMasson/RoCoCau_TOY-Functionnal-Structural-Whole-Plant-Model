# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Script pour visualiser la Optimal Partitionning Theory.
TODO : REVOIR LES LABELS DES DIFFERENTES MODALITES, ILS SONT UN PEU DIFFICILE A EXPLIQUER (A FORTIORI A COMPRENDRE)
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import pandas as pd
import os

def trace_Both_Growth_Factor(ax_, path_to_csv, csv_name):

    df_GF = pd.read_csv(''.join([path_to_csv, csv_name]))
    df_GF = df_GF.fillna(0)
    list_GFR = df_GF.grr
    list_GFB = df_GF.grb
    list_t = df_GF.t

    ax_.scatter(x=list_GFB, y=list_t, s=8, c='darkgreen')
    ax_.plot(list_GFB, list_t, c='darkgreen', linewidth=0.5, label='Caulinaire')
    ax_.axhline(y=11, xmin=min(list_GFB), xmax=max(list_GFB), c='darkgreen')
    ax_.scatter(x=list_GFR, y=list_t, s=8, c='darkred')
    ax_.plot(list_GFR, list_t, c='darkred',  linewidth=0.5, label='Racinaire')
    ax_.axhline(y=11, xmin=min(list_GFR), xmax=max(list_GFR), c='darkred')

    ax_.fill_between(x=[min(list_GFB), max(list_GFB)], y1=11, y2=0, color='darkgreen', alpha=0.1)
    ax_.fill_between(x=[min(list_GFR), max(list_GFR)], y1=11, y2=0, color='darkred', alpha=0.1)
    ax_.set_xlabel('Facteurs de Croissance', fontsize=8)
    #ax_.set_title('Facteurs de Croissance', fontsize=8, fontstyle='italic')
    if csv_name == 'GR_W2_L1.csv' :
        ax_.legend(fontsize=6)

    ax_.set_xticks(np.asarray([0, round(min(list_GFR),3), round(max(list_GFR),3), round(min(list_GFB),3), round(max(list_GFB),3), 1]))
    ax_.set_yticks(np.asarray([0,5,10]))
    ax_.set_yticklabels([0,5,10], fontsize = 8)
    ax_.set_xticklabels([0, round(min(list_GFR),3), round(max(list_GFR),3), round(min(list_GFB),3), round(max(list_GFB),3), 1], fontsize=6, fontweight='bold', rotation=45)

    # plt.setp(ax_.get_xticklabels(), fontsize=8, fontweight='bold')
def trace_Carbone(ax_, path_to_csv, csv_name) :
    
    df_GF = pd.read_csv(''.join([path_to_csv, csv_name]))
    df_GF = df_GF.fillna(0)
    list_C = df_GF.C
    list_CumC = np.cumsum(list_C)
    list_t = df_GF.t

    ax_.scatter(x=list_C, y=list_t, s=8, c='sienna', label='Assimilation à t')
    ax_.plot(list_CumC, list_t , c='sienna', linewidth=2, label='Assimilation cumulée')
    ax_.fill_betweenx(y=list_t, x1=list_C, x2=0, color='sienna')
    ax_.set_xlabel('Carbone assimilé', fontsize=8, fontstyle='italic')

    ax_.set_xticks(np.asarray([0, round(max(list_CumC),4)]))
    ax_.set_xticklabels([0, round(max(list_CumC),4)], fontsize=8, fontweight='bold')

def trace_Eau(ax_, path_to_csv, csv_name) :
    
    df_GF = pd.read_csv(''.join([path_to_csv, csv_name]))
    df_GF = df_GF.fillna(0)
    list_H2O = df_GF.H2O
    list_CumH2O = np.cumsum(list_H2O)
    list_t = df_GF.t

    ax_.scatter(x=list_H2O, y=list_t, s=8, c='darkblue', label='Absorption à t')
    ax_.plot(list_CumH2O, list_t, c='darkblue', linewidth=2, label='Absorption cumulée')
    ax_.fill_betweenx(y=list_t, x1=list_H2O, x2=0, color='darkblue')
    ax_.set_xlabel('Eau absorbée', fontsize=8, fontstyle='italic')

    ax_.set_xticks(np.asarray([0, round(max(list_CumH2O),4)]))
    ax_.set_xticklabels([0, round(max(list_CumH2O),4)], fontsize=8, fontweight='bold')

def trace_Eau_et_Carbone(ax_, path_to_csv, csv_name):
    
    df_GF = pd.read_csv(''.join([path_to_csv, csv_name]))
    df_GF = df_GF.fillna(0)
    list_C = df_GF.C
    list_CumC = np.cumsum(list_C)
    list_H2O = df_GF.H2O*(-1)
    list_CumH2O = np.cumsum(list_H2O)
    list_t = df_GF.t
    
    ax_.axvline(x=0, ymin=0, ymax=max(list_CumC), color='k', linestyle='--')

    ax_.scatter(x=list_C, y=list_t, s=8, c='sienna')
    ax_.plot(list_CumC, list_t , c='sienna', linewidth=2, label='Assimilation C')
    ax_.fill_betweenx(y=list_t, x1=list_C, x2=0, color='sienna')
    ax_.scatter(x=list_H2O, y=list_t, s=8, c='darkblue')
    ax_.plot(list_CumH2O, list_t, c='darkblue', linewidth=2, label='Absorption H20')
    ax_.fill_betweenx(y=list_t, x1=list_H2O, x2=0, color='darkblue')

    ax_.set_xticks(np.asarray([round(min(list_CumH2O),2), 0, round(max(list_CumC),2)]))
    ax_.set_xticklabels([(-1)*round(min(list_CumH2O),2), 0, round(max(list_CumC),2)], fontsize=8, fontweight='bold')
    ax_.set_yticks([0, 5, 10])
    ax_.set_yticklabels([0,5,10], fontsize=8)
    if csv_name != 'GR_W2_L1.csv' :
        ax_.legend(fontsize=6)

def trace_PE(ax_, path_to_image, image_name) :

    img = mpimg.imread(os.path.join(path_to_image, image_name))
    ax_.imshow(img)
    ax_.get_xaxis().set_visible(False)
    ax_.get_yaxis().set_visible(False)
    ax_.axis('off')
    #ax_.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

def trace_SR(ax_, path_to_image, image_name) :

    img = mpimg.imread(os.path.join(path_to_image, image_name))
    ax_.imshow(img)
    ax_.get_xaxis().set_visible(False)
    ax_.get_yaxis().set_visible(False)
    ax_.axis('off')

def trace_SC(ax_, path_to_image, image_name) :

    img = mpimg.imread(os.path.join(path_to_image, image_name))
    ax_.imshow(img)
    ax_.get_xaxis().set_visible(False)
    ax_.get_yaxis().set_visible(False)
    ax_.axis('off')

def trace_one_step(fig, gs, path_to_image, path_to_csv, i, j, PE, SR, SC, GR) :
    ax_PE = fig.add_subplot(gs[j:j+3, i:i+3])
    trace_PE(ax_PE, path_to_image, PE)
    #ax_SC = fig.add_subplot(gs[j, i+2])
    #trace_SC(ax_SC, path_to_image, SC)
    #ax_SR = fig.add_subplot(gs[j, i+3])
    #trace_SR(ax_SR, path_to_image, SR)
    ax_GR = fig.add_subplot(gs[j+1:j+3, i+3:i+5])
    trace_Both_Growth_Factor(ax_GR, path_to_csv, GR)
    #ax_Eau = fig.add_subplot(gs[j+1:j+3, i+4])
    #trace_Eau(ax_Eau, path_to_csv, GR)
    #ax_Carbone = fig.add_subplot(gs[j+1:j+3, i+5])
    #trace_Carbone(ax_Carbone, path_to_csv, GR)
    ax_Var = fig.add_subplot(gs[j+1:j+3, i+5:i+7])
    trace_Eau_et_Carbone(ax_Var, path_to_csv, GR)

