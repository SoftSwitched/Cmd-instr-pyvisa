"""
Created on Wed Jan  5 15:39:26 2022
@author: ccolonna

"""
import numpy as np 
import pyvisa as pv
import pandas as pd
import time 


Instr_lab = pd.DataFrame({'ID' :['MY59201238','MY57252118',' 454132','MY59003642','1420497','MY59002198',' 454121','LCRY3702N14552',
                                 ' 428712','MY59003408','MY57227626','MY59243295','MY59002476','MY59002491',' J00428425',' 1733980001',
                                 ' 1880310002', ' 2238200001','CU200081'],
                        'Label':['OSCI015', 'OSCI009','ALIM061','MULTI060','MULTI039','MULTI059','ALIM062','OSCI007','ALIM058',
                                 'MULTI058','MULTI057','OSCI014','MULTI061','MULTI062','ALIM053','ALIM075','ALIM088', 'ALIM104','GEBF3'],
                        'Brand':['Keysight', 'Keysight','TTi','Keysight','Keythley','Keysight','TTi','Lecroy',
                                 'TTi','Keysight','Keysight','Keysight','Keysight','Keysight','Sorensen','EA','EA','EA','Tektronix'],
                        'Func' :['Scope','Scope','Supply','Multi','Multi','Multi','Supply','Scope','Supply','Multi',
                                 'Multi','Scope','Multi','Multi','Supply','Load','Supply', 'Load','GBF']})


class Instruments:
    
    def __init__(self, ID, Adress):
        ind = np.where(Instr_lab.ID == ID)[0][0]
        self.ID    = Instr_lab.ID[ind]
        self.Label = Instr_lab.Label[ind]
        self.Brand = Instr_lab.Brand[ind]
        self.Func  = Instr_lab.Func[ind]
        self.Adress = Adress
        self.rm = pv.ResourceManager()
        
        if(self.Func == 'Scope'): # If scope, bigger buffer
            self.rm.open_resource(self.Adress).chunk_size = 102400


        
####################### SCOPE ###########################################wv 

    def Auto_scale (self):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            self.rm.open_resource(self.Adress).write(':AUToscale')

        else : 
            print('Bad call to function or function not implemented')
            
    def Display_chan (self, Channel, ON): # (0 = OFF, 1 = ON)
         if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
             self.rm.open_resource(self.Adress).write(':CHANnel'+str(Channel)+':DISPlay '+str(ON))

         else : 
             print('Bad call to function or function not implemented')
    
    def Trigger_set (self, Channel, Level, Mode_set_trig = 0, Mode_acq = 0):   
         if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
             if (Mode_set_trig ==1):
                 self.rm.open_resource(self.Adress).write(':TRIGger:LEVel:ASETup')
             else: 
                 self.rm.open_resource(self.Adress).write(':TRIGger:MODE EDGE')
                 self.rm.open_resource(self.Adress).write(':TRIGger:SOURce CHANnel '+str(Channel))
                 self.rm.open_resource(self.Adress).write(':TRIGger:LEVel ' + str(Level))
            
             if (Mode_acq ==1):
                 self.rm.open_resource(self.Adress).write(':SINGle')
             else:
                 self.rm.open_resource(self.Adress).write(':RUN')   
             

 
         else : 
             print('Bad call to function or function not implemented')   
             
    def Timebase_set (self, Scale, Position=0): 
        # time for 10 div in seconds in NR3 format ex 1e-6/ time in seconds from the trigger to the display reference
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            self.rm.open_resource(self.Adress).write(':TIMebase:RANGe '+str(Scale))
            self.rm.open_resource(self.Adress).write(':TIMebase:POSition '+str(Position))

   
        else : 
            print('Bad call to function or function not implemented')
            
    def Channel_set (self, Channel, Scale, Position='0', Mode='DC'): 
       if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
           self.rm.open_resource(self.Adress).write('CHANnel'+str(Channel)+':SCALe '+str(Scale)+'V')
           # V/div
           self.rm.open_resource(self.Adress).write('CHANnel'+str(Channel)+':OFFSet '+str(Position)+'V')
           # Value set in the center of the screen
           self.rm.open_resource(self.Adress).write('CHANnel'+str(Channel) +':COUPling '+ Mode)

 
       else : 
           print('Bad call to function or function not implemented')   
           
           
    def Label_chan (self, Channel, Label):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            self.rm.open_resource(self.Adress).write(':CHANnel'+str(Channel)+':LABel ' + '"'+Label+'"')
            self.rm.open_resource(self.Adress).write(':DISPlay:LABel 1')

    
        else : 
            print('Bad call to function or function not implemented')
            
    def Acquire_data (self):
        if (self.Brand == 'Keysight') and (self.Func == 'Scope'): # Driver Scope Keysight
            self.rm.open_resource(self.Adress).write(':DIGitize')
            self.rm.open_resource(self.Adress).write('WAVeform:POINts:MODE NORMal')
            self.rm.open_resource(self.Adress).write('WAVeform:FORMat ASCii')
            self.rm.open_resource(self.Adress).write('WAVeform:POINts 1000')
            data = []
            Range = float(self.rm.open_resource(self.Adress).query('TIMebase:WINDow:RANGe?'))
            Pos = float(self.rm.open_resource(self.Adress).query('TIMebase:POSition?'))
            data.append(np.linspace(-5*Range+Pos,5*Range+Pos,992)) #Timebase
            for i in [1,2,3,4]:
                if(int(self.rm.open_resource(self.Adress).query('CHANnel'+str(i)+':DISPlay?')[0])== 1):
                    self.rm.open_resource(self.Adress).write(':WAVeform:SOURce CHAN'+str(i))
                    data.append(np.asarray(self.rm.open_resource(self.Adress).query('WAVeform:DATA?')[10:].split(",")).astype(float))

            return data
        else : 
            print('Bad call to function or function not implemented')

