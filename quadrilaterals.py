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

def near_to_zero(v):
	if abs(v) < 0.0001:
		return True
	else:
		return False


def paint_circle(x=0, y=0, radius=1, detail=12):
	delta = (2*math.pi) / detail

	"""
	glBegin(GL_TRIANGLES)

	for i in range(0, detail):
		glVertex2f(x + math.cos(delta*i)*radius, y + math.sin(delta*i)*radius)

	glEnd()
	"""

	glBegin(GL_LINE_LOOP)

	for i in range(0, detail):
		glVertex2f(x + math.cos(delta*i)*radius, y + math.sin(delta*i)*radius)

	glEnd()

class JObject:
	def __init__(self, visible=True):
		self._visible = visible
		self._color = QColor(255,255,255)
		self._background_color = QColor(0, 0, 0)
	def setVisibility(self, v):
		self._visible = v
	def getVisibility(self):
		return self._visible
	def setColor(self, color):
		self._color = color
	def getColor(self, color):
		return self._color
	def setOpenGlColor(self):
		glColor3f(self._color.red()/255.0, self._color.green()/255.0, self._color.blue()/255.0)
	def setGlBackGroundColor(self):
		glColor3f(self._background_color.red()/255.0, self._background_color.green()/255.0, self._background_color.blue()/255.0)
	def setGlColor(self):
		glColor3f(self._color.red()/255.0, self._color.green()/255.0, self._color.blue()/255.0)


class Link:
	def __init__(self, anchor, attribute):
		self._anchor = anchor
		self._attribute = attribute
	def getAnchor(self):
		return self._anchor
	def getAttribute(self):
		return self._attribute
	def getAnchorGlPoint(self):
		center = self._anchor.getCenter()
		glVertex2f(center.getX(), center.getY())
	def getAttributeGlPoint(self):
		center = self._attribute.getCenter()
		glVertex2f(center.getX(), center.getY())


class Text(JObject):
	# x e y sono la posizione relativa del testo
	def __init__(self, text=[], x=0, y=0):
		JObject.__init__(self)
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

	def paint(self, paintHidden=False):
		if self.getVisibility() or paintHidden:
			glMatrixMode(GL_MODELVIEW)
			glPushMatrix()
			glTranslatef(self.__x, self.__y, 0)

			for i in range(0, len(self.__text)):
				GLUT.glutStrokeCharacter(GLUT.GLUT_STROKE_MONO_ROMAN, ord(self.__text[i]))

			glPopMatrix()

	def __len__(self):
		return len(self.__text)

class JPoint2d(JObject):
	def __init__(self, x, y):
		JObject.__init__(self, False)
		self._x = x
		self._y = y
	def getX(self):
		return self._x
	def getY(self):
		return self._y
	def setX(self, x):
		self._x = x
	def setY(self, y):
		self._y = y
	def dot(self, p2):
		return self.getX() * p2.getX() + self.getY() * p2.getY()
	def normalize(self):
		v = math.sqrt(self.dot(self))
		if near_to_zero(v):
			return JPoint2d(0, 0)
		else:
			return self / v
	def invert(self):
		return JPoint2d(-self.getX(), -self.getY())
	def distance(self, p2):
		v = p2 - self
		return math.sqrt( v.dot(v) )
	def __sub__(self, p2):
		return JPoint2d(self.getX() - p2.getX(), self.getY() - p2.getY())
	def __add__(self, p2):
		return JPoint2d(p2.getX() + self.getX(), p2.getY() + self.getY())
	def __div__(self, v):
		return JPoint2d(self.getX() / v, self.getY() / v)
	def __mul__(self, v):
		return JPoint2d(self.getX() * v, self.getY() * v)

class JRhombus(JObject):
	def __init__(self, major_diagonal, minor_diagonal):
		JObject.__init__(self)
		self._major_diagonal = major_diagonal
		self._minor_diagonal = minor_diagonal
		self._anchors = []
		self._tx = 0
		self._ty = 0

	def getMajorDiagonal(self):
		return self._major_diagonal

	def getMinorDiagonal(self):
		return self._minor_diagonal

	def setMajorDiagonal(self, major_diagonal):
		self._major_diagonal = major_diagonal

	def setMinorDiagonal(self, minor_diagonal):
		self._minor_diagonal = minor_diagonal

	def translate(self, tx, ty, lock_control_points=False):
		# Traslo l'entita' rispetto alla sua origine *
		self._tx += tx
		self._ty += ty
	def isSelected(self, x, y):
		pass



