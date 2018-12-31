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


def paint_circle(x=0, y=0, radius=1, detail=12):
	delta = (2*math.pi) / detail

	glBegin(GL_LINE_LOOP)

	for i in range(0, detail):
		glVertex2f(x + math.cos(delta*i)*radius, y + math.sin(delta*i)*radius)

	glEnd()


class Text:
	# x e y sono la posizione relativa del testo
	def __init__(self, text=[], x=0, y=0):
		self.__text = text
		self.__x = x
		self.__y = y

	def set_position(self, x, y):
		self.__x = x
		self.__y = y

	def set_text(self, text):
		self.__text = text

	def get_text(self):
		return self.__text

	def paint(self):
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glTranslatef(self.__x, self.__y, 0)

		for i in range(0, len(self.__text)):
			GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_MONO_ROMAN, ord(self.__text[i]))

		glPopMatrix()

	def __len__(self):
		return len(self.__text)


class Entity:
	def __init__(self, name):
		self._name = Text(name, 30, 60)
		self._tx = 0
		self._ty = 0
		self._width = len(self._name)*104.76 + 60
		self._height = 119.05 + 120

	def get_name(self):
		return self._name.get_text()

	def set_name(self, newName):
		self._name.set_text(newName)
		self._width = len(self._name)*104.76 + 60
		self._height = 119.05 + 120

	def translate(self, tx, ty):
		self._tx += tx
		self._ty += ty

	def get_selected(self, x, y):
		if ((x >= self._tx) and (x <= self._tx + self._width) and (y >= self._ty) and (y <= self._ty + self._height)):
			return self
		else:
			return None

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def paint(self):
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glTranslatef(self._tx, self._ty, 0)
		glBegin(GL_LINE_LOOP)
		glVertex2f(0, 0)
		glVertex2f(self._width, 0)
		glVertex2f(self._width, self._height)
		glVertex2f(0, self._height)
		glEnd()

		self._name.paint()
		glPopMatrix()


class Attribute:
	def __init__(self, name, x=0, y=0):
		self.__label = Text(name, 20, 0)
		self.__x = x
		self.__y = y

	def get_name(self):
		return self.__label.get_text()

	def set_name(self, name):
		self.__label.set_text(name)

	#def paint(self):


class GLWidget(QGLWidget):

	def __init__(self, parent):
		# Inizializza Antenato
		QGLWidget.__init__(self, parent)
		self._zoom_factor = 1.0
		self._pan_x = 0
		self._pan_y = 0
		self.e = Entity("Cliente")

	def panY(self, pan_y):
		self._pan_y += pan_y

	def panX(self, pan_x):
		self._pan_x += pan_x

	def initializeGL(self):
		GLUT.glutInit([], [])

		black = QColor(0,0,0)

		# Imposto colore di cancellazione
		self.qglClearColor(black)

		glViewport(0, 0, self.width(), self.height())
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0 - self._pan_x * self._zoom_factor, self.width()*self._zoom_factor - self._pan_x * self._zoom_factor , 0.0 + self._pan_y * self._zoom_factor, self.height()*self._zoom_factor + self._pan_y * self._zoom_factor, -1.0, 1.0)

	def paintGL(self):

		glClear(GL_COLOR_BUFFER_BIT);
		glColor3f(1.0, 1.0, 0.0)

		"""
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)
		glEnable(GL_LINE_SMOOTH)
		glLineWidth(2.0)
		"""


		self.e.paint()

		#paint_circle(30, 30, 20, 12)

		"""
		a = Text("Ciao Bello")
		a.x = 100
		a.y = 100
		a.paint()
		"""

		"""
		glPushMatrix()
		for i in range(33, 50):
		GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_ROMAN, i)
		glPopMatrix()
		"""

		"""
		glBegin(GL_POLYGON)
		glVertex3f(25, 25, 0.0)
		glVertex3f(75, 25, 0.0)
		glVertex3f(75, 75, 0.0)
		glVertex3f(25, 75, 0.0)
		glEnd()

		glBegin(GL_LINES)
		glVertex3f(0.0, 0.0, 0.0)
		glVertex3f(self.width()-1, 0.0, 0.0)
		glVertex3f(self.width()-1, self.height()-1, 0.0)
		glVertex3f(0.0, self.height()-1, 0.0)
		glEnd()
		"""

		glFlush()

	def resizeGL(self, w, h):
		glViewport(0, 0, self.width(), self.height())
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0 - self._pan_x * self._zoom_factor, self.width()*self._zoom_factor - self._pan_x * self._zoom_factor, 0.0 + self._pan_y * self._zoom_factor, self.height()*self._zoom_factor + self._pan_y * self._zoom_factor, -1.0, 1.0)


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

	def mousePressEvent(self, QMouseEvent):
		if QMouseEvent.buttons() & 4:
			self.mouse_down_x = QMouseEvent.pos().x()
			self.mouse_down_y = QMouseEvent.pos().y()
		elif QMouseEvent.buttons() & 1:
			r = self.glWidget.e.get_selected(QMouseEvent.pos().x(), QMouseEvent.pos().y())
			if r != None:
				print "Noooo! x: %d, y: %d"%(QMouseEvent.pos().x(), QMouseEvent.pos().y())
			else:
				print "Yeppa!"

	def mouseMoveEvent(self, QMouseEvent):
		if QMouseEvent.buttons() & 4:
			delta_x = QMouseEvent.pos().x() - self.mouse_down_x
			delta_y = QMouseEvent.pos().y() - self.mouse_down_y
			print "Delta X: %d, Delta Y: %d"%(delta_x, delta_y)
			self.glWidget.panX(delta_x)
			self.glWidget.panY(delta_y)

			self.mouse_down_x = QMouseEvent.pos().x()
			self.mouse_down_y = QMouseEvent.pos().y()

			self.glWidget.initializeGL()

			self.glWidget.updateGL()
	def mouseReleaseEvent(self, QMouseEvent):
		if QMouseEvent.buttons() & 4:
			cursor =QtGui.QCursor()
			print cursor.pos()


app = QtGui.QApplication(sys.argv)
window = Window(None)
window.show()
sys.exit(app.exec_())