####################### SUPPLY ###########################################  
    
    def Sup_val_set(self, Volt, Amp, Channel=1, Power =10):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('VOLT '+str(Volt)+'V')
            self.rm.open_resource(self.Adress).write('CURR '+str(Amp)+'A')
            self.rm.open_resource(self.Adress).write('POW '+str(Power)+'W')

            
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')
             
        else : 
            print('Bad call to function or function not implemented')
      
    def Sup_prot_set(self, OVP, OCP, Channel=1, OPP =100):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('VOLT:PROT '+str(OVP)+'V')
            self.rm.open_resource(self.Adress).write('CURR:PROT '+str(OCP)+'A')
            self.rm.open_resource(self.Adress).write('POW:PROT '+str(OPP)+'W')
 
            
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')
        else : 
            print('Bad call to function or function not implemented')
                       
    def Sup_mes(self, Channel = 1):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            volt = float(self.rm.open_resource(self.Adress).query('MEAS:VOLT?')[0:-3])
            amp  = float(self.rm.open_resource(self.Adress).query('MEAS:CURR?')[0:-3])
            power= float(self.rm.open_resource(self.Adress).query('MEAS:POW?')[0:-3])
            volt_prot = float(self.rm.open_resource(self.Adress).query('VOLT:PROT?')[0:-3])
            amp_prot  = float(self.rm.open_resource(self.Adress).query('CURR:PROT?')[0:-3])
            power_prot= float(self.rm.open_resource(self.Adress).query('POW:PROT?')[0:-3])

            return volt, amp, power, volt_prot, amp_prot, power_prot
        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')
             
        else : 
            print('Bad call to function or function not implemented')

    def Sup_ON(self, Channel = 1):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('OUTP ON')

        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')          
        else : 
            print('Bad call to function or function not implemented')
            
    def Sup_OFF(self, Channel = 1):
        if (self.Brand == 'TTi') and (self.Func == 'Supply'): # Driver TTi supply
            print('Not YET implemented')
        elif (self.Brand == 'EA') and (self.Func == 'Supply'): # Driver  EA supply
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('OUTP OFF')

        elif (self.Brand == 'Sorensen') and (self.Func == 'Supply'): #Driver Sorensen supply
            print('Not YET implemented')          
        else : 
            print('Bad call to function or function not implemented')
            
            
####################### LOAD ###########################################  
    
    def Load_val_set(self, Volt, Amp, Channel=1, Power =10):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('VOLT '+str(Volt) +'V')
            self.rm.open_resource(self.Adress).write('CURR '+str(Amp)+'A')
            self.rm.open_resource(self.Adress).write('POW '+str(Power)+'W')    

        else : 
            print('Bad call to function or function not implemented')
      
    def Load_prot_set(self, OVP, OCP, Channel=1, OPP =10):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('VOLT:PROT '+str(OVP)+'V')
            self.rm.open_resource(self.Adress).write('CURR:PROT '+str(OCP)+'A')
            self.rm.open_resource(self.Adress).write('POW:PROT '+str(OPP)+'W')
   
        else : 
            print('Bad call to function or function not implemented')
             
            
    def Load_mes(self, Channel=1):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            volt = float(self.rm.open_resource(self.Adress).query('MEAS:VOLT?')[0:-3])
            amp  = float(self.rm.open_resource(self.Adress).query('MEAS:CURR?')[0:-3])
            power= float(self.rm.open_resource(self.Adress).query('MEAS:POW?')[0:-3])
            volt_prot = float(self.rm.open_resource(self.Adress).query('VOLT:PROT?')[0:-3])
            amp_prot  = float(self.rm.open_resource(self.Adress).query('CURR:PROT?')[0:-3])
            power_prot= float(self.rm.open_resource(self.Adress).query('POW:PROT?')[0:-3])

            return volt, amp, power, volt_prot, amp_prot, power_prot             
        else : 
            print('Bad call to function or function not implemented')

    def Load_ON(self, Channel = 1):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('INP ON')      

        else : 
            print('Bad call to function or function not implemented')
            
    def Load_OFF(self, Channel = 1):
        if (self.Brand == 'EA') and (self.Func == 'Load'): # Driver  EA load
            self.rm.open_resource(self.Adress).write("*CLS") # Reset config 
            self.rm.open_resource(self.Adress).write("*RST") # Reset config
            self.rm.open_resource(self.Adress).write('INP OFF')  
 
        else : 
            print('Bad call to function or function not implemented')
            
