!#/bin/python
import serial
import time


class temperature_controller:
	def __init__(self, which_port, verbose=True):
		self.port = serial.Serial(which_port)
		
		self.temp = None
		self.mash_start_time = None
		self.boil_start_time = None

		self.sensors = {'HLT':0,
				'Mash':1,
				'Boil':2}

	def get_temperature(self, which_sensor):
		if which_sensor in self.sensors:
			which_sensor = self.sensors[which_sensor]
		self.port.write(bytes(which_sensor))
		self.which_sensor = int(self.port.readline().decode(
				'ascii').strip().split('='))
		if self.verbose:
			print(f' Sensor {which_sensor}:{self.temp}')
		return self.temp

	
	def set_desired_temperature(self, which_sensor, desired_temp):
		self.which_sensor_setpoint = float(desired_temp)


	def close(self):
		self.port.close()

if __name__ == '__main__':
	pass
