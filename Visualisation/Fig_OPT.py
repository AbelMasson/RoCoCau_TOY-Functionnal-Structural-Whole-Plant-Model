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

def trace_fig_OPT2(path_to_image, path_to_csv) :
    fig_OPT = plt.figure(constrained_layout=True, figsize=(21, 10))
    gs = fig_OPT.add_gridspec(10, 21, wspace=0.05)

    #x = [i/100 for i in range(100)]
    #y = [1 - (i/100) for i in range(100)]
    #fig_OPT_ax1 = fig_OPT.add_subplot(gs[0, 0])
    #fig_OPT_ax1.plot(x, y, color='k', linewidth=2)
    #fig_OPT_ax1.text(0.1, 0.1, 'Water \n Conditions', fontweight='bold')
    #fig_OPT_ax1.text(0.6, 0.6, 'Light \n Conditions', fontweight='bold')
    #fig_OPT_ax1.axis('off')
    
    lj = [0,3,6]
    li = [0,7,14]
    l_Water=[0.6,0.8,0.99]
    l_Light=[0.5, 0.75, 1]
    for j in [0, 3, 6] :
        for i in [0, 7, 14] :
            ax = fig_OPT.add_subplot(gs[lj[int(j/3)], li[int(i/7)]:li[int(i/7)]+7])
            props = dict(boxstyle='round', facecolor='blue', alpha=0.2, ec='k')
            textstr = 'Water = {}'.format(l_Water[int(j/3)]) + ' / ' + 'Light = {}'.format(l_Light[int(i/7)])
            ax.text(0.6, 0.3, textstr, fontsize=10, fontweight='bold', bbox=props)
            ax.axis('off')
    '''
    for i, param_value in enumerate([0.6,0.8,0.99]) :
        for k in range(3) :
            ax = fig_OPT.add_subplot(gs[lj[i], li[k]+3:li[k]+5])
            ax.text(x=0, y=0.3, s='Water = {}'.format(param_value), fontsize=10, fontweight='bold')
            ax.axis('off')

    for i, param_value in enumerate([0.5, 0.75, 1]) :
        for k in range(3) :
            ax = fig_OPT.add_subplot(gs[lj[k], li[i]+5:li[i]+7])
            ax.text(x=0, y=0.3, s='Light = {}'.format(param_value), fontsize=10, fontweight='bold')
            ax.axis('off')
    '''    
    ID = 0
    l_PE = ['PE_W2_L1.png', 'PE_W2_L2.png', 'PE_W2_L3.png', 'PE_W3_L1.png', 'PE_W3_L2.png', 'PE_W3_L3.png', 'PE_W4_L1.png', 'PE_W4_L2.png', 'PE_W4_L3.png']
    l_SR = ['SR_W2_L1.png', 'SR_W2_L2.png', 'SR_W2_L3.png', 'SR_W3_L1.png', 'SR_W3_L2.png', 'SR_W3_L3.png', 'SR_W4_L1.png', 'SR_W4_L2.png', 'SR_W4_L3.png']
    l_SC = ['SC_W2_L1.png', 'SC_W2_L2.png', 'SC_W2_L3.png', 'SC_W3_L1.png', 'SC_W3_L2.png', 'SC_W3_L3.png', 'SC_W4_L1.png', 'SC_W4_L2.png', 'SC_W4_L3.png']
    l_GR = ['GR_W2_L1.csv', 'GR_W2_L2.csv', 'GR_W2_L3.csv', 'GR_W3_L1.csv', 'GR_W3_L2.csv', 'GR_W3_L3.csv', 'GR_W4_L1.csv', 'GR_W4_L2.csv', 'GR_W4_L3.csv']

    for j in [0, 3, 6] :
        for i in [0, 7, 14] :
            trace_one_step(fig=fig_OPT, gs=gs, path_to_image=path_to_image, path_to_csv=path_to_csv, i=i, j=j, PE=l_PE[ID], SR=l_SR[ID], SC=l_SC[ID], GR=l_GR[ID])
            ID += 1
    #plt.suptitle('Impact de la disponibilité des ressources sur la croissance des plantes' + '\n' + 'selon la théorie du partitionnement optimal des ressources simulée par TOY')
    fig_OPT.savefig('/home/abel/Desktop/Fig_OPT/fig_OPT2_sans_titre.png')
    #plt.show()

