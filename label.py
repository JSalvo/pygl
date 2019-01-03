import sys
import PyQt4
from PyQt4 import QtGui, QtOpenGL
from PyQt4.QtGui import QWidget, QHBoxLayout, QColor
from PyQt4.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL import GLUT
import math
from PyQt4 import Qt

#from text import Text
from quadrilaterals import JRectangle, Text

class Label(JRectangle):
	def __init__(self, text):
		JRectangle.__init__(self)
		self._text = Text(text, 0, 10)

		self.setWidth( len(self._text)*104.76)
		self.setHeight( 119.05 + 20 )
		self.set_drawable(False)

	def get_text(self):
		return self._text.get_text()

	# Imposto il nome dell'entita'
	def set_text(self, newText):
		self._text.set_text(newText)

		# Larghezza e altezza del rettangolo rappresentate l'entita', dipendono
		# dal nome dell'entita' stessa
		self.setWidth( len(self._name)*104.76 )
		self.setHeight( 119.05 + 20 )

	def get_selected(self, x, y):
		# Se il punto x, y e' contenuto nel rettangolo che descrive l'entita',
		# produce questo oggetto, altrimenti ...

		result = None

		if self._visible or True:
			if result != None:
				return result
			elif self.isSelected(x, y):
				return self

		return result


	def paint(self, paintHidden=False):
		#self.setOpenGlColor()
		if self.getVisibility() or paintHidden:
			JRectangle.paint(self)

			glMatrixMode(GL_MODELVIEW)

			glPushMatrix()
			# La posizine dell'entita' viene resa, attraverso una traslazione
			# relativamente alla sua origine*
			glTranslatef(self._tx, self._ty, 0)
			self._text.paint()
			glPopMatrix()

# * "L'origine dell'entita' e' l'angolo basso sinistro del rettangolo che la rappresenta "
