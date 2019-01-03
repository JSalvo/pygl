#!/usr/bin/python
# INSTALLARE PYTHONQT4
# INSTALLARE PYTHON-OPENGL
# INSTALLARE PYTHON-QT4-GL
# INSTALLARE python-tk

import sys
import PyQt4
from PyQt4 import QtGui, QtOpenGL
from PyQt4.QtGui import QWidget, QHBoxLayout, QColor
from PyQt4.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL import GLUT
import math
from PyQt4 import Qt


from entity import Entity
from scene import Scene
from attribute import Attribute
from bezier import Bezier

from quadrilaterals import JCircle, Link
from anchor import Anchor
from automata import AutomataState, AutomataArc

Key_Tab = int("0x01000001", 16)
Key_Shift = int("0x01000020", 16)
Key_Control = int("0x01000021", 16)

def paint_circle(x=0, y=0, radius=1, detail=12):
	delta = (2*math.pi) / detail

	glBegin(GL_LINE_LOOP)

	for i in range(0, detail):
		glVertex2f(x + math.cos(delta*i)*radius, y + math.sin(delta*i)*radius)

	glEnd()


class GLWidget(QGLWidget):

	def __init__(self, parent):
		# Inizializza Antenato
		QGLWidget.__init__(self, parent)
		self._zoom_factor = 1.0
		self._pan_x = 0
		self._pan_y = 0

		self.scene = Scene()

		self._drawHidden = False

		customer = Entity("Customer")
		self.scene.add_entity(customer)

		order = Entity("Order")
		order.set_drawable(True)
		self.scene.add_entity(order)

		age = Attribute("Age")
		age.setPrimaryKey(True)
		order.add_attribute(age)

		anchor = Anchor()
		anchor.anchor_to_rectangle(order)

		bezier = Bezier()
		#self.scene.add_entity(bezier)

		link1 = Link(anchor, age)
		order.addLink(link1)

		s0 = AutomataState("S0")
		s1 = AutomataState("S1")
		arc = AutomataArc(s0, s1)
		arc2 = AutomataArc(s0, s0)
		arc3 = AutomataArc(s1, s1)

		self.scene.add_entity(arc)
		self.scene.add_entity(arc2)
		self.scene.add_entity(arc3)
		self.scene.add_entity(s0)
		self.scene.add_entity(s1)




		self._mid_down_x = None
		self._mid_down_y = None

		self._mid_up_x = None
		self._mid_up_y = None


		self._left_down_x = None
		self._left_down_y = None

		self._left_up_x = None
		self._left_up_y = None

		self._last_mid_down_x = None
		self._last_mid_down_y = None


		self._tab_down = False

		self._selected_object = None

	def panY(self, pan_y):
		self._pan_y += pan_y
		self.refresh()

	def setHiddenVisibility(self, drawHidden):
		self._drawHidden = drawHidden
		self.refresh()

	def setHiddenVisibilitySwitch(self):
		if self._drawHidden:
			self._drawHidden = False
		else:
			self._drawHidden = True
		self.refresh()

	def panX(self, pan_x):
		self._pan_x += pan_x
		self.refresh()


	def panXY(self, pan_x, pan_y):
		self._pan_y += pan_y
		self._pan_x += pan_x
		self.refresh()

	def add_zoom(self, value):
		self._zoom_factor += value

		if self._zoom_factor < 1:
			self._zoom_factor = 1
		self.refresh()


	def refresh(self):
		self.initializeGL()
		self.updateGL()

	def initializeGL(self):
		GLUT.glutInit([], [])

		black = QColor(0,0,0)
		white = QColor(255,255,255)

		# Imposto colore di cancellazione
		self.qglClearColor(black)


		glViewport(0, 0, self.width(), self.height())
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		glOrtho(0.0, self.width(), 0.0, self.height(), -1.0, 1.0)
		glTranslatef(self.width()/2.0, +self.height()/2.0, 0)
		glScalef(1.0 / self._zoom_factor, 1.0 / self._zoom_factor, 1)
		glTranslatef(-self.width()/2.0 , -self.height()/2.0, 0)


	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT);
		glColor3f(1, 1, 1)


		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)
		glEnable(GL_LINE_SMOOTH)
		glLineWidth(2.0)

		self.scene.paint(self._drawHidden)

		#paint_circle(30, 30, 20, 12)

		glFlush()

	def resizeGL(self, w, h):
		glViewport(0, 0, self.width(), self.height())
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		glOrtho(0.0, self.width(), 0.0, self.height(), -1.0, 1.0)
		glTranslatef(self.width()/2.0, +self.height()/2.0, 0)
		glScalef(1.0 / self._zoom_factor, 1.0 / self._zoom_factor, 1)
		glTranslatef(-self.width()/2.0 , -self.height()/2.0, 0)


	def midDownDetected(self, x, y):
		self._mid_down_x = x
		self._mid_down_y = y
		self._mid_up_x = None
		self._mid_up_y = None

	def print_click(self, x, y):
		print "x: %d, y: %d"%self.xy_from_screen_to_model(x, y)

	# Converte le coordinate "schermo" x, y in coordinate "modello"
	def xy_from_screen_to_model(self, x, y):
		y = self.height() - y
		return (((x - self.width() / 2.0) * self._zoom_factor) + (self.width() / 2.0), ((y -self.height() / 2.0) * self._zoom_factor) + (self.height() / 2.0))


	def mouseMoveDetected(self, x, y):
		if self._tab_down:
			if self._mid_down_x != None and self._mid_down_y != None:

				#print "Fai un pan"
				delta_x = x - self._mid_down_x
				delta_y = y - self._mid_down_y

				self.panXY(delta_x, delta_y)
				self.scene.pan((1.0 * delta_x) * self._zoom_factor, -(1.0 * delta_y)  * self._zoom_factor)

			self._mid_down_x = x
			self._mid_down_y = y

	def midUpDetected(self, x, y):
		self._mid_down_x = None
		self._mid_down_y = None

		self._mid_up_x = x
		self._mid_up_y = y

	def tabDownDetected(self):
		self._tab_down = True
		print "Tab giu"

	def tabUpDetected(self):
		self._tab_down = False
		print "Tab su"

	def mousePressEvent(self, QMouseEvent):
		if QMouseEvent.buttons() & 4:
			self.midDownDetected(QMouseEvent.pos().x(), QMouseEvent.pos().y())
		elif QMouseEvent.buttons() & 1:
			xy_model = self.xy_from_screen_to_model(QMouseEvent.pos().x(), QMouseEvent.pos().y())

			self._selected_object = self.scene.get_selected(xy_model[0], xy_model[1])
			self._left_down_x = xy_model[0]
			self._left_down_y = xy_model[1]

			self._left_up_x = None
			self._left_up_y = None

	def translate_selected_object(self, x, y):
		delta_x = x - self._left_down_x
		delta_y = y - self._left_down_y

		self._selected_object.translate(delta_x, delta_y)



	def mouseMoveEvent(self, QMouseEvent):
		if QMouseEvent.buttons() & 4:
			self.mouseMoveDetected(QMouseEvent.pos().x(), QMouseEvent.pos().y())
		elif QMouseEvent.buttons() & 1:
			xy_model = self.xy_from_screen_to_model(QMouseEvent.pos().x(), QMouseEvent.pos().y())

			if self._selected_object != None:
				self.translate_selected_object(xy_model[0], xy_model[1])
				self._left_down_x = xy_model[0]
				self._left_down_y = xy_model[1]
				self.refresh()


	def mouseReleaseEvent(self, QMouseEvent):
		if QMouseEvent.buttons() & 4:
			cursor =QtGui.QCursor()
			print cursor.pos()
		elif QMouseEvent.buttons() & 1:
			self._selected_object = None



	def wheelEvent(self, QWheelEvent):
		self.add_zoom(int(QWheelEvent.delta() / 120.0))


