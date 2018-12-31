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

Key_Tab = int("0x01000001", 16)


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


class Scene:
	def __init__(self):
		self.entities = []
	def add_entity(self, entity):
		self.entities.append(entity)
	def get_selected(self, x, y):
		selected = None
		for e in self.entities:
			selected = e.get_selected(x, y)
			if selected != None:
				break
		return selected
	def paint(self):
		for entity in self.entities:
			entity.paint()


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
		self.scene = Scene()
		self.scene.add_entity(self.e)

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

		# Imposto colore di cancellazione
		self.qglClearColor(black)

		glViewport(0, 0, self.width(), self.height())
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0 - self._pan_x * self._zoom_factor, self.width()*self._zoom_factor - self._pan_x * self._zoom_factor , 0.0 + self._pan_y * self._zoom_factor, self.height()*self._zoom_factor + self._pan_y * self._zoom_factor, -1.0, 1.0)

	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT);
		glColor3f(1.0, 1.0, 0.0)

		self.scene.paint()

		#paint_circle(30, 30, 20, 12)

		glFlush()

	def resizeGL(self, w, h):
		glViewport(0, 0, self.width(), self.height())
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0 - self._pan_x * self._zoom_factor, self.width()*self._zoom_factor - self._pan_x * self._zoom_factor, 0.0 + self._pan_y * self._zoom_factor, self.height()*self._zoom_factor + self._pan_y * self._zoom_factor, -1.0, 1.0)

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
		return ((x - self._pan_x)* self._zoom_factor, (y + self._pan_y) * self._zoom_factor)


	def mouseMoveDetected(self, x, y):
		if self._tab_down:
			if self._mid_down_x != None and self._mid_down_y != None:

				#print "Fai un pan"
				delta_x = x - self._mid_down_x
				delta_y = y - self._mid_down_y

				self.panXY(delta_x, delta_y)

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
		if QKeyEvent.key() & Key_Tab:
			# Intercetto la pressione del Tab, evitando di ri-processarlo
			# durante una pressione continua
			if not QKeyEvent.isAutoRepeat():
				print "Tab giu"
				self.glWidget.tabDownDetected()

	def keyReleaseEvent(self, QKeyEvent):
		if QKeyEvent.key() & Key_Tab:
			# Intercetto il rilascio del Tab, evitando di ri-processarlo
			# durante una pressione continua
			if not QKeyEvent.isAutoRepeat():
				print "Tab su"
				self.glWidget.tabUpDetected()






app = QtGui.QApplication(sys.argv)
window = Window(None)
window.show()
sys.exit(app.exec_())
