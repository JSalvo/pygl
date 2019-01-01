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


class Bezier:
	def __init__(self):
		self._control_points = []
		self._control_points.append(JCircle(10))
		self._control_points.append(JCircle(10))
		self._control_points.append(JCircle(10))
		self._control_points.append(JCircle(10))


	def get_selected(self, x, y):
		result = None

		for control_point in self._control_points:
			if control_point.isSelected(x, y):
				result = control_point
				break

		return result

	def paint(self):
		points = []
		for control_point in self._control_points:
			points.append(control_point.getCenter())
			control_point.paint()

		# Visualizza i punti di controllo
		glBegin(GL_LINE_STRIP)
		for p in points:
			glVertex2f(p.getX(), p.getY())
		glEnd()

		glBegin(GL_LINE_STRIP)
		for i in range(0, 100):
			t = i / 100.0
			# Formula parametrica della Curva di Bezier cubica
			p = points[0]*(1-t)**3 + points[1]*3*t*(1-t)**2 + points[2]*3*t**2*(1-t) + points[3]*t**3
			glVertex2f(p.getX(), p.getY())
		glEnd()
