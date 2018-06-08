import os
from phue import Bridge
from HomeAutomationActivity import *
from JarvisGlobals import *

def modAction(data):
	return{"action":data}
actionTypeModifier = Parse.TypeModifier(None, modAction, "")

def modObject(data):
	return {"object":data}
objectTypeModifier = Parse.TypeModifier(None, modObject, "")

def combineMapsFn(data):
	result = {}
	for item in data:
		for key in item:
		    result[key] = item[key]
	return result
combineMaps = Parse.TypeModifier(None, combineMapsFn, "")

class HueActivity(HomeAutomationActivity):

	def __init__(self):
		HomeAutomationActivity.__init__(self)
		# Parse config from file
		if os.path.exists('configs/HueActivity.txt'):
			hueConfigFile = open('configs/HueActivity.txt')
			hueConfig = hueConfigFile.readlines()
			hueConfigFile.close()
			self.bridge = Bridge(hueConfig[0].strip())

			# if not connected for the first time
			if len(hueConfig) < 2 or hueConfig[1].strip().lower() != 'true':
				print 'Press button now'
								
				self.bridge.connect()
				hueConfigFile = open('configs/HueActivity.txt','w')
				hueConfigFile.write(hueConfig[0])
				hueConfigFile.write('True')
		
			self.devices = {}
			light_objs = self.bridge.get_light_objects('name')
			for name in light_objs:
				self.devices[name.lower()] = light_objs[name]

			# define grammar
			lights = noOp()
			for light in self.devices:
				lights = string(light) | lights
		
			verbList = ['on','off','dim','brighten', 'dimmer', 'brighter']

			verbs = noOp()
			for verb in verbList:
				verbs = string(verb) | verbs
		
			objectRef = ~string("the")["0-1"] >> ((lights / string('it')) % objectTypeModifier)['0-1'] >> ~string("light")["0-1"]

			actionOrder1 = objectRef >> (verbs % actionTypeModifier)
			actionOrder2 = (verbs % actionTypeModifier) >> objectRef

		
			self.grammar = ~string("turn")['0-1'] >> (actionOrder1 / actionOrder2) % combineMaps >> end()
			self.grammar.setWhitepspace(standardWhitespace())
			
		else:
			return None

	def lightSwitch(self,deviceName, toOn):
		if deviceName not in self.devices.keys():
			return False
		self.currentDevice = deviceName
		self.devices[deviceName].on = toOn
		return True

	# Brightness from 0-254
	def lightDim(self,deviceName,goUp):
		if deviceName not in self.devices.keys():
			return False
		self.currentDevice = deviceName
		currentBrightness = self.devices[deviceName].brightness
		self.devices[deviceName].transitiontime = 4
		if goUp:
			self.devices[deviceName].brightness = min(currentBrightness + 25,254)
		else:
			self.devices[deviceName].brightness = max(currentBrightness - 25, 0)
		return True

	def parse(self,stringToParse):
		
		try:
			data = self.grammar.parse(stringToParse)
			print data
			if 'object' not in data or data['object'] == 'it':
				if self.currentDevice == None:
					return errorParse,"Please request a device"
			else:
				self.currentDevice = data['object']

			if data['action'] == 'on':
				self.lightSwitch(self.currentDevice,True)
			elif data['action'] == 'off':
				self.lightSwitch(self.currentDevice,False)
			elif 'dim' in data['action']:
				self.lightDim(self.currentDevice,False)
			elif 'bright' in data['action']:
				self.lightDim(self.currentDevice,True)				

			return didParse,None
		except:
			return cannotParse,None
			