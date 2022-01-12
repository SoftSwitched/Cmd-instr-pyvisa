# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 11:14:11 2022

@author: ccolonna
"""
import numpy as np 
import time 
from v1 import *

"""
#####################PROGRAMME DE TEST FLYBACK AUX########################################
ALIM088 -> [0,130V] par pas de 2V -> Regarder quand l'alim aux démarre en fnct de la charge 
ALIM104 -> [0,300mA] par pas de 50mA -> On limite à 300mA pour des raisons thermiques 
MULTI062 -> Iin, mesure en DC seulement (FLYB après Filtre d'entrée)
MULTI061 -> Mesure de J22 V_AUX pour vérifier la qualité de l'alim aux (drivers pri)
OSCI015 -> Voie 1 : Tension aux bornes de Q1 
        -> Voie 2 : Tension base Q6 (comQ1)
        -> Voie 3 : Tension J16 (IN DRIV Q1)
        -> Voie 4 : Tension DR J20 
MULTI059 -> Tension de sortie voie principale (mesure AC et DC)
MULTI060 -> Tension en sortie de régulateur linéaire (VREG = J31)
"""
#Réglage Scope 
OSCI015.Display_chan(1,1)
OSCI015.Display_chan(2,1)
OSCI015.Display_chan(3,1)
OSCI015.Display_chan(4,1)

OSCI015.Timebase_set(5e-5,15e-6) # 1us/div, origine à 0 
OSCI015.Channel_set(1,50,0) # Chan1 50V/div, origin = 0V 
OSCI015.Channel_set(2,2,0) # Chan2 2V/div, origin = 0V 
OSCI015.Channel_set(2,2,0) # Chan3 2V/div, origin = 0V 
OSCI015.Channel_set(2,2,0) # Chan4 2V/div, origin = 0V 
OSCI015.Trigger_set (1, 10,1) # Chan1, 10V trig set to auto, Run mode

#Mise OFF des appareil 
ALIM088.Sup_OFF()
ALIM104.Load_OFF() 
ALIM088.Sup_prot_set(135,2, 100)
ALIM104.Load_prot_set(7,0.35,2)
ALIM088.Sup_val_set(0,0,20)
ALIM104.Load_val_set(0,0)

ALIM088.Sup_ON()
ALIM104.Load_ON() 

#Réglage des multis
MULTI062.Mult_set('CURR','DC')
MULTI061.Mult_set('VOLT','DC')
MULTI059.Mult_set('VOLT','DC') #Pour la première partie 
MULTI060.Mult_set('VOLT','DC')

Vin_range = np.linspace(8,130,61)
Iout_range= np.linspace(0,0.3,16)
Vin ,Iin , Vout_dc , Vout_ac ,Iout , Eff  , Vaux , Vreg , Scope_data = [],[],[],[],[],[],[],[],[]# same length as Vin range 
Vin_r, Iin_r, Vout_dcr, Vout_acr, Iout_r, Eff_r, Vaux_r, Vreg_r, data_r = [],[],[],[],[],[],[],[],[]

for v in Vin_range :
    ALIM088.Sup_val_set(v,1,100)
    ALIM088.Sup_ON()
    for i in Iout_range : 
        ALIM104.Load_val_set(0,i)
        ALIM104.Load_ON()
        OSCI015.Trigger_set (1, 20) # Chan1, 10V trig set to manual, Run mode
        time.sleep(0.2) # delay to wait the converter stabilization
        
        # Acquisition des valeurs continus  
        MULTI059.Mult_set('VOLT','DC')
        Vout_dcr.append(MULTI059.Mult_acq())
        if(Vout_dcr[-1]< 3) : # no regulation 
            Vin_r.append(0)
            Vout_acr.append(0)
            Vout_dcr[-1] = 0 
            Iin_r.append(0)
            Iout_r.append(0)
            Eff_r.append(0)
            Vaux_r.append(0)
            Vreg_r.append(0)
        else:
            MULTI059.Mult_set('VOLT','AC')
            Vout_acr.append(MULTI059.Mult_acq())
            Vin_r.append(ALIM088.Sup_mes()[0])
            Iin_r.append(MULTI062.Mult_acq())
            Iout_r.append(ALIM104.Load_mes()[1])
            time.sleep(0.2) # delay to wait the converter stabilization
            Eff_r.append((Vout_dcr[-1]*Iout_r[-1])/(Vin_r[-1]*Iin_r[-1]))
            Vaux_r.append(MULTI061.Mult_acq())
            Vreg_r.append(MULTI060.Mult_acq())
        #Acquisition Scope 
        data_r.append(OSCI015.Acquire_data())
        
    Vin.append(Vin_r)
    Iin.append(Iin_r)
    Vout_dc.append(Vout_dcr)
    Vout_ac.append(Vout_acr)
    Iout.append(Iout_r)
    Eff.append(Eff_r)
    Vaux.append(Vaux_r)
    Vreg.append(Vreg_r)
    Scope_data.append(data_r)
    Vin_r, Iin_r, Vout_dcr, Vout_acr, Iout_r, Eff_r, Vaux_r, Vreg_r, data_r = [],[],[],[],[],[],[],[],[]

#Extinction des appareils 
ALIM088.Sup_OFF()
ALIM104.Load_OFF()