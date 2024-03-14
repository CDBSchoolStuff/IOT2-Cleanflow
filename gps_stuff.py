class GPS_Stuff:
    from gps_bare_minimum import GPS_Minimum
    from machine import UART
    
    #########################################################################
    # CONFIGURATION
    gps_port = 2
    gps_speed = 9600

    #########################################################################
    # OBJECTS
    uart = UART(gps_port, gps_speed)
    gps = GPS_Minimum(uart)


    #########################################################################
    # Functions

    def get_mqtt_gps(self):
        lat = lon = None
        if self.gps.receive_nmea_data():
            if self.gps.get_latitude() != -999.0 and self.gps.get_longitude() != -999.0 and self.gps.get_validity() == "A":
                lat = str(self.gps.get_latitude())
                lon = str(self.gps.get_longitude())
                return lat + "," + lon + "," + "0.0"
            else:
                print(f"GPS data not valid:\nlatitude: {lat}\nlongtitude: {lon}")
                return False
        else:
            # print("GPS data not available...")
            return False