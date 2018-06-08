from JarvisGlobals import *
from pyscr.Parser.RuleBook import *
from pyscr.Parser.Parse import *

class JarvisActivity:
	
	def __init__(self):
		self.grammar = noOp()

	# This is the only required function. Returns result of parsing.
	def parse(self, stringToParse):
		return cannotParse,None