from battery_status import Battery_Status
#from gps_stuff import GPS_Stuff
from pump_control import Pump_Control

########################################
# OWN MODULES
from adc_sub import ADC_substitute



#import umqtt_robust2 as mqtt
#import _thread

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys

#########################################################################
# CONFIGURATION

PIN_BAT = 32
PIN_PUMP = 33

#########################################################################
# OBJECTS

battery_subadc = ADC_substitute(PIN_BAT)  # The battery object
Battery = Battery_Status(battery_subadc)
# GPS = GPS_Stuff()

pump_pOut = Pin(PIN_PUMP, Pin.OUT)
Pump = Pump_Control(pump_pOut)


#########################################################################
# PROGRAM

battery_status_start = ticks_ms()
battery_status_period_ms = 1000 # 1000ms = 1s

#gps_stuff_start = ticks_ms()
#gps_stuff_period_ms = 1000

pump_control_start = ticks_ms()
pump_control_period_ms = 1000 # 1000ms = 1s

while True:
    try:
        #------------------------------------------------------
        # Battery Status
        if ticks_ms() - battery_status_start > battery_status_period_ms:
            battery_status_start = ticks_ms()
            
            battery_pct = Battery.get_battery_pct()
            print("Batteri procent:", battery_pct, "%")


        #------------------------------------------------------
        # Battery Status
        
        if ticks_ms() - pump_control_start > pump_control_period_ms:
            pump_control_start = ticks_ms()
            
            Pump.pump_test()

        #------------------------------------------------------
        # GPS Stuff
        
        # if ticks_ms() - gps_stuff_start > gps_stuff_period_ms:
        #     gps_stuff_start = ticks_ms()
            
        #     print(GPS.get_adafruit_gps())
    

    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        #mqtt.c.disconnect()
        sys.exit()
        
