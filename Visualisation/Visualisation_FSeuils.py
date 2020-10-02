# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Script pour visualiser les seuils.
TODO : REVOIR LES LABELS DES DIFFERENTES MODALITES, ILS SONT UN PEU DIFFICILE A EXPLIQUER (A FORTIORI A COMPRENDRE)
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import pandas as pd

def trace_Growth_Factor(ax_, path_to_csv, csv_name, Sm, Sr) :
    df_GF = pd.read_csv(''.join([path_to_csv, csv_name]))
    list_GF = df_GF.grr
    list_t = df_GF.t

    ax_.axvline(x=Sm, ymin=0, ymax=1, linestyle='--', color='grey')
    ax_.axvline(x=Sr, ymin=0, ymax=1, linestyle='--', color='grey')
    ax_.axhline(y=11, xmin=min(list_GF), xmax=max(list_GF), color='darkblue')

    ax_.scatter(x=list_GF, y=list_t, )
    ax_.set_xlabel('Facteur de Croissance', fontsize=8)
    ax_.set_title('Evolution du Facteur de Croissance', fontsize=8, fontstyle='italic')

    ax_.set_xticks(np.asarray([0, Sm, Sr, 1]))
    ax_.set_xticklabels([0,'Sm','Sr', 1])

    plt.setp(ax_.get_xticklabels(), fontsize=8, fontweight='bold')

