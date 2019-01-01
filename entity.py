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
from quadrilaterals import JRectangle

class Entity(JRectangle):
	def __init__(self, name):
		JRectangle.__init__(self)
		self._name = Text(name, 30, 60)

		self.setWidth( len(self._name)*104.76 + 60 )
		self.setHeight( 119.05 + 120 )
		self._attributes = []

	def get_name(self):
		return self._name.get_text()

	# Imposto il nome dell'entita'
	def set_name(self, newName):
		self._name.set_text(newName)

		# Larghezza e altezza del rettangolo rappresentate l'entita', dipendono
		# dal nome dell'entita' stessa
		self.setWidth( len(self._name)*104.76 + 60 )
		self.setHeight( 119.05 + 120 )

	def get_selected(self, x, y):


		result = JRectangle.get_selected(self, x, y)

		if result != None:
			return result

		for attribute in self._attributes:
			result = attribute.get_selected(x - self._tx, y - self._ty)
			if result != None:
				break

		if result != None:
			return result
		elif self.isSelected(x, y):
			return self

		return result


	def add_attribute(self, attribute):
		self._attributes.append(attribute)

	def paint(self):
		JRectangle.paint(self)

		glMatrixMode(GL_MODELVIEW)

		glPushMatrix()
		# La posizine dell'entita' viene resa, attraverso una traslazione
		# relativamente alla sua origine*
		glTranslatef(self._tx, self._ty, 0)
		self._name.paint()
		for attribute in self._attributes:
			attribute.paint()

		for anchor in self._anchors:
			anchor.paint()
		glPopMatrix()

# * "L'origine dell'entita' e' l'angolo basso sinistro del rettangolo che la rappresenta "
