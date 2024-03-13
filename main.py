from battery_status import Battery_Status
#from gps_stuff import GPS_Stuff

########################################
# OWN MODULES
from adc_sub import ADC_substitute


#import umqtt_robust2 as mqtt
#import _thread

#from machine import ADC, Pin
from time import ticks_ms, sleep
import sys

#########################################################################
# CONFIGURATION

pin_adc_bat = 32


#########################################################################
# OBJECTS

battery_subadc = ADC_substitute(pin_adc_bat)  # The battery object
Battery = Battery_Status(battery_subadc)
# GPS = GPS_Stuff()



#########################################################################
# PROGRAM

battery_status_start = ticks_ms()
battery_status_period_ms = 1000 # 1000ms = 1s

#gps_stuff_start = ticks_ms()
#gps_stuff_period_ms = 1000


while True:
    try:
        #------------------------------------------------------
        # Battery Status
        
        if ticks_ms() - battery_status_start > battery_status_period_ms:
            battery_status_start = ticks_ms()
            
            battery_pct = Battery.get_battery_status()
            print("Battery Pct: " + battery_pct)
        #------------------------------------------------------
        # GPS Stuff
        
        # if ticks_ms() - gps_stuff_start > gps_stuff_period_ms:
        #     gps_stuff_start = ticks_ms()
            
        #     print(GPS.get_adafruit_gps())
        
    

    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        #mqtt.c.disconnect()
        sys.exit()
        
