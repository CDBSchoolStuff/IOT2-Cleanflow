
# This is all code for establishing network connection in preperation for MQTT communication.
# Complete project details at https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

import network
import esp
esp.osdebug(None)
import gc
gc.collect()


from credentials import credentials

# try:
#     ssid = credentials['ssid']
#     password = credentials['password']

#     station = network.WLAN(network.STA_IF)

#     station.active(True)
#     station.connect(ssid, password)
    
#     while station.isconnected() == False:
#         pass
#     print('Connection successful')
#     print(station.ifconfig())
    
# except: # Except tilføjet for at lade koden køre uden forbindelse til netværk.
#     print("Network connection failed.")
    
ssid = credentials['ssid']
password = credentials['password']

station = network.WLAN(network.STA_IF)

try:
    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass

    print('Connection successful')
    print(station.ifconfig())
    
except: # Except tilføjet for at lade koden køre uden forbindelse til netværk.
    print("Network connection failed.")