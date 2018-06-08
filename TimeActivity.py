from JarvisGlobals import *
from JarvisActivity import *
from pyscr.Parser.RuleBook import *
from pyscr.Parser.Parse import *
import time


class TimeActivity(JarvisActivity):

	def __init__(self):
		# define grammar
		JarvisActivity.__init__(self)
		actionOrder1 = string('time') >> string('is') >> string('it')
		actionOrder2 = string('is') >> string('the') >> string('time')

	
		self.grammar = ~string("what") >> (actionOrder1 / actionOrder2) >> end()
		self.grammar.setWhitepspace(standardWhitespace())


	def parse(self,stringToParse):

		try:
			self.grammar.parse(stringToParse)
			return didParse,'it is {0}'.format(time.strftime('%I:%M %p'))
		except:
			return cannotParse,None