def trace_fig_OPT(path_to_image) :

    fig_OPT = plt.figure(constrained_layout=True, figsize=(20, 12))
    gs = fig_OPT.add_gridspec(7, 7)

    x = [i/100 for i in range(100)]
    y = [1 - (i/100) for i in range(100)]
    fig_OPT_ax1 = fig_OPT.add_subplot(gs[0, 0])
    fig_OPT_ax1.plot(x, y, color='k', linewidth=2)
    fig_OPT_ax1.text(0.1, 0.1, 'Water \n Conditions', fontweight='bold')
    fig_OPT_ax1.text(0.6, 0.6, 'Light \n Conditions', fontweight='bold')
    fig_OPT_ax1.axis('off')

    for i, param_value in enumerate([0.6,0.8,0.99]) :
        ax = fig_OPT.add_subplot(gs[(2*i+1):(2*i+3), 0])
        ax.text(x=0.2, y=0.2, s='Water = {}'.format(param_value), fontsize=14, fontweight='bold', rotation=90)
        ax.axis('off')

    for i, param_value in enumerate([0.5, 0.75, 1]) :
        ax = fig_OPT.add_subplot(gs[0, (2*i+1):(2*i+3)])
        ax.text(x=0.4, y=0.4, s='Light = {}'.format(param_value), fontsize=14, fontweight='bold')
        ax.axis('off')

    for i, fig_list in enumerate([['PE_W2_L1.png', 'PE_W2_L2.png', 'PE_W2_L3.png'],
                                  ['PE_W3_L1.png', 'PE_W3_L2.png', 'PE_W3_L3.png'],
                                  ['PE_W4_L1.png', 'PE_W4_L2.png', 'PE_W4_L3.png']]) :
        for j in range(3) :
            ax = fig_OPT.add_subplot(gs[(2*i+1), 2*(j+1)])
            trace_PE(ax, path_to_image, image_name=fig_list[j])

    for i, fig_list in enumerate([['SR_W2_L1.png', 'SR_W2_L2.png', 'SR_W2_L3.png'],
                                  ['SR_W3_L1.png', 'SR_W3_L2.png', 'SR_W3_L3.png'],
                                  ['SR_W4_L1.png', 'SR_W4_L2.png', 'SR_W4_L3.png']]) :
        for j in range(3) :
            ax = fig_OPT.add_subplot(gs[(2*i+1),(2*j)+1])
            trace_SR(ax, path_to_image, image_name=fig_list[j])

    for i, fig_list in enumerate([['SC_W2_L1.png', 'SC_W2_L2.png', 'SC_W2_L3.png'],
                                  ['SC_W3_L1.png', 'SC_W3_L2.png', 'SC_W3_L3.png'],
                                  ['SC_W4_L1.png', 'SC_W4_L2.png', 'SC_W4_L3.png']]):
        for j in range(3) :
            ax = fig_OPT.add_subplot(gs[2*(i+1), (2*j)+1])
            trace_SC(ax, path_to_image, image_name=fig_list[j])

    for i, fig_list in enumerate([['GR_W2_L1.csv', 'GR_W2_L2.csv', 'GR_W2_L3.csv'],
                                  ['GR_W3_L1.csv', 'GR_W3_L2.csv', 'GR_W3_L3.csv'],
                                  ['GR_W4_L1.csv', 'GR_W4_L2.csv', 'GR_W4_L3.csv']]):
        for j in range(3) :
            ax = fig_OPT.add_subplot(gs[2*(i+1), 2*(j+1)])
            trace_Both_Growth_Factor(ax, path_to_image, csv_name=fig_list[j])
            if i == 0 and j == 0 :
                ax.legend(fontsize='xx-small')

    fig_OPT.savefig('/home/abel/Desktop/Fig_OPT/fig_OPT.png')
    #plt.show()

