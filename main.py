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
		self.__name = Text(name, 30, 60)

	def get_name(self):
		return self.__name.get_text()

	def set_name(self, newName):
		self.__name.set_text(newName)

	def paint(self):
		width = len(self.__name)*104.76 + 60
		height = 119.05 + 120

		glBegin(GL_LINE_LOOP)
		glVertex2f(0, 0)
		glVertex2f(width, 0)
		glVertex2f(width, height)
		glVertex2f(0, height)
		glEnd()

		self.__name.paint()


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

	def initializeGL(self):
		GLUT.glutInit([], [])

		black = QColor(0,0,0)

		# Imposto colore di cancellazione
		self.qglClearColor(black)

		glViewport(0, 0, self.width(), self.height())
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0, self.width(), 0.0, self.height(), -1.0, 1.0)

	def paintGL(self):

		glClear(GL_COLOR_BUFFER_BIT);
		glColor3f(1.0, 1.0, 0.0)

		"""
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)
		glEnable(GL_LINE_SMOOTH)
		glLineWidth(2.0)
		"""

		e = Entity("Cliente")
		e.paint()

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
		glOrtho(0.0, self.width(), 0.0, self.height(), -1.0, 1.0)


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
	def mousePressEvent(self, QMouseEvent):
		print QMouseEvent.pos()

	def mouseReleaseEvent(self, QMouseEvent):
		cursor =QtGui.QCursor()
		print cursor.pos()


app = QtGui.QApplication(sys.argv)
window = Window(None)
window.show()
sys.exit(app.exec_())