####################### MULTI ########################################### 

    def Mult_set(self, mode_VA, mode_ACDC):
        if (self.Brand == 'Keysight') and (self.Func == 'Multi'): # Driver  Keysight Multi
            self.rm.open_resource(self.Adress).write('CONF:'+ mode_VA +':'+ mode_ACDC)

        else : 
            print('Bad call to function or function not implemented')
           
    def Mult_acq(self):
        if (self.Brand == 'Keysight') and (self.Func == 'Multi'): # Driver  Keysight Multi
            data = float(self.rm.open_resource(self.Adress).query('READ?') ) 

            return data
        else : 
            print('Bad call to function or function not implemented')
            
            
####################### GBF ########################################### 

    def GBF_PWM_set(self, Ton, Period, Amp, dt1 = 100, dt2 = 100): # Duty %, Period us, Amp V, dt1 ns, dt2 ns 
        if (self.Brand == 'Tektronix') and (self.Func == 'GBF'): # Driver  GBF tektro
            self.rm.open_resource(self.Adress).write('*CLS')
            self.rm.open_resource(self.Adress).write('*RST')
            time.sleep(0.2)
            # Réglage de la voie 1 
            self.rm.open_resource(self.Adress).write('SOURce1:FUNCtion PULSe')
            D1 = ((Ton-(dt2+dt1)/2000)/Period)*100 
            self.rm.open_resource(self.Adress).write('SOURce1:PULSe:DCYCle '+str(np.floor(D1)))
            self.rm.open_resource(self.Adress).write('SOURce1:PULSe:PERiod '+str(Period)+'us')
            self.rm.open_resource(self.Adress).write('SOURce1:PULSe:TRANsition:LEADing MIN')
            self.rm.open_resource(self.Adress).write('SOURce1:PULSe:TRANsition:TRAiling MIN')
            self.rm.open_resource(self.Adress).write('SOURce1:PULSe:DELay '+str(dt2)+'ns')
            self.rm.open_resource(self.Adress).write('SOURce1:VOLTage:LEVel:IMMediate:HIGH ' +str(Amp)+'V')
            self.rm.open_resource(self.Adress).write('SOURce1:VOLTage:LEVel:IMMediate:LOW 0V') 
            self.rm.open_resource(self.Adress).write('*SAV 1') 
            #♦Réglage de la voie 2 
            D2 = ((Ton+(dt2+dt1)/2000)/Period)*100 
            self.rm.open_resource(self.Adress).write('SOURce2:FUNCtion PULSe') 
            self.rm.open_resource(self.Adress).write('SOURce2:PULSe:DCYCle '+str(np.floor(D2)))
            self.rm.open_resource(self.Adress).write('SOURce2:PULSe:PERiod '+str(Period)+'us')  
            self.rm.open_resource(self.Adress).write('SOURce2:PULSe:TRANsition:LEADing MIN')
            self.rm.open_resource(self.Adress).write('SOURce2:PULSe:TRANsition:TRAiling MIN')
            self.rm.open_resource(self.Adress).write('SOURce2:VOLTage:LEVel:IMMediate:HIGH ' +str(Amp)+'V')
            self.rm.open_resource(self.Adress).write('SOURce2:VOLTage:LEVel:IMMediate:LOW 0V')
            self.rm.open_resource(self.Adress).write('OUTPut2:POLarity INV')
            time.sleep(0.3)
            self.rm.open_resource(self.Adress).write('*SAV 1') 
            self.rm.open_resource(self.Adress).write('*RCL 1') 
   
        else : 
            print('Bad call to function or function not implemented')


# On scan tous les instruments disponibles pour déterminer ceux qui sont connectés 
# On les assigne en tant qu'objets instr. Chaque fonction sera ensuite définie dans la classe avec classe

rm = pv.ResourceManager()
res= rm.list_resources()
list_instr = []
for i in res :
    try : 
        list_instr.append((rm.open_resource(i)).query("*IDN?"))
        ind = np.where(Instr_lab.ID == list_instr[-1].split(',')[2])[0][0]
        globals()[Instr_lab.Label[ind]] = Instruments(Instr_lab.ID[ind], i) 
        print('Instrument reconized and added to objects: ' + str(Instr_lab.Label[ind]))
    except  pv.VisaIOError:
        if((i == res[-1]) and (list_instr == [])):
           print('No visa instruments connected')
        pass   
    except IndexError :
        print('No visa instruments reconized : ' + list_instr[-1])
        pass