def trace_scenarios_with_example_with_GF_Branch() :
    fig3 = plt.figure(constrained_layout=True, figsize=(20,12))
    gs = fig3.add_gridspec(4, 8)

    f3_ax1 = fig3.add_subplot(gs[0, 0:2])
    trace(f3_ax1, Sm=0.1, Sr=0.2, Al=0.9, axe_type='Insensible', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Insensible.csv')

    f3_ax2 = fig3.add_subplot(gs[0, 2:4])
    trace(f3_ax2, Sm=0.5, Sr=0.6, Al=0.9, axe_type='Sensible Mort', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_Mort.csv')

    f3_ax3 = fig3.add_subplot(gs[0, 4:6])
    trace(f3_ax3, Sm=0.1, Sr=0.2, Al=0.2, axe_type='Sensible Attenuation', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_Att.csv')

    f3_ax4 = fig3.add_subplot(gs[0, 6:8])
    trace(f3_ax4, Sm=0.1, Sr=0.5, Al=0.9, axe_type='Sensible Ramification', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_Ram.csv')

    f3_ax5 = fig3.add_subplot(gs[1, 0])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_insensible.png')
    f3_ax5.imshow(img)
    f3_ax5.get_xaxis().set_visible(False)
    f3_ax5.get_yaxis().set_visible(False)
    f3_ax5.axis('off')
    f3_ax5.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax6 = fig3.add_subplot(gs[1, 1])
    trace_Growth_Factor(f3_ax6, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Insensible.csv', Sm=0.1, Sr=0.2)

    f3_ax7 = fig3.add_subplot(gs[1, 2])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_Mort.png')
    f3_ax7.imshow(img)
    f3_ax7.get_xaxis().set_visible(False)
    f3_ax7.get_yaxis().set_visible(False)
    f3_ax7.axis('off')
    f3_ax7.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax8 = fig3.add_subplot(gs[1, 3])
    trace_Growth_Factor(f3_ax8, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_Mort.csv', Sm=0.5, Sr=0.6)

    f3_ax9 = fig3.add_subplot(gs[1, 4])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_Att.png')
    f3_ax9.imshow(img)
    f3_ax9.get_xaxis().set_visible(False)
    f3_ax9.get_yaxis().set_visible(False)
    f3_ax9.axis('off')
    f3_ax9.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax10 = fig3.add_subplot(gs[1, 5])
    trace_Growth_Factor(f3_ax10, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_Att.csv', Sm=0.1, Sr=0.2)

    f3_ax11 = fig3.add_subplot(gs[1, 6])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_Ram.png')
    f3_ax11.imshow(img)
    f3_ax11.get_xaxis().set_visible(False)
    f3_ax11.get_yaxis().set_visible(False)
    f3_ax11.axis('off')
    f3_ax11.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax12 = fig3.add_subplot(gs[1, 7])
    trace_Growth_Factor(f3_ax12, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_Ram.csv', Sm=0.1, Sr=0.5)

    f3_ax13 = fig3.add_subplot(gs[2, 0:2])
    trace(f3_ax13, Sm=0.5, Sr=0.6, Al=0.2, axe_type='Sensible Mort&Attenuation', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_AttMort.csv')

    f3_ax14 = fig3.add_subplot(gs[2, 2:4])
    trace(f3_ax14, Sm=0.5, Sr=0.9, Al=0.9, axe_type='Sensible Mort&Ramification', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_RamMort.csv')

    f3_ax15 = fig3.add_subplot(gs[2, 4:6])
    trace(f3_ax15, Sm=0.1, Sr=0.5, Al=0.2, axe_type='Sensible Attenuation&Ramification', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_AttRam.csv')

    f3_ax16 = fig3.add_subplot(gs[2, 6:8])
    trace(f3_ax16, Sm=0.5, Sr=0.9, Al=0.2, axe_type='Sensible Attenuation&Ramification&Mort', path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_AttRamMort.csv')

    f3_ax17 = fig3.add_subplot(gs[3, 0])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_AttMort.png')
    f3_ax17.imshow(img)
    f3_ax17.get_xaxis().set_visible(False)
    f3_ax17.get_yaxis().set_visible(False)
    f3_ax17.axis('off')
    f3_ax17.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax18 = fig3.add_subplot(gs[3, 1])
    trace_Growth_Factor(f3_ax18, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_AttMort.csv', Sm=0.5, Sr=0.6)

    f3_ax19 = fig3.add_subplot(gs[3, 2])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_RamMort.png')
    f3_ax19.imshow(img)
    f3_ax19.get_xaxis().set_visible(False)
    f3_ax19.get_yaxis().set_visible(False)
    f3_ax19.axis('off')
    f3_ax19.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax20 = fig3.add_subplot(gs[3, 3])
    trace_Growth_Factor(f3_ax20, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_RamMort.csv', Sm=0.5, Sr=0.9)

    f3_ax21 = fig3.add_subplot(gs[3, 4])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_AttRam.png')
    f3_ax21.imshow(img)
    f3_ax21.get_xaxis().set_visible(False)
    f3_ax21.get_yaxis().set_visible(False)
    f3_ax21.axis('off')
    f3_ax21.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax22 = fig3.add_subplot(gs[3, 5])
    trace_Growth_Factor(f3_ax22, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_AttRam.csv', Sm=0.1, Sr=0.5)

    f3_ax23 = fig3.add_subplot(gs[3, 6])
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_AttRamMort.png')
    f3_ax23.imshow(img)
    f3_ax23.get_xaxis().set_visible(False)
    f3_ax23.get_yaxis().set_visible(False)
    f3_ax23.axis('off')
    f3_ax23.text(250, 600, 'water=0.69 \n lum=0.75', fontsize=8)

    f3_ax24 = fig3.add_subplot(gs[3, 7])
    trace_Growth_Factor(f3_ax24, path_to_csv='/home/abel/Desktop/CSV_growth/', csv_name='FC_AL_Sens_AttRamMort.csv', Sm=0.5, Sr=0.9)

    #fig3.suptitle("Huit modalités types de réponse à un stress environnemental, \n Exemple de réponse des axes longs du système caulinaire",
    #    fontsize=10, fontweight='bold', y=0.99)
    fig3.tight_layout()

    plt.savefig('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Huit_Modalite_examples_with_FC_branch3_sans_titre.png')
    plt.show()
    
if __name__ == '__main__' :
    trace_scenarios_with_example_with_GF_Branch()
