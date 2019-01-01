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

def paint_circle(x=0, y=0, radius=1, detail=12):
	delta = (2*math.pi) / detail

	glBegin(GL_LINE_LOOP)

	for i in range(0, detail):
		glVertex2f(x + math.cos(delta*i)*radius, y + math.sin(delta*i)*radius)

	glEnd()


class JPoint2d:
	def __init__(self, x, y):
		self._x = x
		self._y = y
	def getX(self):
		return self._x
	def getY(self):
		return self._y
	def setX(self, x):
		self._x = x
	def setY(self, y):
		self._y = y
	def __sub__(self, p2):
		return JPoint2d(p2.getX() - self.getX(), p2.getY() - self.getY())
	def __add__(self, p2):
		return JPoint2d(p2.getX() + self.getX(), p2.getY() + self.getY())
	def __div__(self, v):
		return JPoint2d(self.getX() / v, self.getY() / 2)

class JRectangle:
	def __init__(self, width=0, height=0):
		self._tx = 0
		self._ty = 0
		self._width = width
		self._height = height
		self._drawable = True
		self._anchors = []

	def getLimits(self):
		result = {}
		result["left"] = 0
		result["right"] = self._width
		result["bottom"] = 0
		result["top"] = self._height
		return result

	def get_selected(self, x, y):
		result = None
		for anchor in self._anchors:
			 result = anchor.get_selected(x-self._tx, y-self._ty)
			 if result != None:
				 print "Ancora!!!"
				 break
		return result


	def addAnchor(self, a):
		self._anchors.append(a)

	def set_drawable(self, drawable):
		self._drawable = drawable

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def setWidth(self, width):
		self._width = width

	def setHeight(self, height):
		self._height = height

	def paint(self):
		if self._drawable:
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


class JCircle:
	def __init__(self,radius=1):
		self._radius = radius
		self._tx = 0
		self._ty = 0
		self._detail = 20
		self._drawable = True

	def set_drawable(self, drawable):
		self._drawable = drawable

	def getRadius(self):
		return self._radius

	def setRadius(self, r):
		self._radius = r

	def getCenter(self):
		return JPoint2d(self._tx, self._ty)

	def translate(self, tx, ty):
		# Traslo l'entita' rispetto alla sua origine *
		self._tx += tx
		self._ty += ty

	def paint(self):
		if self._drawable:
			glMatrixMode(GL_MODELVIEW)

			glPushMatrix()
			glTranslatef(self._tx, self._ty, 0)
			# Disegno il cerchio con
			delta = (2*math.pi) / self._detail

			glBegin(GL_LINE_LOOP)
			for i in range(0, self._detail):
				glVertex2f(math.cos(delta*i)*self._radius, math.sin(delta*i)*self._radius)
			glEnd()

			glPopMatrix()

	def isSelected(self, x, y):
		# x**2 + y**2
		if math.sqrt((x - self._tx)**2 + (y-self._ty)**2) <= self._radius:
			return True
		else:
			return False
