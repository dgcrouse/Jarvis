import random
from VoiceIOHandler import VoiceIOHandler
from TextIOHandler import TextIOHandler
from HomeAutomationState import HomeAutomationState
from InformationState import InformationState
from JarvisGlobals import *

def selectRandomResponse(responseList):
	return responseList[random.randrange(len(responseList))]

class Jarvis():

	def __init__(self):
		self.myState = None

		self.myStates = []
		self.myStates.append(HomeAutomationState())
		self.myStates.append(InformationState())

		self.ioHandler = VoiceIOHandler()
	
		# Fill out responses
		self.helloResponses = self.loadResponses('responses/hello.txt')
		self.goodbyeResponses = self.loadResponses('responses/goodbye.txt')
		self.affirmativeResponses = self.loadResponses('responses/success.txt')
		self.negativeResponses = self.loadResponses('responses/failure.txt')
		self.errorResponses = self.loadResponses('responses/error.txt')

	def loadResponses(self,responseFilepath):
		responseFile = open(responseFilepath)
		outputLines = []
		for line in [l.lower().strip() for l in responseFile.readlines()]:
			if line != '':
				outputLines.append(line)
		return outputLines

	def respondHello(self):
		self.ioHandler.output(selectRandomResponse(self.helloResponses))

	def respondGoodbye(self):
		self.ioHandler.output(selectRandomResponse(self.goodbyeResponses))

	def respondSuccess(self):
		self.ioHandler.output(selectRandomResponse(self.affirmativeResponses))
	
	def respondFailure(self):
		self.ioHandler.output(selectRandomResponse(self.negativeResponses))

	def respondError(self):
		self.ioHandler.output(selectRandomResponse(self.errorResponses))

	def processInput(self):
		inputString = self.ioHandler.waitForInput()
		if self.myState == None:
			if 'jarvis' in inputString:
				self.myState = self.myStates[0]
				self.ioHandler.setLowPowerMode(False)
				self.respondHello()
		else:
			if 'thank you' in inputString or 'that is all' in inputString:
				self.myState = None
				self.respondGoodbye()
				self.ioHandler.setLowPowerMode(True)
			elif inputString == 'CNU':
				self.ioHandler.output('I couldn\'t understand what you said')
			elif inputString == 'CNC':
				self.ioHandler.output('I cannot connect to the internet right now')
			else:
				parseSuccess, response = self.myState.parse(inputString)
				cnt = 1
				while cnt < len(self.myStates) and parseSuccess == cannotParse:
					stateToTry = self.myStates[cnt]
					if stateToTry != self.myState:
						parseSuccess, response = stateToTry.parse(inputString)
						if(parseSuccess == cannotParse):
							self.myState = stateToTry
					cnt+=1
				if response is not None:
					self.ioHandler.output(response)
				else:
					if parseSuccess == didParse:
						self.respondSuccess()
					elif parseSuccess == errorParse:
						self.respondError()
					else:
						self.respondFailure()

if __name__ == "__main__":
	jarvis = Jarvis()
	while(True):
		jarvis.processInput()
	