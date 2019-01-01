class Attribute:
	def __init__(self, name, x=0, y=0):
		self.__label = Text(name, 20, 0)
		self.__x = x
		self.__y = y

	def get_name(self):
		return self.__label.get_text()

	def set_name(self, name):
		self.__label.set_text(name)

	#def paint(self):