class Window(QWidget):
	def __init__(self, parent):
		# Inizializzo antenato
		QWidget.__init__(self, parent)

		# Creo widget che visualizza opengl
		glWidget = GLWidget(None)

		# Creo un layour orizzontale
		mainLayout = QHBoxLayout()

		# Aggiungo la widget per opengl al layout
		mainLayout.addWidget(glWidget)

		# Imposto il layout per questo (self) oggetto
		self.setLayout(mainLayout)

		self.setMinimumWidth(600)

		self.setMinimumHeight(400)

		self.mouse_down_x = None
		self.mouse_down_y = None

		self.glWidget = glWidget
	def keyPressEvent(self, QKeyEvent):
		if QKeyEvent.key() == Key_Control:
			# Intercetto la pressione del Ctrl, evitando di ri-processarlo
			# durante una pressione continua
			if not QKeyEvent.isAutoRepeat():
				print "Tab giu"
				self.glWidget.tabDownDetected()
		elif QKeyEvent.key() == Key_Tab:
			if not QKeyEvent.isAutoRepeat():
				self.glWidget.setHiddenVisibilitySwitch()
	def keyReleaseEvent(self, QKeyEvent):
		if QKeyEvent.key() == Key_Control:
			# Intercetto il rilascio del Tab, evitando di ri-processarlo
			# durante una pressione continua
			if not QKeyEvent.isAutoRepeat():
				print "Tab su"
				self.glWidget.tabUpDetected()
		elif QKeyEvent.key() == Key_Tab:
			if not QKeyEvent.isAutoRepeat():
				pass






app = QtGui.QApplication(sys.argv)
window = Window(None)
window.show()
sys.exit(app.exec_())
