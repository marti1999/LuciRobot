import serial
import json 

class Sensors:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=0)

        # ho tenim com objecte per si volem accedir desde python pero per el websocket enviare el json
        self.gas_concentration = 0.0
        self.ultrasound_sensor_1_distance = 0.0
        self.dht11_humidity = 0.0
        self.dht11_temp = 0.0
        
        self.ser.reset_input_buffer()
    
    def parse_sensors(self, json_text):
        print("Parsing: " + str(json_text))
        print(len(json_text))
        json_dict = json.loads(json_text)

        self.gas_concentration = json_dict['gas_concentration']
        self.ultrasound_sensor_1_distance = json_dict['ultrasound_sensor_1_distance']
        self.dht11_humidity = json_dict['dht11_humidity']
        self.dht11_temp = json_dict['dht11_temp']
        
        return json_text

    def error_data(self):
        json_text = {}
        json_text["gas_concentration"] = 0.0
        json_text["ultrasound_sensor_1_distance"] = 0.0
        json_text["dht11_humidity"] = 0.0
        json_text["dht11_temp"] = 0.0
        
        app_json = json.dumps(json_text)

        return str(json_text)

    def read_sensors(self):
        if self.ser.in_waiting > 0:
            json_text = self.ser.readline().decode('utf-8')

            if json_text is None:
                return self.error_data()
            
            return self.parse_sensors(json_text)
        else:
            print("No data available from arduino yet.")
            return self.parse_sensors(self.error_data())
        
    
    def close(self):
        self.ser.close()
    
