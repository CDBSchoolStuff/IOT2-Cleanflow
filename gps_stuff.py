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

    def get_gps_location(self):
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
    
    def get_gps_time(self):
        if self.gps.receive_nmea_data():
            gps_seconds = self.gps.get_utc_seconds()
            gps_minutes = self.gps.get_utc_minutes()
            gps_hours = self.gps.get_utc_hours()
            gps_day = self.gps.get_utc_day()
            gps_month = self.gps.get_utc_month()
            gps_year = self.gps.get_utc_year()
            return f"{gps_year}-{gps_month}-{gps_day}T{gps_hours}:{gps_minutes}:{gps_seconds}"
        else:
            # print("GPS data not available...")
            return False
        