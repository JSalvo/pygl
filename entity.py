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

class Entity(JRectangle):
	def __init__(self, name):
		JRectangle.__init__(self)
		self._name = Text(name, 30, 60)

		self.setWidth( len(self._name)*104.76 + 60 )
		self.setHeight( 119.05 + 120 )
		self._attributes = []
		self._links = []

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

		result = None
		if self._visible or True:
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

	def addLink(self, link):
		self._links.append(link)

	def paint(self, paintHidden=False):
		#self.setOpenGlColor()
		if self.getVisibility() or paintHidden:
			JRectangle.paint(self, paintHidden)

			glMatrixMode(GL_MODELVIEW)

			glPushMatrix()
			# La posizine dell'entita' viene resa, attraverso una traslazione
			# relativamente alla sua origine*
			glTranslatef(self._tx, self._ty, 0)
			self._name.paint(paintHidden)

			glBegin(GL_LINES)
			for link in self._links:
				link.getAnchorGlPoint()
				print "a"
				link.getAttributeGlPoint()
				print "a"
			glEnd()

			for attribute in self._attributes:
				attribute.paint(paintHidden)

			for anchor in self._anchors:
				anchor.paint(paintHidden)


			glPopMatrix()

# * "L'origine dell'entita' e' l'angolo basso sinistro del rettangolo che la rappresenta "
