from JarvisState import JarvisState
from HueActivity import HueActivity

class HomeAutomationState(JarvisState):
	
	def __init__(self):
		JarvisState.__init__(self)
		self.activityList.append(HueActivity())