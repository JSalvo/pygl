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
from quadrilaterals import JCircle, JObject


class Bezier(JObject):
	def __init__(self):
		JObject.__init__(self)
		self._control_points = []
		self._qGray = QColor(100,100,100)
		self._qRed = QColor(245, 66, 78)

		p1 = JCircle(40)
		p1.setVisibility(False)
		p1.setColor(self._qGray)

		p2 = JCircle(40)
		p2.setVisibility(False)
		p2.setColor(self._qGray)

		p3 = JCircle(40)
		p3.setVisibility(False)
		p3.setColor(self._qGray)

		p4 = JCircle(40)
		p4.setVisibility(False)
		p4.setColor(self._qGray)


		self._control_points.append(p1)
		self._control_points.append(p2)
		self._control_points.append(p3)
		self._control_points.append(p4)

	# Trasla solo i due punti di controllo centrali
	def translate_2central_points(self, tx, ty):
		self._control_points[1].translate(tx, ty)
		self._control_points[2].translate(tx, ty)


	def get_selected(self, x, y):
		result = None

		if self._visible:
			for control_point in self._control_points:
				if control_point.isSelected(x, y):
					result = control_point
					break

		return result

	def paint(self, paintHidden=False):
		self.setOpenGlColor()
		if self.getVisibility() or paintHidden:
			points = []
			for control_point in self._control_points:
				points.append(control_point.getCenter())
				control_point.paint(paintHidden)

			if paintHidden:
				glColor3f(self._qGray.red()/255.0, self._qGray.green()/255.0, self._qGray.blue()/255.0 )
				# Visualizza le linee di controllo
				glBegin(GL_LINE_STRIP)
				for p in points:
					glVertex2f(p.getX(), p.getY())
				glEnd()

			glColor3f(self._qRed.red()/255.0, self._qRed.green()/255.0, self._qRed.blue()/255.0 )
			glBegin(GL_LINE_STRIP)

			for i in range(0, 100):
				t = i / 100.0
				# Formula parametrica della Curva di Bezier cubica
				p = points[0]*(1-t)**3 + points[1]*3*t*(1-t)**2 + points[2]*3*t**2*(1-t) + points[3]*t**3
				glVertex2f(p.getX(), p.getY())
			glEnd()
