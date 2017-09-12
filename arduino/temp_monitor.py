!#/bin/python
import serial

class temperature_controller:
	def __init__(self, which_port, verbose=True):
		self.port = serial.Serial(which_port)
		self.temp = None
	def get_temperature(self, which_sensor):
		self.port.write(bytes(which_sensor))
		self.temp = int(self.port.readline().decode(
				'ascii').strip().split('='))
		if self.verbose:
			print(f' Sensor {which_sensor}:{self.temp}')
		return self.temp
	def close(self):
		self.port.close()

