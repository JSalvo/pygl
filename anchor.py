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
from quadrilaterals import JCircle


Anchor_to_rectangle = 1

def near_to(a, b):
	if (abs(a - b) < 0.001):
		return True
	else:
		return False



class Anchor(JCircle):
	def __init__(self):
		JCircle.__init__(self, 20)
		self._Anchor_type = 0
		self._attached_to = None


	def get_selected(self, x, y):
		result = None

		if self.isSelected(x, y):
			result = self

		return result

	def anchor_to_rectangle(self, rectangle):
		self._attached_to = rectangle
		self._Anchor_type = Anchor_to_rectangle
		rlimits = rectangle.getLimits()
		self._tx = rlimits["left"]
		self._ty = rlimits["top"]
		rectangle.addAnchor(self)

	# Override
	def translate(self, tx, ty):
		if self._Anchor_type == Anchor_to_rectangle:
			rectangle = self._attached_to
			rlimits = rectangle.getLimits()

			new_tx = self._tx + tx
			new_ty = self._ty + ty

			if (near_to(self._tx, rlimits["left"]) and near_to(self._ty, rlimits["top"])):
				if new_ty > rlimits["top"]:
					new_ty = rlimits["top"]
				else:
					new_tx = rlimits["left"]
			elif (near_to(self._tx, rlimits["right"]) and near_to(self._ty, rlimits["top"])):
				if new_ty > rlimits["top"]:
					new_ty = rlimits["top"]
				else:
					new_tx = rlimits["right"]
			elif (near_to(self._tx, rlimits["right"]) and near_to(self._ty, rlimits["bottom"])):
				if new_ty < rlimits["bottom"]:
					new_ty = rlimits["bottom"]
				else:
					new_tx = rlimits["right"]
			elif (near_to(self._tx, rlimits["left"]) and near_to(self._ty, rlimits["bottom"])):
				if new_ty < rlimits["bottom"]:
					new_ty = rlimits["bottom"]
				else:
					new_tx = rlimits["left"]
			elif (near_to(self._tx, rlimits["left"])):
				new_tx = rlimits["left"]
				if new_ty > rlimits["top"]:
					new_ty = rlimits["top"]
				elif new_ty < rlimits["bottom"]:
					new_ty = rlimits["bottom"]
			elif (near_to(self._tx, rlimits["right"])):
				new_tx = rlimits["right"]
				if new_ty > rlimits["top"]:
					new_ty = rlimits["top"]
				elif new_ty < rlimits["bottom"]:
					new_ty = rlimits["bottom"]
			elif (near_to(self._ty, rlimits["top"])):
				new_ty = rlimits["top"]
				if new_tx < rlimits["left"]:
					new_tx = rlimits["left"]
				elif new_tx > rlimits["right"]:
					new_tx = rlimits["right"]
			elif (near_to(self._ty, rlimits["bottom"])):
				new_ty = rlimits["bottom"]
				if new_tx < rlimits["left"]:
					new_tx = rlimits["left"]
				elif new_tx > rlimits["right"]:
					new_tx = rlimits["right"]
			else:
				1 / 0


			self._tx = new_tx
			self._ty = new_ty

	def paint(self):
		JCircle.paint(self)
