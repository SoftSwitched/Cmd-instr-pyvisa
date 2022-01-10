# Cmd-instr-pyvisa
/////////////////////////PURPOSE OF THIS PROGRAM V1.0 /////////////////////////

The purpose of this program is to simplify and homogenize the communication between the computer and the
instruments of the lab. A database containing most of the controllable instruments has been created. 
The devices are added as objects under the name written on their label : 
ex : OSCI015 

The functions can then be called by invoking the following form: 
OSCI015.My_function()

The following functions have been implemented in version v1.0 of the program. 

/////////////////////////GENERAL PURPOSE_FUNCTIONS////////////////////// 

*scan_device()
Function that allows to scan all the devices connected to the computer and to create the objects associated with the known names.
This function must be started before the objects can be called. 

/////////////////////////SCOPE_FUNCTIONS///////////////////////////////

*Auto_scale (self)
Autoscale function that allows to automatically adjust the different channels of the oscillator. No arguments. 
ex : OSCI015.Auto_scale() 
   
*Display_chan (self, Channel, ON)   
Display_chan(self, Channel, ON) displays the channels of the scope. Only the displayed channels can be registered! 
Channel is between int[1..4]
ON = 1 allows the channel to be displayed whereas ON = 0 allows it not to be displayed 
ex : OSCI015.Display_chan(3,1) chan3 display ON 
     
*Trigger_set(self, Channel, Level, Mode_set_trig = 0, Mode_acq = 0)
Trigger_set allows to set the trigger parameters. 
Channel takes the value int[1..4] defines the channel on which you want to trigger. 
Level, the level in volts from which you want to trigger. 
Mode_set_trig, defines whether we want to set this level to auto (=1) or manual (=0). 
Mode_acq defines if a trigger event stops the acquisition (single = 1) or if we want to run in auto trig (run = 0)
ex : OSCI015.Trigger_set(1,2,0,0) trigger set on chan1, 2V, manual mode and RUN (auto trig) 

*Timebase_set(self, Scale, Position) 
Timebase_set is used to define the time base (x axis of the scope). 
Scale gives the duration of a time period. The input must be in the form 2e-6. 
Position gives the position of the trigger (time origin). In the form 2e-6. 
ex : OSCI015.Timebase_set(1e-6,0) set the timebase at 1e-6s/div and the origin a 0s 

*Channel_set (self, Channel, Scale, Position='0', Mode='DC')
Channel_set allows to set a channel of the scope. 
Channel takes the int[1..4] value corresponding to the channel you want to set
Scale the scale in V/div that we want to give to channel x
Position gives the offset (by default 0) 
Mode gives the acquisition mode AC or DC. It must be given in str. By default, this parameter is set to DC. 
ex : OSCI015.Channel_set(1,1) Channel 1, 1V/div, Origin Pos 0V, DC mode 

*Label_chan (self, Channel, Label)    
Label_chan allows to give a name to a channel. 
Channel gives the channel whose name you want to change int(1..4) 
Label the name str(<10 char)
ex : OSCI015.Label_chan(1, 'Jeanpipi') Set Jeanpipi for the label of the first channel (Not recommended)

*Acquire_data (self)
Acquire_data is used to launch an acquisition of the scope window. Only the displayed channels are digitized. 
The function returns vectors. The first vector gives the time base, the others are sorted in ascending order of acquisition. 
ex : data = OSCI015.Acquire_data(), with data[0] = t, data[1] = chan1. 

/////////////////////////SUPPLY FUNCTIONS////////////////////////////// 
    
*Sup_val_set(self, Volt, Amp, Channel=1, Power =10)
Sup_val_set allows you to set the parameters of the power supply. 
Volt the value of the voltage in volts that you wish to set 
Amp the value of the current limit 
Channel the number of the channel. The function must be invoked several times if you wish to set several channels. by default channel = 1 
Power the power limit to be set (default Power = 10W).  
ex : ALIM001.Sup_val_set( 5, 1, 1, 7) Output 1 set to 5V, 1A and 5W 
    
*Sup_prot_set(self, OVP, OCP, Channel=1, OPP =10)
Sup_prot_set is used to define the protections to be set up on the power supply. 
OVP sets the voltage limit in Volt 
OCP sets the current consumption in Amp 
Channel the channel you want to protect. 
OPP sets the max power limit (default OPP =10W)
ex : ALIM001.Sup_prot_set(6,0.8,1,5) Channel 1 protections set to OVP =6V, OCP = 0.8A and OPP = 5W 

*Sup_mes(self, Channel = 1)
Sup_mes returns the values of the various current parameters of the power supply in the form of voltage, current, power, OVP, OCP, OPP
Channel, default argument equal to 1. 
ex : ALIM001.Sup_mes()

*Sup_ON(self, Channel = 1)
The output 1 of the supply is set ON 
ex : ALIM001.Sup_ON(1) 

*Sup_OFF(self, Channel = 1)
The output 1 of the supply is set OFF 
ex : ALIM001.Sup_OFF(1)

          
/////////////////////////LOAD FUNCTIONS///////////////////////////////             

*Load_val_set(self, Volt, Amp, Channel=1, Power =10)
Set parameters of the load. 
Volt give the value of the maximum voltage allowed in V 
Amp set the value of the load in A 
Channel the input channel value (default = 1)
Power the power limit in W (default = 10W). 
ex : LOAD001.Load_val_set(5,3,1,10) Max voltage 5V, max Amp 3A, Max power 10W

*Load_prot_set(self, OVP, OCP, Channel=1, OPP =10)
Load_prot_set is used to define the protections to be set up on the load. 
OVP sets the voltage limit in Volt 
OCP sets the current consumption in Amp 
Channel the channel you want to protect. 
OPP sets the max power limit (default OPP =10W)
ex : LOAD001.Load_prot_set(6,0.8,1,5) Channel 1 protections set to OVP =6V, OCP = 0.8A and OPP = 5W 

*Load_mes(self, Channel=1)    
Load_mes returns the values of the various current parameters of the load in the form of voltage, current, power, OVP, OCP, OPP
Channel, default argument equal to 1. 
ex : LOAD001.Load_mes()

*Load_ON(self, Channel = 1)
The input 1 of the load is set ON 
ex : LOAD001.Load_ON(1) 

*Load_OFF(self, Channel = 1)
The input 1 of the load is set OFF 
ex : LOAD001.Load_OFF(1)     
      
/////////////////////////MULTI FUNCTIONS////////////////////////////             

*Mult_set(self, mode_VA, mode_ACDC)
Mult_set allows you to set the input of the multimeter. 
mode_VA defines the acquisition quantity 'VOLT' or 'CURR
mode_ACDC defines the acquisition mode 'AC' or 'DC'
ex : MULTI001.Mult_set('VOLT','DC') 

*Mult_acq(self) 
Acquisition on the multimeter input 
ex : data = MULTI001.Mult_acq() 




