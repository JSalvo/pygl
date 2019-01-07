import math

def near_to_zero(v):
	if abs(v) < 0.0000001:
		return True
	else:
		return False


class Vector:
	def __init__(self):
		self._vector = []

	# Sum between vectors
	def __add__(self, v2):
		vsize = len(self._vector)
		result = None

		if vsize == len(v2):
			result = self.get_empty_vector_same_type()
			for i in range(0, vsize):
				result[i] = self._vector[i] + v2[i]
		else:
			print "Dimensioni vettore incompatibili - NO SOMMA"

		return result

	# Subctraction between vectors
	def __sub__(self, v2):
		vsize = len(self._vector)
		result = None

		if vsize == len(v2):
			result = self.get_empty_vector_same_type()
			for i in range(0, vsize):
				result[i] = self._vector[i] - v2[i]
		else:
			print "Dimensioni vettore incompatibili - NO SOTTRAZIONE"

		return result

	# Dot product
	def dot(self, v2):
		vsize = len(self._vector)
		result = None

		if vsize == len(v2):
			result = 0
			for i in range(0, vsize):
				result += self._vector[i] * v2[i]
		else:
			print "Dimensioni vettore incompatibili - NO DOT PRODUCT"

		return result

	# Vector length
	def length(self):
		return math.sqrt(self.dot(self))

	# Vector normalized
	def normalize(self):
		return self / self.length()

	# Scalar per vector
	def __rmul__(self, v):
		vsize = len(self._vector)
		result = self.get_empty_vector_same_type()
		for i in range(0, vsize):
			result[i] = v * self._vector[i]

		return result

	# Vector div scalar
	def __div__(self, v):
		vsize = len(self._vector)
		result = self.get_empty_vector_same_type()
		for i in range(0, vsize):
			result[i] = (self._vector[i]*1.0) / v

		return result

	def __getitem__(self, i):
		return self._vector[i]

	def __setitem__(self, i, y):
		self._vector[i] = y


class Vector3d(Vector):
	def __init__(self, a, b, c):
		Vector.__init__(self)
		self._vector = [a,b,c]

	def get_empty_vector_same_type(self):
		return Vector3d(0, 0, 0)

	def __repr__(self):
		return str(self._vector)

	def __len__(self):
		return 3

	def toPoint3d(self):
		return Point3d(self[0], self[1], self[2])

class Vector2d(Vector):
	def __init__(self, a, b):
		Vector.__init__(self)
		self._vector = [a,b]

	def get_empty_vector_same_type(self):
		return Vector2d(0, 0)

	def __repr__(self):
		return str(self._vector)

	def __len__(self):
		return 2

	def toPoint2d(self):
		return Point2d(self[0], self[1])

	def getOrtho(self):
		return Vector2d(self[1], -self[0])

	def invert(self):
		return Vector2d(-self[0], -self[1])

	def __neg__(self):
		return Vector2d(-self[0], -self[1])


class Matrix:
	def __init__(self, rows, columns):
		self._rows = rows
		self._columns = columns
		self._build_matrix()

	def __repr__(self):
		return self._matrix.__repr__()

	def __index__(self, i):
		return self._matrix[i]

	def getMatrix(self):
		return self._matrix

	def _build_matrix(self):
		self._matrix = []
		for i in range(0, self._rows):
			self._matrix.append([0]*self._columns)


class LinearSystem(Matrix):
	def __init__(self, solutions):
		Matrix.__init__(self, solutions, solutions + 1)

	def pivot(self, r1, r2):
		for j in range(0, self._columns):
			tmp = self._matrix[r1][j]
			self._matrix[r1][j] = self._matrix[r2][j]
			self._matrix[r2][j] = tmp

	def reduce(self, r):
		print "Riduzione a partire dalla riga: %d"%r
		for i in range(r+1, self._rows):
			if near_to_zero(self._matrix[i][r]):
				continue
			else:
				k = (1.0 * self._matrix[r][r]) / self._matrix[i][r]

				for j in range(r, self._columns):
					self._matrix[i][j] = self._matrix[i][j] * k - self._matrix[r][j]

	def get_idx_row_to_pivot(self, r):
		for i in range(r+1, self._rows):
			if near_to_zero(self._matrix[i][r]):
				continue
			else:
				return i
		return None

	def get_solutions(self):
		solutions = [0]*self._rows

		for i in range(self._rows-1, -1, -1):
			solutions[i] += self._matrix[i][self._columns-1]

			for j in range(self._rows-1, i, -1):
				solutions[i] += -self._matrix[i][j]*solutions[j]

			solutions[i] /=  1.0*self._matrix[i][i]

		return solutions

	def solve(self):
		for i in range(0, self._rows-1):
			if near_to_zero(self._matrix[i][i]):
				print "Necessario Pivotare"
				k = self.get_idx_row_to_pivot(self, i)
				if k==None:
					return None
				else:
					self.pivot(i, k)
			self.reduce(i)

		return self.get_solutions()


class Point3d(Vector3d):
	def __init__(self, x, y, z):
		Vector3d.__init__(self, x, y, z)
	def __repr__(self):
		return "P(%f, %f, %f)"%(self[0], self[1], self[2])

class Point2d(Vector2d):
	def __init__(self, x, y):
		Vector2d.__init__(self, x, y)
	def __repr__(self):
		return "P(%f, %f)"%(self[0], self[1])
	def toPoint3d(self):
		return Point3d(self[0], self[1], 0)
	def clone(self):
		return Point2d(self[0], self[1])