class JRectangle(JObject):
	def __init__(self, width=0, height=0):
		JObject.__init__(self)
		self._tx = 0
		self._ty = 0
		self._width = width
		self._height = height
		self._drawable = True
		self._anchors = []



	def getLimits(self):
		result = {}
		result["left"] = 0
		result["right"] = self._width
		result["bottom"] = 0
		result["top"] = self._height
		return result

	def get_selected(self, x, y):
		result = None
		if self._visible or True:
			for anchor in self._anchors:
				 result = anchor.get_selected(x-self._tx, y-self._ty)
				 if result != None:
					 break
		return result


	def addAnchor(self, a):
		self._anchors.append(a)

	def set_drawable(self, drawable):
		self._drawable = drawable

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def setWidth(self, width):
		self._width = width

	def setHeight(self, height):
		self._height = height

	def paint(self, paintHidden=True):
		self.setOpenGlColor()
		if self.getVisibility() or paintHidden:
			if self._drawable:
				glMatrixMode(GL_MODELVIEW)

				glPushMatrix()
				# La posizine del rettancolo viene resa, attraverso una traslazione
				# relativamente alla sua origine*
				glTranslatef(self._tx, self._ty, 0)
				# Disegno il rettangolo

				self.setGlBackGroundColor()
				glBegin(GL_QUADS)
				glVertex2f(0, 0)
				glVertex2f(self._width, 0)
				glVertex2f(self._width, self._height)
				glVertex2f(0, self._height)
				glEnd()



				self.setGlColor()
				glBegin(GL_LINE_LOOP)
				glVertex2f(0, 0)
				glVertex2f(self._width, 0)
				glVertex2f(self._width, self._height)
				glVertex2f(0, self._height)
				glEnd()

				glPopMatrix()

	def translate(self, tx, ty, lock_control=False):
		# Traslo l'entita' rispetto alla sua origine *
		self._tx += tx
		self._ty += ty

	def isSelected(self, x, y):
		# Se il punto x, y e' contenuto nel rettangolo
		# produce questo oggetto, altrimenti ...
		if ((x >= self._tx) and (x <= self._tx + self._width) and (y >= self._ty) and (y <= self._ty + self._height)):
			return True
		else:
			return False

# * "L'origine e' l'angolo basso sinistro del rettangolo "


class JCircle(JObject):
	def __init__(self,radius=1):
		JObject.__init__(self)
		self._radius = radius
		self._tx = 0
		self._ty = 0
		self._detail = 80
		self._drawable = True

	def set_drawable(self, drawable):
		self._drawable = drawable

	def getRadius(self):
		return self._radius

	def setRadius(self, r):
		self._radius = r

	def getCenter(self):
		return JPoint2d(self._tx, self._ty)

	def translate(self, tx, ty, lock_control=False):
		# Traslo l'entita' rispetto alla sua origine *
		self._tx += tx
		self._ty += ty

	def paint(self, paintHidden=False):
		#self.setOpenGlColor()
		if self.getVisibility() or paintHidden:
			if self._drawable:
				glMatrixMode(GL_MODELVIEW)

				glPushMatrix()
				glTranslatef(self._tx, self._ty, 0)
				# Disegno il cerchio con
				delta = (2*math.pi) / self._detail

				self.setGlBackGroundColor()
				glBegin(GL_TRIANGLES)
				for i in range(0, self._detail):
					glVertex2f(math.cos(delta*i)*self._radius, math.sin(delta*i)*self._radius)
					glVertex2f(math.cos(delta*(i+1))*self._radius, math.sin(delta*(i+1))*self._radius)
					glVertex2f(0, 0)
				glEnd()

				self.setGlColor()
				glBegin(GL_LINE_LOOP)
				for i in range(0, self._detail):
					glVertex2f(math.cos(delta*i)*self._radius, math.sin(delta*i)*self._radius)
				glEnd()

				glPopMatrix()

	def isSelected(self, x, y):
		# x**2 + y**2
		if self._visible or True:
			if math.sqrt((x - self._tx)**2 + (y-self._ty)**2) <= self._radius:
				return True

		return False
