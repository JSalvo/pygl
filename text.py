import sys
import PyQt4
from PyQt4 import QtGui, QtOpenGL
from PyQt4.QtGui import QWidget, QHBoxLayout, QColor
from PyQt4.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL import GLUT
import math
from PyQt4 import Qt

class Text:
	# x e y sono la posizione relativa del testo
	def __init__(self, text=[], x=0, y=0):
		self.__text = text
		self.__x = x
		self.__y = y

	def set_position(self, x, y):
		self.__x = x
		self.__y = y

	def set_text(self, text):
		self.__text = text

	def get_text(self):
		return self.__text

	def paint(self):
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glTranslatef(self.__x, self.__y, 0)

		for i in range(0, len(self.__text)):
			GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_MONO_ROMAN, ord(self.__text[i]))

		glPopMatrix()

	def __len__(self):
		return len(self.__text)
