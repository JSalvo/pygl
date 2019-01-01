import sys
import PyQt4
from PyQt4 import QtGui, QtOpenGL
from PyQt4.QtGui import QWidget, QHBoxLayout, QColor
from PyQt4.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL import GLUT
import math
from PyQt4 import Qt

from text import Text

class JRectangle:
	def __init__(self, width, height):
		self._tx = 0
		self._ty = 0
		self._width = width
		self._height = height

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def setWidth(self, width):
		self._width = width

	def setHeight(self, height):
		self._height = height

	def paint(self):
		glMatrixMode(GL_MODELVIEW)

		glPushMatrix()
		# La posizine del rettancolo viene resa, attraverso una traslazione
		# relativamente alla sua origine*
		glTranslatef(self._tx, self._ty, 0)
		# Disegno il rettangolo
		glBegin(GL_LINE_LOOP)
		glVertex2f(0, 0)
		glVertex2f(self._width, 0)
		glVertex2f(self._width, self._height)
		glVertex2f(0, self._height)
		glEnd()

		glPopMatrix()

		def translate(self, tx, ty):
			# Traslo l'entita' rispetto alla sua origine *
			self._tx += tx
			self._ty += ty

	def isSelected(self, x, y):
		# Se il punto x, y e' contenuto nel rettangolo
		# produce questo oggetto, altrimenti ...
		if ((x >= self._tx) and (x <= self._tx + self._width) and (y >= self._ty) and (y <= self._ty + self._height)):
			return True
		else:
			return False

# * "L'origine e' l'angolo basso sinistro del rettangolo "
