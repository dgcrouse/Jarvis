class JarvisIOHandler:

	def __init__(self):
		self._isLowPower = True
	
	def setLowPowerMode(self,powerMode):
		self._isLowPower = powerMode

	def waitForInput(self):
		return None
	
	def output(self,text_to_output):
		return None
		