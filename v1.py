# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:39:26 2022

@author: ccolonna
"""
import os 
import numpy as np 
import pyvisa as pv
import pandas as pd


rm = pv.ResourceManager()
res= rm.list_resources()
list_instr = []

Instr_lab = pd.DataFrame({'ID' :['MY59201238','MY57252118',' 454132','MY59003642','1420497','MY59002198',' 454121','LCRY3702N14552',
                                 ' 428712','MY59003408','MY57227626','MY59243295','MY59002476','MY59002491',' J00428425',' 1733980001',
                                 ' 1880310002'],
                        'Label':['OSCI015', 'OSCI014','ALIM061','MULTI060','MULTI039','MULTI059','ALIM062','OSCI007','ALIM058',
                                 'MULTI058','MULTI057','OSCI014','MULTI061','MULTI062','ALIM053','ALIM075','ALIM088'],
                        'Brand':['Keysight', 'Keysight','TTi','Keysight','Keythley','Keysight','TTi','Lecroy',
                                 'TTi','Keysight','Keysight','Keysight','Keysight','Keysight','Sorensen','EA','EA'],
                        'Func' :['Scope','Scope','Supply','Multi','Multi','Multi','Supply','Scope','Supply','Multi',
                                 'Multi','Scope','Multi','Multi','Supply','Load','Supply']})

""" Fonctions à implémenter pour l'oscillo V1 : 
    - Trigger (Channel/ level) + Mode Auto/single  
    - Scale (Channel/ X / Y )
    - Mise en forme des datas de sortie 
    - Acquisition 
    
 Fonctions à implémenter pour l'alim V1 : 
    - Volt (Channel/level)
    - Amp (Channel/Level)
    - OVP/OCP/MaxPow trigger (Channel/Level) (signal lib)
    - ON/OFF 
    
 Fonctions à implémenter pour la charge V1 : 
    - Volt (Channel/level)
    - Amp (Channel/Level)
    - OVP/OCP/MaxPow trigger (Channel/Level) (signal lib)
    - ON/OFF 
    
 Fonctions à implémenter pour les multis : 
    - Type (AMPAC/AMPDC/VOLTAC/VOLTDC)
    - Calibre 
    - Set up mes (RMS/Eff, Average)
    - TRIG (signal lib)
"""

class Instruments:
    
    def __init__(self, ID, Adress):
        ind = np.where(Instr_lab.ID == ID)[0][0]
        self.ID    = Instr_lab.ID[ind]
        self.Label = Instr_lab.Label[ind]
        self.Brand = Instr_lab.Brand[ind]
        self.Func  = Instr_lab.Func[ind]
        self.Adress = Adress
        
####################### SCOPE ###########################################

    def Auto_scale (self):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write(':AUToscale')
            rm.close()
        else : 
            print('Bad call to function or function not implemented')
            
    def Display_chan (self, Channel, ON): # (0 = OFF, 1 = ON)
         if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
             rm.open_resource(self.Adress).write(':CHANnel'+str(Channel)+':DISPlay '+str(ON))
             rm.close()
         else : 
             print('Bad call to function or function not implemented')
    
    def Trigger_set (self, Channel, Level, Mode_set_trig = 0, Mode_acq = 0):   
         if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
             if (Mode_set_trig ==1):
                 rm.open_resource(self.Adress).write(':TRIGger:LEVel:ASETup')
             else: 
                 rm.open_resource(self.Adress).write(':TRIGger:MODE EDGE')
                 rm.open_resource(self.Adress).write(':TRIGger:SOURce CHANnel '+str(Channel))
                 rm.open_resource(self.Adress).write(':TRIGger:LEVel ' + str(Level))
            
             if (Mode_acq ==1):
                 rm.open_resource(self.Adress).write(':SINGle')
             else:
                 rm.open_resource(self.Adress).write(':RUN')     
             rm.close()
         else : 
             print('Bad call to function or function not implemented')   
             
    def Timebase_set (self, Scale, Position): 
        # time for 10 div in seconds in NR3 format ex 1e-6/ time in seconds from the trigger to the display reference
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write(':TIMebase:RANGe '+str(Scale))
            rm.open_resource(self.Adress).write(':TIMebase:POSition '+str(Position))
            rm.close()
        else : 
            print('Bad call to function or function not implemented')
            
    def Channel_set (self, Channel, Scale, Position='0', Mode='DC'): 
       if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
           rm.open_resource(self.Adress).write('CHANnel'+str(Channel)+':SCALe '+str(Scale)+'V')
           # V/div
           rm.open_resource(self.Adress).write('CHANnel'+str(Channel)+':OFFSet '+str(Position)+'V')
           # Value set in the center of the screen
           rm.open_resource(self.Adress).write('CHANnel'+str(Channel) +':COUPling '+ Mode)
           rm.close()
       else : 
           print('Bad call to function or function not implemented')   
           
           
    def Label_chan (self, Channel, Label):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write(':CHANnel'+str(Channel)+':LABel ' + '"'+Label+'"')
            rm.open_resource(self.Adress).write(':DISPlay:LABel 1')
            rm.close()
        else : 
            print('Bad call to function or function not implemented')
            
    def Acquire_data (self):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write('WAVeform:POINts:MODE NORMal')
            rm.open_resource(self.Adress).write('WAVeform:FORMat BYTE')
            rm.open_resource(self.Adress).write('WAVeform:POINts 1000')
            data = rm.open_resource(self.Adress).write('DIGitize')
            return data
        else : 
            print('Bad call to function or function not implemented')

####################### SUPPLY ###########################################  

    
# On scan tous les instruments disponibles pour déterminer ceux qui sont connectés 
# On les assigne en tant qu'objets instr. Chaque fonction sera ensuite définie dans la classe avec classe

for i in res :
    try : 
        list_instr.append((rm.open_resource(i)).query("*IDN?"))
        ind = np.where(Instr_lab.ID == list_instr[-1].split(',')[2])[0][0]
        locals()[Instr_lab.Label[ind]] = Instruments(Instr_lab.ID[ind], i) 
    except  pv.VisaIOError:
        if((i == res[-1]) and (list_instr == [])):
           print('No visa instruments connected')
        pass   
    except IndexError :
        print('No visa instruments reconized')
        pass
    
rm.close()





