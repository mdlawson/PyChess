from itertools import izip_longest

class Rook:
	def __init__(self, pos):
		self.pos = pos
	def isLegal(self, move):
		if move[0] == 0 or move[1] == 0:
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm a rook! I'm located at:",self.pos
class Bishop:
	def __init__(self, pos):
		self.pos = pos
	def isLegal(self, move):
		if abs(move[0])==abs(move[1]):
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm a Bishop! I'm located at:",self.pos
class Knight:
	def __init__(self, pos):
		self.pos = pos
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,2] or move == [2,1]:
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm a Knight! I'm located at:",self.pos
class King:
	def __init__(self, pos):
		self.pos = pos
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,0] or move == [0,1] or move == [1,1]:
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm the King! I'm located at:",self.pos
class Queen:
	def __init__(self, pos):
		self.pos = pos
	def isLegal(self, move):
		if Bishop.isLegal(self, move) or Rook.isLegal(self, move):
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm the queen! I'm located at:",self.pos

def mappingLoop(piece):
	valid = []
	for x in range(8):
		for y in range(8):
			print "Mapping [",x,",",y,"]...", 
			if piece.isLegal([(y-piece.pos[0]),(x-piece.pos[1])]) == 0:
				print "Valid!"
				valid.append([y,x])
			else:
				print "Invalid!"
	return valid

def checkingLoop(posFrom, move, board):
	if move[0] < 0:
		yRange = range(-1, move[0]-1, -1)
	else:
		yRange = range(1, move[0]+1, 1)
	if move[1] < 0:
		xRange = range(-1, move[1]-1, -1)
	else:
		xRange = range(1, move[1]+1, 1)
	for y,x in izip_longest(yRange,xRange, fillvalue=0):
		print y, ",", x
		if board[posFrom[0]+y][posFrom[1]+x] != "  ":
			print "there is a piece in the way!"

pieces = {'r':Rook,'n':Knight,'b':Bishop,'Q':Queen,'K':King}	

board = [									# This is the original board
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],	# I changed bishops and knights the right way round
["  ","  ","  ","  ","  ","  ","  ","  "],	# N = Knights, as in normal chess notation, "N"
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["1r","1n","1b","1Q","1K","  ","  ","  "]
]
def setupPieces(board):
	for y in range(len(board)):
		for x in range(len(board[y])):
			if board[y][x] != "  ":
				print "Found piece",board[y][x],", creating new",pieces[board[y][x][-1]]
				board[y][x] = (pieces[board[y][x][-1]])([y, x])
				board[y][x].sayHi()
#WR1 = Rook()
#mappingLoop([3,4],WR1)
#checkingLoop([3,3],[-3,0],board)
setupPieces(board)