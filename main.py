########################################
# OWN MODULES
from adc_sub import ADC_substitute
from battery_status import Battery_Status
from pump_control import Pump_Control
from gps_stuff import GPS_Stuff
import flow_sensor
import mqtt_sender


#import umqtt_robust2 as mqtt
#import _thread

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys

#########################################################################
# CONFIGURATION

PIN_BAT = 32
PIN_PUMP = 33
PIN_FLOWSENSOR = 12
MQTT_TOPIC_BATTERY = "mqtt_bat"


#########################################################################
# OBJECTS

battery_subadc = ADC_substitute(PIN_BAT)  # The battery object
Battery = Battery_Status(battery_subadc)

pump_pOut = Pin(PIN_PUMP, Pin.OUT)
Pump = Pump_Control(pump_pOut)

GPS = GPS_Stuff()


#########################################################################
# Global variables

battery_pct = 0
prev_bat_pct = 0
gps_data = 0
global pulse

flow_pIn = Pin(PIN_FLOWSENSOR, Pin.IN)
flow_pIn.irq(trigger=Pin.IRQ_FALLING, handler=flow_sensor.callback)



#########################################################################
# STUFF TO RUN ONCE
mqtt_sender.client = mqtt_sender.connect_and_subscribe() # Connect to MQTT

#########################################################################
# PROGRAM

battery_status_start = ticks_ms()
battery_status_period_ms = 1000 # 1000ms = 1s

pump_control_start = ticks_ms()
pump_control_period_ms = 10000 # 1000ms = 1s

gps_stuff_start = ticks_ms()
gps_stuff_period_ms = 5000

mqtt_sender_start = ticks_ms()
mqtt_sender_period_ms = 1000

flow_sensor_start = ticks_ms()
flow_sensor_period_ms = 1000



while True:
    try:
        
        #------------------------------------------------------
        # Flow Sensor
            
        #flow_pIn.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=flow_sensor.callback(flow_pIn))
        
        #------------------------------------------------------
        # Battery Status
        if ticks_ms() - battery_status_start > battery_status_period_ms:
            battery_status_start = ticks_ms()
            
            battery_pct = Battery.get_battery_pct()
            print("Batteri procent:", battery_pct, "%")


        #------------------------------------------------------
        # Pump Controller
        
        if ticks_ms() - pump_control_start > pump_control_period_ms:
            pump_control_start = ticks_ms()
            
            #Pump.pump_test()

        #------------------------------------------------------
        # GPS Stuff
        
        if ticks_ms() - gps_stuff_start > gps_stuff_period_ms:
            gps_stuff_start = ticks_ms()
            
            #gps_data = GPS.get_mqtt_gps()
            #gps_time = GPS.get_gps_time()
            #print(f"GPS data: {gps_data}")
        
        #------------------------------------------------------
        # MQTT sender
        #mqtt_sender.run_once()
        
        if ticks_ms() - mqtt_sender_start > mqtt_sender_period_ms:
            mqtt_sender_start = ticks_ms()
            
            # Send data if there is a change (this principle saves power)
            if battery_pct != prev_bat_pct:
                gps_time = GPS.get_gps_time()
                data_string = f"{battery_pct} | {gps_time}" # The data to send. CHANGE IT! (Added the "sensor_id")
                
                mqtt_sender.send_message(data_string, MQTT_TOPIC_BATTERY)
                    
                # Update the previous values for use next time
                prev_bat_pct = battery_pct
                print(data_string)

    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        #mqtt.c.disconnect()
        sys.exit()
        