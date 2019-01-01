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

	def process_point_list(self, plist):
		result = [plist[0]]
		for i in range(0, len(plist)-1):
			result.append((plist[i+1] + plist[i])/2.0)
		result.append( plist[len(plist)-1] )
		return result



	def paint(self):
		points = []
		for control_point in self._control_points:
			points.append(control_point.getCenter())
			control_point.paint()

		p1 = self._control_points[0].getCenter()
		p2 = (self._control_points[1].getCenter() + self._control_points[0].getCenter()) / 2.0
		p3 = (self._control_points[2].getCenter() + self._control_points[1].getCenter()) / 2.0
		p4 = (self._control_points[3].getCenter() + self._control_points[2].getCenter()) / 2.0
		p5 = self._control_points[3].getCenter()




		proc = points
		for i in range(0, 40):
			proc = self.process_point_list(proc)


		glBegin(GL_LINE_STRIP)
		for p in points:
			glVertex2f(p.getX(), p.getY())
		glEnd()


		glBegin(GL_LINE_STRIP)
		for p in proc:
			glVertex2f(p.getX(), p.getY())
		glEnd()
