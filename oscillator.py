from parameters import * 
from globals import globals
import math

class Oscillator:
	def __init__(self):
		self.bpm = parameters.bpm
		self.delta_t = parameters.delta_t
		self.residualVolume = parameters.stroke_volume
		self.calculate()

	def calculate(self):
		self.rest = int(math.ceil(((1 - self.bpm / 60.0 * parameters.qrs_interval) / (self.bpm / 60.0)) / parameters.delta_t))
		self.beat = int(math.ceil(self.bpm / 60.0 / parameters.delta_t))
		self.stepVolume = parameters.stroke_volume / self.beat

	def getVelocity(self):
		if self.bpm != parameters.bpm or self.delta_t != parameters.delta_t:
			self.calculate()
		
		remaining = globals.time % (self.rest + self.beat)
		if remaining < self.beat:
			return parameters.sink_velocity
		else:
			return parameters.ejection_velocity
	
	def setlastVolume(self, lastVolume):
		self.residualVolume -= lastVolume

	def getVolume(self):
		if self.bpm != parameters.bpm or self.delta_t != parameters.delta_t:
			self.calculate()
		
		remaining = globals.time % (self.rest + self.beat)
		if remaining < self.beat:
			if ((globals.time - 1) % (self.rest + self.beat)) >= self.beat:
				self.residualVolume = parameters.stroke_volume
		if self.residualVolume >= self.stepVolume:
			return self.stepVolume
		else:
			return self.residualVolume

oscillator = Oscillator()