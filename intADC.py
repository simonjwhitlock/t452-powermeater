import time
import board
from analogio import AnalogIn
import microcontroller
import ulab.numpy as np

microcontroller.cpu.frequency = 600000000

midval = 32768
fulrange = 65536

v1_mult = 220
a1_mult = 10
v2_mult = 220
a2_mult = 10

in0 = AnalogIn(board.A0)
in1 = AnalogIn(board.A1)
in2 = AnalogIn(board.A2)
in3 = AnalogIn(board.A3)
inmid = AnalogIn(board.A4)


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


def Analyse(volt, amp, v_mult, a_mult):

    max_v = ((max(volt)-ADCmid)*3.3)/fulrange
    min_v = ((min(volt)-ADCmid)*3.3)/fulrange
    count_v = len(volt)
    vsqsum = 0
    for v in volt:
        v = ((v-ADCmid)*3.3)/fulrange
        vsq = v*v
        vsqsum += vsq
    vrms = (np.sqrt(vsqsum/count_v))#*v_mult
    print("v rms :", vrms)
    print("v max :", max_v)
    print("v min :", min_v)
    
    max_a = ((max(amp)-ADCmid)*3.3)/fulrange
    min_a = ((min(amp)-ADCmid)*3.3)/fulrange
    count_a = len(amp)
    asqsum = 0
    for a in amp:
        a = ((a-ADCmid)*3.3)/fulrange
        asq = a*a
        asqsum += asq
    arms = (np.sqrt(asqsum/count_a))*a_mult
    print("a rms :", arms)
    print("a max :", max_a)
    print("a min :", min_a)
    
    true_p = vrms * arms
    print("true power:", true_p)

    
ADCmid = inmid.value
print(ADCmid)
print(midval)
volt_one,amp_one = Read_one()
Analyse(volt_one,amp_one,v1_mult,a1_mult)
