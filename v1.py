"""
Created on Wed Jan  5 15:39:26 2022
@author: ccolonna

"""
import numpy as np 
import pyvisa as pv
import pandas as pd

rm = pv.ResourceManager()
res= rm.list_resources()
list_instr = []

Instr_lab = pd.DataFrame({'ID' :['MY59201238','MY57252118',' 454132','MY59003642','1420497','MY59002198',' 454121','LCRY3702N14552',
                                 ' 428712','MY59003408','MY57227626','MY59243295','MY59002476','MY59002491',' J00428425',' 1733980001',
                                 ' 1880310002'],
                        'Label':['OSCI015', 'OSCI009','ALIM061','MULTI060','MULTI039','MULTI059','ALIM062','OSCI007','ALIM058',
                                 'MULTI058','MULTI057','OSCI014','MULTI061','MULTI062','ALIM053','ALIM075','ALIM088'],
                        'Brand':['Keysight', 'Keysight','TTi','Keysight','Keythley','Keysight','TTi','Lecroy',
                                 'TTi','Keysight','Keysight','Keysight','Keysight','Keysight','Sorensen','EA','EA'],
                        'Func' :['Scope','Scope','Supply','Multi','Multi','Multi','Supply','Scope','Supply','Multi',
                                 'Multi','Scope','Multi','Multi','Supply','Load','Supply']})


class Instruments:
    
    def __init__(self, ID, Adress):
        ind = np.where(Instr_lab.ID == ID)[0][0]
        self.ID    = Instr_lab.ID[ind]
        self.Label = Instr_lab.Label[ind]
        self.Brand = Instr_lab.Brand[ind]
        self.Func  = Instr_lab.Func[ind]
        self.Adress = Adress
        
####################### SCOPE ###########################################wv 

    def Auto_scale (self):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write(':AUToscale')
 
        else : 
            print('Bad call to function or function not implemented')
            
    def Display_chan (self, Channel, ON): # (0 = OFF, 1 = ON)
         if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
             rm.open_resource(self.Adress).write(':CHANnel'+str(Channel)+':DISPlay '+str(ON))
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
 
         else : 
             print('Bad call to function or function not implemented')   
             
    def Timebase_set (self, Scale, Position): 
        # time for 10 div in seconds in NR3 format ex 1e-6/ time in seconds from the trigger to the display reference
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write(':TIMebase:RANGe '+str(Scale))
            rm.open_resource(self.Adress).write(':TIMebase:POSition '+str(Position))
   
        else : 
            print('Bad call to function or function not implemented')
            
    def Channel_set (self, Channel, Scale, Position='0', Mode='DC'): 
       if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
           rm.open_resource(self.Adress).write('CHANnel'+str(Channel)+':SCALe '+str(Scale)+'V')
           # V/div
           rm.open_resource(self.Adress).write('CHANnel'+str(Channel)+':OFFSet '+str(Position)+'V')
           # Value set in the center of the screen
           rm.open_resource(self.Adress).write('CHANnel'+str(Channel) +':COUPling '+ Mode)
 
       else : 
           print('Bad call to function or function not implemented')   
           
           
    def Label_chan (self, Channel, Label):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write(':CHANnel'+str(Channel)+':LABel ' + '"'+Label+'"')
            rm.open_resource(self.Adress).write(':DISPlay:LABel 1')
    
        else : 
            print('Bad call to function or function not implemented')
            
    def Acquire_data (self):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            rm.open_resource(self.Adress).write(':DIGitize')
            rm.open_resource(self.Adress).write('WAVeform:POINts:MODE NORMal')
            rm.open_resource(self.Adress).write('WAVeform:FORMat ASCii')
            rm.open_resource(self.Adress).write('WAVeform:POINts 1000')
            data = []
            Range = float(rm.open_resource(self.Adress).query('TIMebase:WINDow:RANGe?'))
            Pos = float(rm.open_resource(self.Adress).query('TIMebase:POSition?'))
            data.append(np.linspace(-5*Range+Pos,5*Range+Pos,992)) #Timebase
            for i in [1,2,3,4]:
                if(int(rm.open_resource(self.Adress).query('CHANnel'+str(i)+':DISPlay?')[0])== 1):
                    rm.open_resource(self.Adress).write(':WAVeform:SOURce CHAN'+str(i))
                    data.append(np.asarray(rm.open_resource(self.Adress).query('WAVeform:DATA?')[10:].split(",")).astype(float))
            return data
        else : 
            print('Bad call to function or function not implemented')

