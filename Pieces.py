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

def containsAny(str, set):
	return 1 in [c in str for c in set]

def takingOwnPiece(player,posTo):
	if player in board[posTo[1]][posTo[0]]:
		print "You can't take your own pieces!"
		return 1

def howMany(str):
	if str == "p":
		return 8
	if str in "RNB":
		return 2
	if str in "QK":
		return 1

def findPiece(pieceType,posTo):
		count = 0
		i = 1
		while i <= howMany(pieceType[1]):
			if checkLegal(pieceDict[pieceType+`i`],posTo) == 0:
				count = count + 1
				piece = pieceType+`i`
			i=i+1
		if count == 0:
			return "Piece can't move there"
		if count != 1:
			return "More than one piece can move there"


def decodeNotation(player,str):
	if (len(str) == 2) and (containsAny(str[:1],"abcdefgh")) and (containsAny(str[1:],"12345678")):
		mtype = "normal"
		pieceType = player+"p"
		posTo = chessToCoord(str)
	elif (len(str) == 3) and (containsAny(str[0],"KQRBNp") == 1) and (containsAny(str[1],"abcdefgh") == 1) and (containsAny(str[2],"12345678") == 1):
		mtype = "normal"
		pieceType = player+str[0]
		posTo = chessToCoord(str[1:])
#	elif str == "0-0":
#		err,toCoord,fromCoord = checkCastling("kingside",player)
#		if err == 0:
#			return 0
#		else:
#			print err
#			print "Can't castle"
#			return 1,1
#	elif str == "0-0-0":
#		err,toCoord,fromCoord = checkCastling("queenside",player)
#		if err == 0:
#			return toCoord,fromCoord
#		else:
#			print err
#			print "Can't castle"
#			return 1,1
	elif (len(str) == 4) and (containsAny(str[0],"abcdefgh") == 1) and (containsAny(str[1],"12345678") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		pieceType = "unknown"
		mtype = "coord"
		posTo = chessToCoord(str[2:])
		posFrom = chessToCoord(str[:2])
		piece = board[posFrom[0]][posFrom[1]]
	elif (len(str) == 4) and (containsAny(str[0],"KQRBNp") == 1) and (containsAny(str[1],"x") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "normaltake"
		pieceType = player+str[0]
		posTo = chessToCoord(str[2:])
#	elif (len(str) == 4) and (containsAny(str[1:],"+") == 0):
#		mtype = "check"

#	elif (len(str) == 5):
	
	else: # This could be refactored
		return "Unknown Notation"

	if mtype[:6] == "normal":
		if (mtype[6:] == "take") and (board[posTo[0]][posTo[1]] == "   "):
			print "You aren't taking anything"
		result = findPiece(pieceType,posTo)
		if result != 0:
			return result
	if checkLegal(pieceDict[piece],posTo) == 0:
		movePiece(pieceDict[piece].pos,posTo)
		return 0
	else:
		return "Move not Legal"
def chessToCoord(str):
	coord = [0,0]
	char = str[:1]
	coord[0] = ord(char)-97
	num = str[1:]
	coord[1] = int(num)-1
	return coord

#def workOutPosFrom(player,piece,toCoord,mtype,str):
#	if mtype[:6] == "normal":
#		if (mtype[6:] == "take") and (board[toCoord[1]][toCoord[0]] == "   "):
#			print "You aren't taking anything"
#		coords = checkWhere(player,piece)
#		count = 0
#		for fromCoord in coords:
#			if checkLegal(fromCoord,toCoord,piece) == None:
#				count = count + 1
#				posFrom = fromCoord
#				if count > 1:
#					print "There are multiple pieces which can do that move"
#					return 1
#		if count == 1:
#			return posFrom
#		return 1
#	elif mtype == "coord":
#		fromCoord = chessToCoord(str[:2])
#		if player not in board[fromCoord[1]][fromCoord[0]]:
#			print "Select your own piece"
#			return 1
#		piece = board[fromCoord[1]][fromCoord[0]][1]
#		if checkLegal(fromCoord,toCoord,piece) != None:
#			print checkLegal(fromCoord,toCoord,piece)
#			return 1
#		else:
#			return fromCoord
			
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

def checkLegal(piece, posTo):
	move = [posTo[0]-piece.pos[0],posTo[1]-piece.pos[1]]
	if piece.isLegal(move) != 0:
		return 1
	if board[posTo[0]][posTo[1]] == "   ":
		return 0
	if pieceDict[board[posTo[0]][posTo[1]]].team != piece.team and piece.isLegal(move) == 0:
		return 0

def movePiece(posFrom, posTo):
	if board[posTo[0]][posTo[1]] != "   ":
		pieceDict[board[posTo[0]][posTo[1]]].status = 1
	board[posTo[0]][posTo[1]] = board[posFrom[0]][posFrom[1]]
	board[posFrom[0]][posFrom[1]] = "   "
	return 0
#	posFrom[0],posFrom[1] = posTo[0],posTo[1]

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

def setupPieces(board): # this is an init type function, sets up all the pieces on the board by calling them shortcode given on the board. problems with multiple pieces on same team needing uniques. 
	for x in range(len(board)):
		for y in range(len(board[x])):
			if board[x][y] != "   ":
				print "Found piece",board[x][y],", creating new",pieces[board[x][y][-2]]
				pieceDict[board[x][y]] = (pieces[board[x][y][-2]])([x, y],int(board[x][y][0]))

def player(num):
	print "Player",num,"turn: \n\n"
	while True:
		naturalInput = raw_input("Your move (standard chess notation):")
		result = decodeNotation(num,naturalInput)
		if result == 0:
			break
		else:
			print result
			print "Invalid input"

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
history = []

#MAIN LOOP
quit = False
setupPieces(board)
while quit == False:
	printBoard(board)
	player("1")
	printBoard(board)
	player("2")