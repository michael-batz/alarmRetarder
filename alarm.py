class Alarm:

	def __init__(self, id, time, message):
		self.id = id
		self.time = time
		self.messgae = message

	def getId(self):
		return self.id

	def getTime(self):
		return self.time

	def getMessage(self):
		return self.message

