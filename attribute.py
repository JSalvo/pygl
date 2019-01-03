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
from quadrilaterals import JCircle, Text


class Attribute(JCircle):
	def __init__(self, name):
		JCircle.__init__(self, 40)
		self._label = Label(name)
		self._primary_key = False

	def setPrimaryKey(self, value):
		self._primary_key = value
		if value:
			self._background_color = QColor(255,255,255)
		else:
			self._background_color = QColor(0, 0, 0)

	def get_name(self):
		return self._label.get_text()

	def set_name(self, name):
		self._label.set_text(name)

	def get_selected(self, x, y):
		result = None
		if self._visible or True:
			result = self._label.get_selected(x - self._tx, y - self._ty)

			if result != None:
				return result

			elif self.isSelected(x, y):
				return self

		return result

	def paint(self, paintHidden=False):
		#self.setOpenGlColor()
		if self.getVisibility() or paintHidden:
			JCircle.paint(self)
			glPushMatrix()
			glTranslatef(self._tx, self._ty, 0)
			self._label.paint()
			glPopMatrix()