class Segment:
	def __init__(self, pa, pb):
		self._pa = pa
		self._pb = pb
	def get_line(self):
		return Line2d( self._pa.clone(), self._pb - self._pa )
	def __repr__(self):
		return "%s -> %s"%(self._pa.__repr__(), self._pb.__repr__())


class Line2d:
	def __init__(self, p, v):
		self._p = p
		self._v = v

	def getVector(self):
		return self._v

	def getPoint2d(self):
		return self._p

	def getPointLine(self, t):
		return Point2d(self._p[0] + t*self._v[0], self._p[1] + t*self._v[1])

	def getIntersectionPoint(self, l):
		solutions = None
		result = (None, None, None)

		# Il prodotto scalare di due vettori normalizzati, "paralleli" è 1 o -1
		v = self.getVector().normalize().dotProduct( l.getVector().normalize() )

		# Se il valore assoluto del prodotto scalare, tra il vettore della linea
		# self e il vettore della linea l è 1, la linea self e la linea l, sono
		# parallele ...
		if near_to_zero(abs(v) - 1):
			# ... quindi, nessun punto di interesezione
			return (None, None, None)
		else:
			# ... altrimenti, risolvo il sistema lineare rappresentante le due
			# linee, andando ad ottenere le incognite dell'equazioni parametriche
			# rappresdentanti le due linee
			solutions = self._getLinearSystem(l).solve()

		if solutions != None:
			# p1 e p2, rispettivamente sulla linea self e su quella l, dovrebbero
			# essere coincidenti (in qunato il medesimo punto di interesezione
			# tra le due linee )
			p1 = self.getPointLine(solutions[0])
			p2 = l.getPointLine(solutions[1])

			result = (p1, solutions[0], solutions[1])

		return result

	def _getLinearSystem(self, l2):
		# t*v[0] - k*w[0] = pb.x - pa.x
		# t*v[1] - k*w[1] = pb.y - pa.y

		# Vettore di questa linea
		v = self.getVector()

		# Vettore della linea l2
		w = l2.getVector()

		# Punto di questa linea
		pa = self.getPoint2d()

		# Punt odella linea l2
		pb = l2.getPoint2d()

		# Ottengo la matrice per un sistema lineare a 2 incognite
		ls = LinearSystem(2)

		# "Compilo" i valori della matrice
		ls[0][0] = v[0]
		ls[0][1] = -w[0]
		ls[0][2] = pb[0] - pa[0]

		ls[1][0] = v[1]
		ls[1][1] = -w[1]
		ls[1][2] = pb[1] - pa[1]

		return ls



# px = pa.x + t*v[0]
# py = pa.y + t*v[1]

# px = pb.x + k*w[0]
# py = pb.y + k*w[1]

# t*v[0] - k*w[0] = pb.x - pa.x
# t*v[1] - k*w[1] = pb.y - pa.y

# a*t - b*w = c
# d*t - e*w = f




v = Vector3d(1,2,3)
print v
print v+v
print v-v
print 2*v
print v/2
print v.dot(v)

p = Point3d(4, 5, 6)
print p
print p + p
print p - p
print (p / 2).toPoint3d()
print ((p + p)/2).toPoint3d()

p1 = Point3d(1,2,3)
print p1
p2 = Point3d(4,5,6)
print p2

print (p2 - p1).length()


pa = Point2d(1,2)
pb = Point2d(4,5)

dirPaPb = (pb - pa).normalize()
dirOrthoPaPb = dirPaPb.getOrtho()

pbase_triang = pb - 1.5 * dirPaPb
p1 = (pbase_triang + 1.5 * dirOrthoPaPb).toPoint2d()
p2 = (pbase_triang - 1.5 * dirOrthoPaPb).toPoint2d()

print pb
print p1
print p2

d1 = (pb - p1).length()
d2 = (pb - p2).length()
d3 = (p1 - p2).length()

print d1, d2, d3
print ""

q = math.sqrt((1.5**2  - 0.75**2))

dirPaPb = (pb - pa).normalize()
dirOrthoPaPb = dirPaPb.getOrtho()

pbase_triang = pb - q * dirPaPb
p1 = (pbase_triang + 0.75 * dirOrthoPaPb).toPoint2d()
p2 = (pbase_triang - 0.75 * dirOrthoPaPb).toPoint2d()

print pb
print p1
print p2

d1 = (pb - p1).length()
d2 = (pb - p2).length()
d3 = (p1 - p2).length()

print d1, d2, d3


m = Matrix(3, 4)
print m

l1 = Line2d(Point2d(4,3), Vector2d(1,2))
l2 = Line2d(Point2d(-1,4), Vector2d(5,1))

print "Linea 1"
print l1.getPoint2d()
print l1.getVector()

print "Linea 2"
print l2.getPoint2d()
print l2.getVector()


print ""
ls = l1.getLinearSystem(l2)
soluzioni = ls.solve()


print ls
print soluzioni

print l1.getIntersectionPoint(l2)


pa = Point2d(8, 2)
pb = Point2d(2, 7)

segmento1 = Segment(pa, pb)
print segmento1
print segmento1.get_line()


pa = Point2d(1, 1)
pb = Point2d(4, 5)

segmento2 = Segment(pa, pb)
print segmento2
print segmento2.get_line()

print segmento1.get_line().getIntersectionPoint(segmento2.get_line())
