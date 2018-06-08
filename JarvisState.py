from JarvisGlobals import *

class JarvisState:
	
	def __init__(self):
		self.activityList = [] # list of all activities a state supports
	
	def parse(self, stringToParse):
		for activity in self.activityList:
			parseSuccess,response = activity.parse(stringToParse)
			if parseSuccess != cannotParse:
				return parseSuccess,response
		
		return cannotParse,None