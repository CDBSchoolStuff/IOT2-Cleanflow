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

class Flow_Sensor:
    #########################################################################
    # INIT
    
    def __init__(self, Pump):
        self.Pump = Pump
    
    
    ########################################
    # VARIABLES

    pulse = 0
    current_pulse = 0

    ########################################
    # FUNCTIONS

    # Denne callback funktion kaldes hver gang der detecteres en "rising edge" på indgangsbenet til flow sensoren.
    def callback(self, p):
        self.pulse = self.pulse + 1
        self.current_pulse = self.current_pulse + 1
        print('Pulse:', self.pulse)
        print('Current Pulse:', self.current_pulse)
        self.Pump.controller(self.pulse)
    
    
    # Beregner den totale mængde tappet vand baseret på pulser fra flowsensoren.
    def get_total_liter(self):
        pulse = self.current_pulse

        file = open("total_pulse.txt", "r")
        try:
            saved_pulse = int(file.read())
        except:
            print("Couldn't update prev_pulse")
            saved_pulse = 0
        print("saved_pulse:", saved_pulse)
        file.close()
        
        file = open("total_pulse.txt", "w")
        total_pulse = int(saved_pulse) + pulse
        file.write(f'{total_pulse}')
        file.close()
        print("Total Pulse:", total_pulse)
        self.current_pulse = 0

        liter = float(total_pulse / 450)
        return round(liter, 2)
    
    def get_liter(self, pulse_arg):
        liter = float(pulse_arg / 450)
        return round(liter, 2)
    
    # Nulstiller den gemte puls værdi. Bruges så tælling kan starte forfra efter at data er blevet sendt.
    def reset_saved_liter(self):
        file = open("total_pulse.txt", "w")
        new_pulse = 0
        file.write(f'{new_pulse}')
        file.close()
        print("Saved pulse have been reset.")