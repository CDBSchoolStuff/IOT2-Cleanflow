from machine import ADC, Pin
from time import sleep

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



    ########################################
    # FUNCTIONS
    
    testvalue = 0
    
    def pump_test(self):
        self.testvalue = not self.testvalue
        self.pOut.value(not self.testvalue)
        print("Pump test:", self.testvalue)