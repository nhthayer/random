import serial
import time


class temperature_controller:
    def __init__(self, which_port, verbose=True):
        self.port = serial.Serial(which_port)
        self.verbose = verbose
        self.port.readline() # Blocks until start message is written
        self.temp = None
        self.mash_start_time = None
        self.boil_start_time = None
        self.sensors = {'HLT': 0, 'Mash': 1, 'Boil': 2}

    def get_temperature(self, which_sensor):
        if which_sensor not in self.sensors:
            raise UserWarning(f'{which_sensor} not in named sensors')
        sensor_index = self.sensors[which_sensor]
        if self.verbose:
            print(f'-> {sensor_index}')
        self.port.write(bytes('%s' % sensor_index, 'ascii'))
        reading = float(
            self.port.readline().decode('ascii').strip().split('=')[1])
        setattr(self, f'{which_sensor}_temp', reading)
        return reading

    def set_desired_temperature(self, which_sensor, desired_temp):
        setattr(self, f'{which_sensor}_setpoint', float(desired_temp))

    def close(self):
        self.port.close()

if __name__ == '__main__':
    sensor = temperature_controller('/dev/cu.usbmodem1421')
    for i in range(10):
        print('HLT:',  sensor.get_temperature('HLT'))
        print('Mash:', sensor.get_temperature('Mash'))
        print('Boil',  sensor.get_temperature('Boil'))
    sensor.close()
