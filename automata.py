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
from bezier import Bezier
from quadrilaterals import JCircle, Text, near_to_zero, JPoint2d


class AutomataState(JCircle):
	def __init__(self, name):
		JCircle.__init__(self, 200)
		self._label = Label(name)
		self._label.translate(-self._label.getWidth()/2.0, -self._label.getHeight()/2.0)
		self._links_to = []

	def get_name(self):
		return self._label.get_text()

	def set_name(self, name):
		self._label.set_text(name)

	def get_selected(self, x, y):
		result = None

		if self._visible:
			if self.isSelected(x, y):
				return self

		return result

	def add_link_to(self, link):
		self._links_to.append(link)

	def paint(self, paintHidden=False):
		#self.setOpenGlColor()
		if self.getVisibility() or paintHidden:
			JCircle.paint(self)
			glPushMatrix()
			glTranslatef(self._tx, self._ty, 0)
			self._label.paint()
			glPopMatrix()

class AutomataArc(Bezier):
	def __init__(self, s1, s2):
		Bezier.__init__(self)
		self._control_points[0] = s1
		self._control_points[3] = s2


	def check(self, t, d):
		p = p1*(1-t)**3 + p2*3*t*(1-t)**2 + p3*3*t**2*(1-t) + p4*t**3

	def get_border_points(self, d1, d2):
		p1 = self._control_points[0].getCenter()
		p2 = self._control_points[1].getCenter()
		p3 = self._control_points[2].getCenter()
		p4 = self._control_points[3].getCenter()

		ph = JPoint2d(0, 0)
		pq = JPoint2d(0, 0)

		counter = 0

		ti=0.5
		tf=1
		t = 0.5

		p = p1*(1-t)**3 + p2*3*t*(1-t)**2 + p3*3*t**2*(1-t) + p4*t**3
		d = p.distance(p4)

		if d >= d2:
			while ( not near_to_zero(d - d2) and ti >= 0.5 ):
				print "%f, %f"%(d, d2)
				print "%f, %f, %f"%(ti, t, tf)

				print counter

				if d < d2:
					tf = t
				else:
					ti = t


				t = ti + (tf - ti) / 2.0

				p = p1*(1-t)**3 + p2*3*t*(1-t)**2 + p3*3*t**2*(1-t) + p4*t**3
				d = p.distance(p4)
				counter += 1

			pq = p

			ti=0.5
			tf=1
			t = 0.5

			p = p1*(1-t)**3 + p2*3*t*(1-t)**2 + p3*3*t**2*(1-t) + p4*t**3
			d = p.distance(p4)
			counter = 0
			while ( not near_to_zero(d - d1) and ti >= 0.5 ):
				print counter
				if d < d1:
					tf = t
				else:
					ti = t

				t = ti + (tf - ti) / 2.0

				p = p1*(1-t)**3 + p2*3*t*(1-t)**2 + p3*3*t**2*(1-t) + p4*t**3
				d = p.distance(p4)
				counter += 1
			ph = p

		return (ph, pq)


	def paint(self, paintHidden=False):
		Bezier.paint(self, paintHidden)
		p1 = None
		pm = None
		(p1, pm) = self.get_border_points(200, 300)

		v = p1 - pm

		v = v.normalize()
		v = JPoint2d(-v.getY(), v.getX())

		p2 = pm + v*30
		p3 = pm - v*30

		glColor3f(0, 1, 0)
		glBegin(GL_TRIANGLES)
		glVertex2f(p1.getX(), p1.getY())
		glVertex2f(p2.getX(), p2.getY())
		glVertex2f(p3.getX(), p3.getY())
		#glVertex2f(pm.getX(), pm.getY())
		glEnd()
