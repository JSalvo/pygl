import sys
import PyQt4
from PyQt4 import QtGui, QtOpenGL
from PyQt4.QtGui import QWidget, QHBoxLayout, QColor
from PyQt4.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL import GLUT
import math
from PyQt4 import Qt


class Scene:
	def __init__(self):
		self.entities = []
		self._pan_x = 0
		self._pan_y = 0
	def add_entity(self, entity):
		self.entities.append(entity)
	def get_selected(self, x, y):
		selected = None
		for e in self.entities:
			selected = e.get_selected(x - self._pan_x , -self._pan_y + y)
			if selected != None:
				break
		return selected
	def pan(self, x, y):
		self._pan_x += x
		self._pan_y += y
	def paint(self, drawHidden=False):
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glTranslatef(self._pan_x, self._pan_y, 0)
		for entity in self.entities:
			entity.paint(drawHidden)
		glPopMatrix()
