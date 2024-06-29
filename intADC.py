'''
Import needed librarys into python engine. 
'''
import time
import board
from analogio import AnalogIn
import microcontroller
import ulab.numpy as np

'''
Set processor core clock frequency
For Teensy 4.1 default is 600000000
'''
microcontroller.cpu.frequency = 600000000

'''
variable settings:
fullrange - the maximum raw value that can be returned buy the used ADCs
v/a_mult - multipyers to convert measured voltage at the ADC to mains voltage and current on the high voltage side of circut
'''
fulrange = 65536

v_one_mult = 216.9132341
a_one_mult = 10
v_two_mult = 216.9132341
a_two_mult = 10

'''
configure the ADC pins for the board
'''
in0 = AnalogIn(board.A0)
in1 = AnalogIn(board.A1)
in2 = AnalogIn(board.A2)
in3 = AnalogIn(board.A3)
inmid = AnalogIn(board.A4)

'''
Definitions for reading the ADCs for the two mains suppies
Returns 2 lists of values per supply
'''
def Read_one():
    timenow = time.monotonic_ns()
    print("start time", timenow)
    t_end = timenow + 50000000
    print("end time", t_end)
    volt = []
    amp = []
    
    while time.monotonic_ns() < t_end:
        v = in0.value
        a = in1.value
        volt.append(v)
        amp.append(a)
        
    return (volt, amp)

def Read_two():
    timenow = time.monotonic_ns()
    print("start time", timenow)
    t_end = timenow + 50000000
    print("end time", t_end)
    volt = []
    amp = []

    while time.monotonic_ns() < t_end:
        v = in2.value
        a = in3.value
        volt.append(v)
        amp.append(a)
    
    return (volt, amp)

'''
main analysis of each channels returned values returns:
S - apparent power
P - active power
Q - reactive power
PF - power Factor
Vrms - RMS voltage value
Arms - RMS current value
'''
def Analyse(volt, amp, v_mult, a_mult):
    '''convert raw values to volts and amps, apply multipyer to find mains values.'''
    volt = [(((x - ADCmid)*3.3)/fulrange)*v_mult for x in volt]
    amp = [(((x - ADCmid)*3.3)/fulrange)*a_mult for x in amp]
    
    '''find the min and max voltage values, also the total number of sample points'''
    max_v = max(volt)
    min_v = min(volt)
    count_v = len(volt)
    
    '''calculate the RMS voltage using the traditional method and the aporximate using the peak value'''
    vsqsum = 0
    for v in volt:
        vsq = v*v
        vsqsum += vsq
    vrms = np.sqrt(vsqsum/count_v)
    vrms_aprox = max_v * (1/ np.sqrt(2))
    
    '''find the min and max current values, also the total number of sample points'''
    max_a = max(amp)
    min_a = min(amp)
    count_a = len(amp)
    
    '''calculate the RMS currnent using the traditional method and the aporximate using the peak value'''
    asqsum = 0
    for a in amp:
        asq = a*a
        asqsum += asq
    arms = np.sqrt(asqsum/count_a)
    
    '''calculate the apparent power: product of rms voltage and rms currnent'''
    apparent_p = vrms * arms
    
    '''
    calculate instantainious power for each sample point,
    join the two list, then calcultate the product of each set of values
    record output into new list
    '''
    joint = [volt,amp]
    inst_p = []
    for x in zip(*joint) :
        power = x[0] * x[1]
        inst_p.append(power)
    
    '''find max instantainious power value'''
    inst_pmax = max(inst_p)
    
    '''calculate power factor'''
    power_f = (inst_pmax/apparent_p)-1
    
    '''calculate active power'''
    active_p = inst_pmax - apparent_p
    
    '''calculate reactive power'''
    reactive_p = np.sqrt(inst_pmax*((2*apparent_p)-inst_pmax))
    
    '''return calculated values'''
    return(apparent_p,active_p,reactive_p,power_f,vrms,arms)
    
ADCmid = inmid.value
print(ADCmid)
volt_one,amp_one = Read_one()
print(volt_one)
print(amp_one)
volt_two,amp_two = Read_two()
S_one,P_one,RP_one,PF_one,Vrms_one,Arms_one = Analyse(volt_one,amp_one,v_one_mult,a_one_mult)
print(S_one,P_one,RP_one,PF_one,Vrms_one)
S_two,P_two,RP_two,PF_two,vrms_two,Arms_two = Analyse(volt_two,amp_two,v_two_mult,a_two_mult)
print(S_two,P_two,RP_two,PF_two)