def trace(ax_, Sm, Sr, Al, axe_type, path_to_csv, csv_name) :

    df_GF = pd.read_csv(''.join([path_to_csv, csv_name]))
    list_GF = df_GF.grr

    n_points = 200

    x_GF = np.linspace(min(list_GF), max(list_GF), int((max(list_GF) - min(list_GF)) * n_points))

    ax_.axvline(x=Sm, ymin=0, ymax=1, linestyle='--', color='grey')
    ax_.axvline(x=Sr, ymin=0, ymax=1, linestyle='--', color='grey')
    ax_.axhline(y=Al, xmin=0, xmax=Sr, linestyle='--', color='grey')
    ax_.axhline(y=1.1, xmin=min(list_GF), xmax=max(list_GF), color='darkblue')

    #ax_.axvspan(Sr, 1, alpha=0.2, color='green')
    #ax_.axvspan(Sm, Sr, alpha=0.2, color='orange')
    #ax_.axvspan(0, Sm, alpha=0.2, color='red')
    
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
    ax_.plot(np.linspace(0, 1, len(line)), line, color='red', linewidth=2)
    ax_.fill_between(x_GF, y1=[line[int(i*n_points)] + 0.05 for i in x_GF], y2=1.1, alpha=0.2, color='darkblue')

    ax_.set_xticks(np.asarray([0, Sm, Sr, 1]))
    ax_.set_yticks(np.asarray([0, Al, 1]))
    ax_.set_xticklabels(['0', 'Sm = '+str(Sm), 'Sr = '+str(Sr), '1'])
    ax_.set_yticklabels(['0', 'Al = '+str(Al), '1'])

    plt.setp(ax_.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor", fontsize=8, fontweight='bold')
    plt.setp(ax_.get_yticklabels(),rotation=45, ha="right",
             rotation_mode="anchor", fontsize=8, fontweight='bold')

    ax_.set_title(axe_type, fontsize=8, fontweight='bold')

def trace_scenarios() :
    fig, axs = plt.subplots(2, 4, sharex = False, sharey = False, figsize=(12,6))

    trace(axs[0, 0], Sm=0.1, Sr=0.2, Al=0.9, axe_type='Insensible')
    #axs[0, 0].text(0.7, 0.5, 'Sm=0.1 \n Sr=0.2 \n Al=0.9', fontsize=8)
    trace(axs[0, 1], Sm=0.5, Sr=0.6, Al=0.9, axe_type='Sensible Mort')
    #axs[0, 1].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.6 \n Al=0.9', fontsize=8)
    trace(axs[0, 2], Sm=0.1, Sr=0.2, Al=0.2, axe_type='Sensible Attenuation')
    #axs[0, 2].text(0.7, 0.2, 'Sm=0.1 \n Sr=0.2 \n Al=0.2', fontsize=8)
    trace(axs[1, 0], Sm=0.1, Sr=0.5, Al=0.9, axe_type='Sensible Ramification')
    #axs[1, 0].text(0.7, 0.5, 'Sm=0.1 \n Sr=0.5 \n Al=0.9', fontsize=8)

    trace(axs[0, 3], Sm=0.5, Sr=0.6, Al=0.2, axe_type='Sensible Mort&Attenuation')
    #axs[0, 3].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.6 \n Al=0.2', fontsize=8)
    trace(axs[1, 1], Sm=0.5, Sr=0.9, Al=0.9, axe_type='Sensible Mort&Ramification')
    #axs[1, 1].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.9 \n Al=0.9', fontsize=8)
    trace(axs[1, 2], Sm=0.1, Sr=0.5, Al=0.2, axe_type='Sensible Attenuation&Ramification')
    #axs[1, 2].text(0.7, 0.1, 'Sm=0.1 \n Sr=0.5 \n Al=0.2', fontsize=8)
    trace(axs[1, 3], Sm=0.5, Sr=0.9, Al=0.2, axe_type='Sensible Attenuation&Ramification&Mort')
    #axs[1, 3].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.9 \n Al=0.2', fontsize=8)

    fig.suptitle("Huit modalités types de réponse à un stress environnemental", fontsize=10, fontweight='bold')
    fig.tight_layout()

    plt.savefig('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Huit_Modalite.png')
    plt.show()

def trace_scenarios_with_example_latroot() :
    fig, axs = plt.subplots(4, 4, sharex = False, sharey = False, figsize=(12,12))

    trace(axs[0, 0], Sm=0.1, Sr=0.2, Al=0.9, axe_type='Insensible')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Insensible_root.png')
    axs[1,0].imshow(img)
    axs[1,0].get_xaxis().set_visible(False)
    axs[1,0].get_yaxis().set_visible(False)
    axs[1,0].axis('off')
    axs[1, 0].text(800, 800, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[0, 0].text(0.7, 0.5, 'Sm=0.1 \n Sr=0.2 \n Al=0.9', fontsize=8)
    trace(axs[0, 1], Sm=0.5, Sr=0.6, Al=0.9, axe_type='Sensible Mort')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Sens_Mort_root.png')
    axs[1, 1].imshow(img)
    axs[1, 1].get_xaxis().set_visible(False)
    axs[1, 1].get_yaxis().set_visible(False)
    axs[1, 1].axis('off')
    axs[1, 1].text(600, 800, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[0, 1].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.6 \n Al=0.9', fontsize=8)
    trace(axs[0, 2], Sm=0.1, Sr=0.2, Al=0.2, axe_type='Sensible Attenuation')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Sens_Att_root.png')
    axs[1, 2].imshow(img)
    axs[1, 2].get_xaxis().set_visible(False)
    axs[1, 2].get_yaxis().set_visible(False)
    axs[1, 2].axis('off')
    axs[1, 2].text(600, 800, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[0, 2].text(0.7, 0.2, 'Sm=0.1 \n Sr=0.2 \n Al=0.2', fontsize=8)
    trace(axs[2, 0], Sm=0.1, Sr=0.5, Al=0.9, axe_type='Sensible Ramification')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Sens_Ram_root.png')
    axs[3, 0].imshow(img)
    axs[3, 0].get_xaxis().set_visible(False)
    axs[3, 0].get_yaxis().set_visible(False)
    axs[3, 0].axis('off')
    axs[3, 0].text(600, 800, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[1, 0].text(0.7, 0.5, 'Sm=0.1 \n Sr=0.5 \n Al=0.9', fontsize=8)
    trace(axs[0, 3], Sm=0.5, Sr=0.6, Al=0.2, axe_type='Sensible Mort&Attenuation')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Sens_AttMort_root.png')
    axs[1, 3].imshow(img)
    axs[1, 3].get_xaxis().set_visible(False)
    axs[1, 3].get_yaxis().set_visible(False)
    axs[1, 3].axis('off')
    axs[1, 3].text(600, 800, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[0, 3].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.6 \n Al=0.2', fontsize=8)
    trace(axs[2, 1], Sm=0.5, Sr=0.9, Al=0.9, axe_type='Sensible Mort&Ramification')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Sens_RamMort_root.png')
    axs[3, 1].imshow(img)
    axs[3, 1].get_xaxis().set_visible(False)
    axs[3, 1].get_yaxis().set_visible(False)
    axs[3, 1].axis('off')
    axs[3, 1].text(600, 800, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[1, 1].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.9 \n Al=0.9', fontsize=8)
    trace(axs[2, 2], Sm=0.1, Sr=0.5, Al=0.2, axe_type='Sensible Attenuation&Ramification')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Sens_AttRam_root.png')
    axs[3, 2].imshow(img)
    axs[3, 2].get_xaxis().set_visible(False)
    axs[3, 2].get_yaxis().set_visible(False)
    axs[3, 2].axis('off')
    axs[3, 2].text(600, 800, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[1, 2].text(0.7, 0.1, 'Sm=0.1 \n Sr=0.5 \n Al=0.2', fontsize=8)
    trace(axs[2, 3], Sm=0.5, Sr=0.9, Al=0.2, axe_type='Sensible Attenuation&Ramification&Mort')
    img = mpimg.imread('/home/abel/Desktop/Sens_LatRoot_Simu3/Sens_AttRamMort_root.png')
    axs[3, 3].imshow(img)
    axs[3, 3].get_xaxis().set_visible(False)
    axs[3, 3].get_yaxis().set_visible(False)
    axs[3, 3].axis('off')
    axs[3, 3].text(600, 800, 'water=0.69 \n lum=0.75', fontsize=8)
    #axs[1, 3].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.9 \n Al=0.2', fontsize=8)

    fig.suptitle("Huit modalités types de réponse à un stress environnemental, \n Exemple de réponse des axes secondaires du système racinaire", fontsize=10, fontweight='bold', y=0.99)
    fig.tight_layout()

    plt.savefig('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Huit_Modalite_examples_root.png')
    plt.show()

def trace_scenarios_with_example_Branch() :
    fig, axs = plt.subplots(4, 4, sharex = False, sharey = False, figsize=(12,12))

    trace(axs[0, 0], Sm=0.1, Sr=0.2, Al=0.9, axe_type='Insensible')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_insensible.png')
    axs[1,0].imshow(img)
    axs[1,0].get_xaxis().set_visible(False)
    axs[1,0].get_yaxis().set_visible(False)
    axs[1,0].axis('off')
    axs[1, 0].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)

    trace(axs[0, 1], Sm=0.5, Sr=0.6, Al=0.9, axe_type='Sensible Mort')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_Mort.png')
    axs[1, 1].imshow(img)
    axs[1, 1].get_xaxis().set_visible(False)
    axs[1, 1].get_yaxis().set_visible(False)
    axs[1, 1].axis('off')
    axs[1, 1].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[0, 1].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.6 \n Al=0.9', fontsize=8)
    trace(axs[0, 2], Sm=0.1, Sr=0.2, Al=0.2, axe_type='Sensible Attenuation')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_Att.png')
    axs[1, 2].imshow(img)
    axs[1, 2].get_xaxis().set_visible(False)
    axs[1, 2].get_yaxis().set_visible(False)
    axs[1, 2].axis('off')
    axs[1, 2].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[0, 2].text(0.7, 0.2, 'Sm=0.1 \n Sr=0.2 \n Al=0.2', fontsize=8)
    trace(axs[2, 0], Sm=0.1, Sr=0.5, Al=0.9, axe_type='Sensible Ramification')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_Ram.png')
    axs[3, 0].imshow(img)
    axs[3, 0].get_xaxis().set_visible(False)
    axs[3, 0].get_yaxis().set_visible(False)
    axs[3, 0].axis('off')
    axs[3, 0].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[1, 0].text(0.7, 0.5, 'Sm=0.1 \n Sr=0.5 \n Al=0.9', fontsize=8)
    trace(axs[0, 3], Sm=0.5, Sr=0.6, Al=0.2, axe_type='Sensible Mort&Attenuation')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_AttMort.png')
    axs[1, 3].imshow(img)
    axs[1, 3].get_xaxis().set_visible(False)
    axs[1, 3].get_yaxis().set_visible(False)
    axs[1, 3].axis('off')
    axs[1, 3].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[0, 3].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.6 \n Al=0.2', fontsize=8)
    trace(axs[2, 1], Sm=0.5, Sr=0.9, Al=0.9, axe_type='Sensible Mort&Ramification')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_RamMort.png')
    axs[3, 1].imshow(img)
    axs[3, 1].get_xaxis().set_visible(False)
    axs[3, 1].get_yaxis().set_visible(False)
    axs[3, 1].axis('off')
    axs[3, 1].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[1, 1].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.9 \n Al=0.9', fontsize=8)
    trace(axs[2, 2], Sm=0.1, Sr=0.5, Al=0.2, axe_type='Sensible Attenuation&Ramification')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_AttRam.png')
    axs[3, 2].imshow(img)
    axs[3, 2].get_xaxis().set_visible(False)
    axs[3, 2].get_yaxis().set_visible(False)
    axs[3, 2].axis('off')
    axs[3, 2].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)

    #axs[1, 2].text(0.7, 0.1, 'Sm=0.1 \n Sr=0.5 \n Al=0.2', fontsize=8)
    trace(axs[2, 3], Sm=0.5, Sr=0.9, Al=0.2, axe_type='Sensible Attenuation&Ramification&Mort')
    img = mpimg.imread('/home/abel/Desktop/Sensibilité_Branch_Simu/AL_Sens_AttRamMort.png')
    axs[3, 3].imshow(img)
    axs[3, 3].get_xaxis().set_visible(False)
    axs[3, 3].get_yaxis().set_visible(False)
    axs[3, 3].axis('off')
    axs[3, 3].text(300, 400, 'water=0.69 \n lum=0.75', fontsize=8)
    #axs[1, 3].text(0.1, 0.5, 'Sm=0.5 \n Sr=0.9 \n Al=0.2', fontsize=8)

    fig.suptitle("Huit modalités types de réponse à un stress environnemental, \n Exemple de réponse des axes longs du système caulinaire", fontsize=10, fontweight='bold', y=0.99)
    fig.tight_layout()

    plt.savefig('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Huit_Modalite_examples_branch.png')
    plt.show()

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

    fig3.suptitle("Huit modalités types de réponse à un stress environnemental, \n Exemple de réponse des axes longs du système caulinaire",
        fontsize=10, fontweight='bold', y=0.99)
    fig3.tight_layout()

    plt.savefig('/home/abel/Desktop/VoxNet_Strat_Sauvegarde/Huit_Modalite_examples_with_FC_branch3.png')
    #plt.show()

def trace_strat() :
    
    fig, axs = plt.subplots(2,3, sharex=True, sharey=True)
    
    trace(axs[0,0], Sm=0.2, Sr=0.3, Al=0.5, axe_type='Trunk')
    trace(axs[0,1], Sm=0.8, Sr=0.9, Al=0.5, axe_type='LongShoot')
    trace(axs[0,2], Sm=0.5, Sr=0.5, Al=0.5, axe_type='ShortShoot')
    
    trace(axs[1,0], Sm=0.2, Sr=0.3, Al=0.5, axe_type='TapRoot')
    trace(axs[1,1], Sm=0.8, Sr=0.9, Al=0.5, axe_type='LatRoot')
    trace(axs[1,2], Sm=0.5, Sr=0.5, Al=0.5, axe_type='FineRoot')
    
    fig.suptitle('Stratégie Pionnière')
    
    fig, axs = plt.subplots(2,3, sharex=True, sharey=True)
    
    trace(axs[0,0], Sm=0.8, Sr=0.9, Al=0.5, axe_type='Trunk')
    trace(axs[0,1], Sm=0.2, Sr=0.3, Al=0.5, axe_type='LongShoot')
    trace(axs[0,2], Sm=0.5, Sr=0.5, Al=0.5, axe_type='ShortShoot')
    
    trace(axs[1,0], Sm=0.8, Sr=0.9, Al=0.5, axe_type='TapRoot')
    trace(axs[1,1], Sm=0.2, Sr=0.3, Al=0.5, axe_type='LatRoot')
    trace(axs[1,2], Sm=0.5, Sr=0.5, Al=0.5, axe_type='FineRoot')
    
    fig.suptitle('Stratégie Conservatrice')
    
    fig, axs = plt.subplots(2,3, sharex=True, sharey=True)
    
    trace(axs[0,0], Sm=0.3, Sr=0.4, Al=0.5, axe_type='Trunk')
    trace(axs[0,1], Sm=0.3, Sr=0.4, Al=0.5, axe_type='LongShoot')
    trace(axs[0,2], Sm=0.1, Sr=0.1, Al=0.5, axe_type='ShortShoot')
    
    trace(axs[1,0], Sm=0.3, Sr=0.4, Al=0.5, axe_type='TapRoot')
    trace(axs[1,1], Sm=0.3, Sr=0.4, Al=0.5, axe_type='LatRoot')
    trace(axs[1,2], Sm=0.1, Sr=0.1, Al=0.5, axe_type='FineRoot')
    
    fig.suptitle('Stratégie Equilibre')
    fig.show()

def trace_trunk_all() :
    #TODO : Placer les noms des paramètres en abcisse et en ordonnée
    index = 0
    for Sm in [1, 3, 5, 7, 9] :
        for Sr in range(Sm+1,10,2) :
            for Al in range(0,10,3) :
                
                fig, ax_ = plt.subplots(1,1, sharex=True, sharey=True)
                
                trace(ax_, Sm/10, Sr/10, Al/10, axe_type='Trunk')
                
                fig.savefig('/home/lenovo/Bureau/Jeu_paramètres_tronc/Param_Tronc_{}.png'.format(index))
                
                index += 1

import fileinput
import sys

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

import shutil

def Generate_parameter_files_trunk() :
    index = 0
    for Sm in [1, 3, 5, 7, 9] :
        for Sr in range(Sm+1,10,2) :
            for Al in range(0,10,3) :
                
                path = '/home/lenovo/amapsim/wholeplant/parameterexample'
                path_copy = '/home/lenovo/Bureau/Parameter_Examples/parameterexample{}'.format(index)
                shutil.copy(path, path_copy)
                
                replaceAll('/home/lenovo/Bureau/Parameter_Examples/parameterexample{}'.format(index),
                           'trunkDeathThreshold SingleValueParameter 0.1',
                           'trunkDeathThreshold SingleValueParameter {}'.format(Sm/10))
                
                replaceAll('/home/lenovo/Bureau/Parameter_Examples/parameterexample{}'.format(index),
                           'trunkRamificationThreshold SingleValueParameter 0.3',
                           'trunkRamificationThreshold SingleValueParameter {}'.format(Sr/10))
                
                replaceAll('/home/lenovo/Bureau/Parameter_Examples/parameterexample{}'.format(index),
                           'trunkAttenuation SingleValueParameter 0.8',
                           'trunkAttenuation SingleValueParameter {}'.format(Al/10))
                
                index+=1

def replace_axe(i, ParAx_names, id_ax, Sm, Sr, Al) :
    
    replaceAll('/home/lenovo/Bureau/Param_aleatoires/parameterexample{}'.format(i),
                   ParAx_names[id_ax][0] + ' SingleValueParameter 0.x',
                   ParAx_names[id_ax][0] +' SingleValueParameter {}'.format(Sm/10))
                               
    replaceAll('/home/lenovo/Bureau/Param_aleatoires/parameterexample{}'.format(i),
                   ParAx_names[id_ax][1] + ' SingleValueParameter 0.x',
                   ParAx_names[id_ax][1] +' SingleValueParameter {}'.format(Sr/10))
    
    replaceAll('/home/lenovo/Bureau/Param_aleatoires/parameterexample{}'.format(i),
                   ParAx_names[id_ax][2] + ' SingleValueParameter 0.x',
                   ParAx_names[id_ax][2] +' SingleValueParameter {}'.format(Al/10))

def Generate_random_parameter() :
    
    ParAx_names = [['trunkDeathThreshold','trunkRamificationThreshold', 'trunkAttenuation'],
     ['branchDeathThreshold','branchRamificationThreshold', 'branchAttenuation'],
     ['shortshootDeathThreshold','shortshootRamificationThreshold', 'shortshootAttenuation'],
     ['taprootDeathThreshold','taprootRamificationThreshold', 'taprootAttenuation'],
     ['lateralrootDeathThreshold','lateralrootRamificationThreshold', 'lateralrootAttenuation'],
     ['finerootDeathThreshold','finerootRamificationThreshold', 'finerootAttenuation']]
    
    Ax_order = ['Trunk', 'branch', 'shortshoot', 'taproot', 'lateralroot', 'fineroot']
    
    for i in range(20) :
        
        fig, axs = plt.subplots(2,3, sharex=True, sharey=True)
        
        path = '/home/lenovo/amapsim/wholeplant/parameterexample'
        path_copy = '/home/lenovo/Bureau/Param_aleatoires/parameterexample{}'.format(i)
        shutil.copy(path, path_copy)
        
        for j in range(6) :
            
            Sm = np.random.randint(1,10)
            Sr = np.random.randint(Sm,10)
            Al = np.random.randint(1,10)
            
            replace_axe(i, ParAx_names, j, Sm, Sr, Al)
            trace(ax_=axs[j//3][j%3], Sm=Sm/10, Sr=Sr/10, Al=Al/10, axe_type=Ax_order[j])
            
        fig.savefig('/home/lenovo/Bureau/AnimParamAleatoire/Param_aleatoire_{}.png'.format(i))
        
if __name__ == '__main__' :
    #trace_scenarios_with_example_Branch()
    #trace_scenarios_with_example_latroot()
    trace_scenarios_with_example_with_GF_Branch()






























