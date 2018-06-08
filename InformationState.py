from JarvisState import JarvisState
from TimeActivity import TimeActivity

class InformationState(JarvisState):
	
	def __init__(self):
		JarvisState.__init__(self)
		self.activityList.append(TimeActivity())