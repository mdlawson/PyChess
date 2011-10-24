from itertools import izip_longest

class Rook:
	def isLegal(self, move):
		if move[0] == 0 or move[1] == 0:
			return 0
		else:
			return 1
	def moves(self, pos):
		return mappingLoop(pos, self)
class Bishop:
	def isLegal(self, move):
		if abs(move[0])==abs(move[1]):
			return 0
		else:
			return 1
	def moves(self, pos):
		return mappingLoop(pos, self)
class Knight:
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,2] or move == [2,1]:
			return 0
		else:
			return 1
	def moves(self, pos):
		return mappingLoop(pos, self)
class King:
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,0] or move == [0,1] or move == [1,1]:
			return 0
		else:
			return 1
	def moves(self, pos):
		return mappingLoop(pos, self)
class Queen:
	def isLegal(self, move):
		if Bishop.isLegal(self, move) or Rook.isLegal(self, move):
			return 0
		else:
			return 1
	def moves(self, pos):
		return mappingLoop(pos, self)

def mappingLoop(pos, piece):
	valid = []
	for x in range(8):
		for y in range(8):
			print "Mapping [",x,",",y,"]...", 
			if piece.isLegal([(y-pos[0]),(x-pos[1])]) == 0:
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
	

board = [									# This is the original board
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],	# I changed bishops and knights the right way round
["  ","  ","  ","  ","  ","  ","  ","  "],	# N = Knights, as in normal chess notation, "N"
["  ","  ","hh","1r","  ","2p","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "]
]
WR1 = Rook()
#mappingLoop([3,4],WR1)
checkingLoop([3,3],[-3,0],board)