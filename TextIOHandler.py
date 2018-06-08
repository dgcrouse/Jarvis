from JarvisIOHandler import JarvisIOHandler

class TextIOHandler(JarvisIOHandler):

	def waitForInput(self):
		return raw_input('>').lower().strip()

	def output(self,text_to_output):
		print text_to_output