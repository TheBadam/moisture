from machine import ADC, Pin

soil = ADC(Pin(26)) # Soil moisture PIN reference
 
#Calibraton values
MIN_MOISTURE=17940
MAX_MOISTURE=44410

def read_sensor():
    # read moisture value and convert to percentage into the calibration range
    readings = {
        "moisture": {
            "value": (MAX_MOISTURE-soil.read_u16())*100/(MAX_MOISTURE-MIN_MOISTURE),
            "unit": "%"
        }
    }
    return readings