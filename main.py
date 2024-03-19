########################################
# OWN MODULES
from adc_sub import ADC_substitute
from battery_status import Battery_Status
from pump_control import Pump_Control
from gps_stuff import GPS_Stuff
from flow_sensor import Flow_Sensor
import mqtt_sender


#import umqtt_robust2 as mqtt
import _thread

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys

#########################################################################
# CONFIGURATION

PIN_BAT = 32
PIN_PUMP = 33
PIN_FLOWSENSOR = 18
MQTT_TOPIC_BATTERY = "mqtt_bat"
MQTT_TOPIC_LITER = "mqtt_liter"


#########################################################################
# OBJECTS

battery_subadc = ADC_substitute(PIN_BAT)  # The battery object
Battery = Battery_Status(battery_subadc)

pump_pOut = Pin(PIN_PUMP, Pin.OUT)
Pump = Pump_Control(pump_pOut)

GPS = GPS_Stuff()

Flow = Flow_Sensor(Pump)


#########################################################################
# Global variables

battery_pct = 0
prev_bat_pct = 0
gps_data = 0
liter = 0
prev_liter = 0

flow_pIn = Pin(PIN_FLOWSENSOR, Pin.IN)
flow_pIn.irq(trigger=Pin.IRQ_FALLING, handler=Flow.callback)



#########################################################################
# STUFF TO RUN ONCE
mqtt_sender.client = mqtt_sender.connect_to_broker() # Connect to MQTT

try:
    file = open("total_pulse.txt", "x") # Ensures that the liter.txt file exists.
    file.close()
except:
    print("File already exists")

#########################################################################
# PROGRAM


battery_status_start = ticks_ms()
battery_status_period_ms = 1000 # 1000ms = 1s

pump_control_start = ticks_ms()
pump_control_period_ms = 1000 # 1000ms = 1s

gps_stuff_start = ticks_ms()
gps_stuff_period_ms = 5000

mqtt_sender_start = ticks_ms()
mqtt_sender_period_ms = 5000

mqtt_connect_start = ticks_ms()
mqtt_connect_period_ms = 20000

flow_sensor_start = ticks_ms()
flow_sensor_period_ms = 1000


#------------------------------------------------------
# MQTT sender thread
        
def mqtt_thread():
    #mqtt_sender.client = mqtt_sender.connect_to_broker() # Connect to MQTT
    while True:
        try:
            global mqtt_connect_start, mqtt_connect_period_ms, mqtt_sender_start, mqtt_sender_period_ms
            if ticks_ms() - mqtt_connect_start > mqtt_connect_period_ms:
                mqtt_connect_start = ticks_ms()
                # Check connection
                try:
                    print("[MQTT] Checking connection.")
                    mqtt_sender.client.connect()
                    print("[MQTT] Connection OK.")
                except:
                    print("[MQTT] Connection failed. Reconnecting...")
                    mqtt_sender.client = mqtt_sender.connect_to_broker() # Connect to MQTT
            
            
            if ticks_ms() - mqtt_sender_start > mqtt_sender_period_ms:
                mqtt_sender_start = ticks_ms()
                
                global battery_pct, prev_bat_pct, MQTT_TOPIC_BATTERY
                # Send data if there is a change (this principle saves power)
                if battery_pct != prev_bat_pct:
                    gps_time = GPS.get_gps_time()
                    data_string = f"{battery_pct} | {gps_time}" # The data to send. CHANGE IT! (Added the "sensor_id")
                    
                    mqtt_sender.send_message(data_string, MQTT_TOPIC_BATTERY)
                        
                    # Update the previous values for use next time
                    prev_bat_pct = battery_pct
                    print(data_string)
                    
                global liter, prev_liter, MQTT_TOPIC_LITER
                # Send data if there is a change (this principle saves power)
                if liter >= 1:
                    
                    gps_time = GPS.get_gps_time()
                    liter_data_string = f"{liter} | {gps_time}" # The data to send. CHANGE IT! (Added the "sensor_id")
                    
                    mqtt_sender.send_message(liter_data_string, MQTT_TOPIC_LITER)
                    
                    Flow.reset_saved_liter()
                    # Update the previous values for use next time
                    prev_liter = liter
                    print(liter_data_string)
                
                    
        except KeyboardInterrupt:
            print('Ctrl-C pressed...exiting')
            mqtt_sender.client.disconnect()
            sys.exit()

_thread.start_new_thread(mqtt_thread, ())


#------------------------------------------------------
# Main program
while True:
    try:
        
        #------------------------------------------------------
        # Flow Sensor
        if ticks_ms() - flow_sensor_start > flow_sensor_period_ms:
            flow_sensor_start = ticks_ms()
            
            liter = Flow.get_total_liter()
            print("Total Liter:", liter)
        
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
            
            # Runs the pump controller code on an interval. Ensuring that the pump turns off.
            Pump.controller(Flow.pulse)
            #Pump.pump_control()
            #Pump.pump_test()

        #------------------------------------------------------
        # GPS Stuff
        
        if ticks_ms() - gps_stuff_start > gps_stuff_period_ms:
            gps_stuff_start = ticks_ms()
            
            #gps_data = GPS.get_mqtt_gps()
            #gps_time = GPS.get_gps_time()
            #print(f"GPS data: {gps_data}")

    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt_sender.client.disconnect()
        sys.exit()