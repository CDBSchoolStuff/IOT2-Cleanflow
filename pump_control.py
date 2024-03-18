from machine import ADC, Pin
from time import sleep
import flow_sensor

class Pump_Control:
    #########################################################################
    # INIT
    
    def __init__(self, pOut):
        self.pOut = pOut
    
    
    ########################################
    # CONFIGURATION



    ########################################
    # OBJECTS
    

    ########################################
    # VARIABLES

    prev_pulse = 0

    ########################################
    # FUNCTIONS
    
    testvalue = 0
    
    
    def on(self):
        print("Pump on")
        self.pOut.value(1)
        
    def off(self):
        print("Pump off")
        self.pOut.value(0)
    
    def pump_test(self):
        self.testvalue = not self.testvalue
        self.pOut.value(not self.testvalue)
        print("Pump test:", self.testvalue)
        
    def controller(self, pulse):
        if self.prev_pulse != pulse:
            self.on()
            self.prev_pulse = pulse
        else:
            self.off()