####################### SUPPLY ###########################################  
    
    def Sup_val_set(self, Volt, Amp, Channel=1, Power =10):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            rm.open_resource(self.Adress).write('VOLT '+str(Volt))
            rm.open_resource(self.Adress).write('CURR '+str(Amp))
            rm.open_resource(self.Adress).write('POW '+str(Power))
 
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')
             
        else : 
            print('Bad call to function or function not implemented')
      
    def Sup_prot_set(self, OVP, OCP, Channel=1, OPP =10):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            rm.open_resource(self.Adress).write('VOLT:PROT '+str(OVP))
            rm.open_resource(self.Adress).write('CURR:PROT '+str(OCP))
            rm.open_resource(self.Adress).write('POW:PROT '+str(OPP))
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')
        else : 
            print('Bad call to function or function not implemented')
                       
    def Sup_mes(self, Channel = 1):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            volt = rm.open_resource(self.Adress).query('MEAS:VOLT?')
            amp  = rm.open_resource(self.Adress).query('MEAS:CURR?')
            power= rm.open_resource(self.Adress).query('MEAS:POW?')
            volt_prot = rm.open_resource(self.Adress).query('VOLT:PROT?')
            amp_prot  = rm.open_resource(self.Adress).query('CURR:PROT?')
            power_prot= rm.open_resource(self.Adress).query('POW:PROT?')
            return volt, amp, power, volt_prot, amp_prot, power_prot
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')
             
        else : 
            print('Bad call to function or function not implemented')

    def Sup_ON(self, Channel = 1):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            rm.open_resource(self.Adress).write('OUTP ON')
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')          
        else : 
            print('Bad call to function or function not implemented')
            
    def Sup_OFF(self, Channel = 1):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            rm.open_resource(self.Adress).write('OUTP OFF')
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')          
        else : 
            print('Bad call to function or function not implemented')
            
            
####################### LOAD ###########################################  
    
    def Load_val_set(self, Volt, Amp, Channel=1, Power =10):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            rm.open_resource(self.Adress).write('VOLT '+str(Volt))
            rm.open_resource(self.Adress).write('CURR '+str(Amp))
            rm.open_resource(self.Adress).write('POW '+str(Power))             
        else : 
            print('Bad call to function or function not implemented')
      
    def Load_prot_set(self, OVP, OCP, Channel=1, OPP =10):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            rm.open_resource(self.Adress).write('VOLT:PROT '+str(OVP))
            rm.open_resource(self.Adress).write('CURR:PROT '+str(OCP))
            rm.open_resource(self.Adress).write('POW:PROT '+str(OPP))
        else : 
            print('Bad call to function or function not implemented')
             
            
    def Load_mes(self, Channel=1):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            volt = rm.open_resource(self.Adress).query('MEAS:VOLT?')
            amp  = rm.open_resource(self.Adress).query('MEAS:CURR?')
            power= rm.open_resource(self.Adress).query('MEAS:POW?')
            volt_prot = rm.open_resource(self.Adress).query('VOLT:PROT?')
            amp_prot  = rm.open_resource(self.Adress).query('CURR:PROT?')
            power_prot= rm.open_resource(self.Adress).query('POW:PROT?')
            return volt, amp, power, volt_prot, amp_prot, power_prot             
        else : 
            print('Bad call to function or function not implemented')

    def Load_ON(self, Channel = 1):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            rm.open_resource(self.Adress).write('INP ON')      
        else : 
            print('Bad call to function or function not implemented')
            
    def Load_OFF(self, Channel = 1):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            rm.open_resource(self.Adress).write('INP OFF')         
        else : 
            print('Bad call to function or function not implemented')
            
####################### MULTI ########################################### 

    def Mult_set(self, mode_VA, mode_ACDC):
        if (self.Brand == 'Keysight') and (self.Func == 'Multi'): # Driver  Keysight Multi
            rm.open_resource(self.Adress).write('MEASure:'+ mode_VA +':'+ mode_ACDC)          
        else : 
            print('Bad call to function or function not implemented')
           
    def Mult_acq(self):
        if (self.Brand == 'Keysight') and (self.Func == 'Multi'): # Driver  Keysight Multi
            data = rm.open_resource(self.Adress).query('READ?')  
            return data
        else : 
            print('Bad call to function or function not implemented')
            
            
####################### GBF ########################################### 

# Sera créé plus tard ! 


def scan_device():
    # On scan tous les instruments disponibles pour déterminer ceux qui sont connectés 
    # On les assigne en tant qu'objets instr. Chaque fonction sera ensuite définie dans la classe avec classe
    
    for i in res :
        try : 
            list_instr.append((rm.open_resource(i)).query("*IDN?"))
            ind = np.where(Instr_lab.ID == list_instr[-1].split(',')[2])[0][0]
            locals()[Instr_lab.Label[ind]] = Instruments(Instr_lab.ID[ind], i) 
            print('Instrument reconized and added to objects: ' + str(Instr_lab.Label[ind]))
        except  pv.VisaIOError:
            if((i == res[-1]) and (list_instr == [])):
               print('No visa instruments connected')
            pass   
        except IndexError :
            print('No visa instruments reconized')
            pass
    