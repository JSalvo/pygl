import sys
import PyQt4
from PyQt4 import QtGui, QtOpenGL
from PyQt4.QtGui import QWidget, QHBoxLayout, QColor
from PyQt4.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL import GLUT
import math
from PyQt4 import Qt

from label import Label
from quadrilaterals import JCircle


class Attribute(JCircle):
	def __init__(self, name):
		JCircle.__init__(self, 40)
		self._label = Label(name)

	def get_name(self):
		return self._label.get_text()

	def set_name(self, name):
		self._label.set_text(name)

	def get_selected(self, x, y):
		result = None

		result = self._label.get_selected(x - self._tx, y - self._ty)

		if result != None:
			return result

		elif self.isSelected(x, y):
			return self

		return result

	def paint(self):
		JCircle.paint(self)
		glPushMatrix()
		glTranslatef(self._tx, self._ty, 0)
		self._label.paint()
		glPopMatrix()
