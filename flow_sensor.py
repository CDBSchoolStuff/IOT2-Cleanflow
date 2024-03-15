from machine import Pin
import time


########################################
# OWN MODULES



########################################
# CONFIGURATION




########################################
# OBJECTS




########################################
# VARIABLES



########################################
# FUNCTIONS

class Flow:
    pulse = 0

def callback(p):
    # print('pin change', p)
    Flow.pulse = Flow.pulse + 1
    print('Pulse:', Flow.pulse)




# def flow_sensor(self):
#     #print(f"Pulses: {self.pulse}")
#     self.flow_pIn.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)
#     # if self.flow_pIn.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback):
#     #     self.pulse += 1
#     # else: 
#     #     return
