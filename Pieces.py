from itertools import izip_longest

class Rook: # This is a class for a piece
	def __init__(self, pos, team): # when a new object of this class is made, its position needs to be supplied
		self.pos = pos #pieces position is saved as Piece.pos
		self.team = team 
	def isLegal(self, move): # Piece.isLegal checks if a move is legal for th currect piece. takes 1 arg, as self is always supplied
		if move[0] == 0 or move[1] == 0:
			return 0
		else:
			return 1
	def moves(self): # Piece.moves() returns an array of valid moves for the piece
		return mappingLoop(self)
	def sayHi(self): # Useless function for testing
		print "Hi, I'm a rook! I'm located at:",self.pos
class Bishop:
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
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
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
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
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
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
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
	def isLegal(self, move):
		if Bishop.isLegal(self, move) or Rook.isLegal(self, move):
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm the queen! I'm located at:",self.pos
# note the absance of a pawn class. still thinking how to implement pawns in a class, as their legal checking requires much more arguments than everybody elses.

def mappingLoop(piece): #produces an array of valid moves for any given piece, quite neat. However, random bug, seems to think the piece is in the wrong place vertically
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

def checkingLoop(posFrom, move, board): # generic collision detection function, should work for any piece. prints the right output for squares to check, but doesnt check them yet. dont know why. random bugs :L
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
def checkLegal(piece, move):
	if piece.isLegal(move) != 0:
		return 1
	
pieces = {'R':Rook,'N':Knight,'B':Bishop,'Q':Queen,'K':King} # A dictionary for translating piece short codes to piece classes
piece = {}
teams = {'White':1,'Black':2}

board = [									# This is a testing board
["2R1","2N1","2B1","2Q1","2K1","2B2","2N2","2R2"],
["2p1","2p2","2p3","2p4","2p5","2p6","2p7","2p8"],
["   ","   ","   ","   ","   ","   ","   ","   "],	
["   ","   ","   ","   ","   ","   ","   ","   "],
["   ","   ","   ","   ","   ","   ","   ","   "],
["   ","   ","   ","   ","   ","   ","   ","   "],
["1p1","1p2","1p3","1p4","1p5","1p6","1p7","1p8"],
["1R1","1N1","1B1","1Q1","1K1","1B2","1N2","1R2"]
]
def setupPieces(board): # this is an init type function, sets up all the pieces on the board by calling them shortcode given on the board. problems with multiple pieces on same team needing uniques. 
	for y in range(len(board)):
		for x in range(len(board[y])):
			if board[y][x] != "   " and board[y][x][1] != "p":
				print "Found piece",board[y][x],", creating new",pieces[board[y][x][-2]]
				piece[board[y][x]] = (pieces[board[y][x][-2]])([y, x],board[y][x][0])
				piece[board[y][x]].sayHi()
				print board[y][x]
#	print(board)
	piece["1R2"]
#mappingLoop() # various testing stubs :P 
#checkingLoop([3,3],[-3,0],board)
setupPieces(board)