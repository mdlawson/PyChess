from itertools import izip_longest
import sys

class Rook: # This is a class for a piece
	def __init__(self, pos, team): # when a new object of this class is made, its position needs to be supplied
		self.pos = pos
		self.team = team #pieces position is saved as Piece.pos
		self.status = 0
	def isLegal(self, move): # Piece.isLegal checks if a move is legal for th currect piece. takes 1 arg, as self is always supplied
		if move[0] == 0 or move[1] == 0:
			if checkingLoop(self, move) == 0:
				return 0
			else:
				return 1
		else:
			return 1
	def moves(self): # Piece.moves() returns an array of valid moves for the piece
		return mappingLoop(self)
	def sayHi(self): # Useless function for testing
		print "Hi, I'm a rook! I'm located at:",self.pos,".Im on",teams[self.team]
class Bishop:
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
		self.status = 0
	def isLegal(self, move):
		if abs(move[0])==abs(move[1]):
			if checkingLoop(self, move) == 0:
				return 0
			else:
				return 1
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm a Bishop! I'm located at:",self.pos,".Im on",teams[self.team]
class Knight:
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
		self.status = 0
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,2] or move == [2,1]:
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm a Knight! I'm located at:",self.pos,".Im on",teams[self.team]
class King:
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
		self.status = 0
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,0] or move == [0,1] or move == [1,1]:
			return 0
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm the King! I'm located at:",self.pos,".Im on",teams[self.team]
class Queen:
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
		self.status = 0
	def isLegal(self, move):
		if abs(move[0])==abs(move[1]) or move[0] == 0 or move[1] == 0:
			if checkingLoop(self, move) == 0:
				return 0
			else:
				return 1
		else:
			return 1
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm the queen! I'm located at:",self.pos,".Im on",teams[self.team]
# note the absance of a pawn class. still thinking how to implement pawns in a class, as their legal checking requires much more arguments than everybody elses.
class Pawn:
	def __init__(self, pos, team):
		self.pos = pos
		self.team = team
		self.status = 0
	def isLegal(self, move):
		if self.team == 1 and move[1] < 0:		#Pawn can't go backwards
			return 1
		if self.team == 2 and move[1] > 0:		#Pawn can't go backwards
			return 1
		if abs(move[1]) > 2:					#Pawn can't move more than 2 squares in y-direction in any circumstances
			return 1
		if abs(move[0]) > 1:					#Pawn can't move more than 1 square in x-direction under any circumstances
			return 1
		if abs(move[1]) != 1 and self.pos[1] != 1 and self.pos[1] != 6: #Pawn can only move two when haven't moved
			return 1
		if abs(move[0]) == 1 and abs(move[1]) != 1:
			return 1
		if abs(move[0]) == 1 and board[self.pos[0]+move[0]][self.pos[1]+move[1]] == "   ":
			return 1
		if abs(move[0]) == 0 and board[self.pos[0]+move[0]][self.pos[1]+move[1]] != "   ":
			return 1
		else:
			return 0
	def moves(self):
		return mappingLoop(self)
	def sayHi(self):
		print "Hi, I'm a pawn! I'm located at:",self.pos,".Im on",teams[self.team]
	

def mappingLoop(piece): #produces an array of valid moves for any given piece, quite neat. However, random bug, seems to think the piece is in the wrong place vertically
	valid = []
	for x in range(8):
		for y in range(8):
			print "Mapping [",x,",",y,"]...",
			if piece.isLegal([(x-piece.pos[0]),(y-piece.pos[1])]) == 0:
				print "Valid!"
				valid.append([x,y])
			else:
				print "Invalid!"
	return valid

def checkingLoop(piece, move): # generic collision detection function, should work for any piece. prints the right output for squares to check, but doesnt check them yet. dont know why. random bugs :L
	if move[0] < 0:
		yRange = range(-1, move[1]-1, -1)
	else:
		yRange = range(1, move[1]+1, 1)
	if move[1] < 0:
		xRange = range(-1, move[0]-1, -1)
	else:
		xRange = range(1, move[0]+1, 1)
	for x,y in izip_longest(xRange,yRange, fillvalue=0):
		#print y, ",", x
		if board[piece.pos[0]+x][piece.pos[1]+y] != "   ":
			#print "there is a piece in the way!"
			return 1
	return 0

def checkLegal(piece, move):
	if pieceDict[board[posTo[0]][posTo[1]]].team == piece.team:
		return 1
	elif piece.isLegal(move) != 0:
		return 1
	else:
		return 0

def movePiece(piece, posTo):
	if board[posTo[0]][posTo[1]] != "   ":
		pieceDict[board[posTo[0]][posTo[1]]].status = 1
	board[posTo[0]][posTo[1]] = board[piece.pos[0]][piece.pos[1]]
	board[piece.pos[0]][piece.pos[1]] = "   "
	piece.pos[0],piece.pos[1] = posTo[0],posTo[1]
def printBoard(board):	# Prints board obviously, colored comes from library
	i = True
	for j in range(len(board)):
		for k in range(len(board[j])):
			if i==True: 
				sys.stdout.write('\033[47m\033[30m '+board[k][j]+' \033[0m')
				i=not i
			else:
				sys.stdout.write(" "+board[k][j]+" ")
				i=not i
		print ""
		i=not i


pieces = {'R':Rook,'N':Knight,'B':Bishop,'Q':Queen,'K':King, 'p':Pawn} # A dictionary for translating piece short codes to piece classes	
pieceDict = {}
teams = {1:'White',2:'Black'}
board = [									# This is a testing board
["1R1","1p1","   ","   ","   ","   ","2p1","2R1"],
["1N1","1p2","   ","   ","   ","   ","2p2","2N1"],
["1B1","1p3","   ","   ","   ","   ","2p3","2B1"],	
["1Q1","1p4","   ","   ","   ","   ","2p4","2Q1"],	
["1K1","1p5","   ","   ","   ","   ","2p5","2K1"],	
["1B2","1p6","   ","   ","   ","   ","2p6","2B2"],	
["1N2","1p7","   ","   ","   ","   ","2p7","2N2"],
["1R2","1p8","   ","   ","   ","   ","2p8","2R2"]
]
def setupPieces(board): # this is an init type function, sets up all the pieces on the board by calling them shortcode given on the board. problems with multiple pieces on same team needing uniques. 
	for x in range(len(board)):
		for y in range(len(board[x])):
			if board[x][y] != "   ":
				print "Found piece",board[x][y],", creating new",pieces[board[x][y][-2]]
				pieceDict[board[x][y]] = (pieces[board[x][y][-2]])([x, y],int(board[x][y][0]))
				pieceDict[board[x][y]].sayHi()
#mappingLoop("1R1") # various testing stubs :P 
#checkingLoop([3,3],[-3,0],board)
setupPieces(board)
#pieceDict["1p1"].moves()
printBoard(board)
movePiece(pieceDict["1p1"],[4,4])
printBoard(board)
pieceDict["1p1"].sayHi()