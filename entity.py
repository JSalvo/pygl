import sys
import PyQt4
from PyQt4 import QtGui, QtOpenGL
from PyQt4.QtGui import QWidget, QHBoxLayout, QColor
from PyQt4.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL import GLUT
import math
from PyQt4 import Qt

from text import Text

class Entity:
	def __init__(self, name):
		self._name = Text(name, 30, 60)
		self._tx = 0
		self._ty = 0
		self._width = len(self._name)*104.76 + 60
		self._height = 119.05 + 120

	def get_name(self):
		return self._name.get_text()

	# Imposto il nome dell'entita'
	def set_name(self, newName):
		self._name.set_text(newName)

		# Larghezza e altezza del rettangolo rappresentate l'entita', dipendono
		# dal nome dell'entita' stessa
		self._width = len(self._name)*104.76 + 60
		self._height = 119.05 + 120

	def translate(self, tx, ty):
		# Traslo l'entita' rispetto alla sua origine *
		self._tx += tx
		self._ty += ty

	def get_selected(self, x, y):
		# Se il punto x, y e' contenuto nel rettangolo che descrive l'entita',
		# produce questo oggetto, altrimenti ...
		if ((x >= self._tx) and (x <= self._tx + self._width) and (y >= self._ty) and (y <= self._ty + self._height)):
			print "Offlalai!"
			return self
		else:
			# ... ciclo su tutti gli oggetti figli in cerca di un oggetto che
			# contenga (e quindi sia "selected") il punto x, y
			# DA IMPLEMENTARE
			return None

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def paint(self):
		glMatrixMode(GL_MODELVIEW)

		glPushMatrix()
		# La posizine dell'entita' viene resa, attraverso una traslazione
		# relativamente alla sua origine*
		glTranslatef(self._tx, self._ty, 0)

		glBegin(GL_LINE_LOOP)
		glVertex2f(0, 0)
		glVertex2f(self._width, 0)
		glVertex2f(self._width, self._height)
		glVertex2f(0, self._height)
		glEnd()

		self._name.paint()
		glPopMatrix()

# * "L'origine dell'entita' e' l'angolo basso sinistro del rettangolo che la rappresenta "
