import sys
import os
from string import replace
from termcolor import colored

def containsAny(str, set):
	return 1 in [c in str for c in set]

def decodeNotation(player,str,board):
	if (len(str) == 2) and (containsAny(str[:1],"abcdefgh")) and (containsAny(str[1:],"12345678")):
		piece = "p"
		mtype = "pawnsimple"
#		if takingOwnPiece(player,board,toCoord) != 1 and checkInitial(player,piece,toCoord,board,mtype,str) != 1:
#			return toCoord,checkInitial(player,piece,toCoord,board,mtype,str)
#		else:
#			return 1

	if (len(str) == 3) and (containsAny(str[0],"KQRBNp") == 1) and (containsAny(str[1],"abcdefgh") == 1) and (containsAny(str[2],"12345678") == 1):
		piece = str[0]
		mtype = "3"
		toCoord = chessToCoord(str[1:])
#		if takingOwnPiece(player,board,toCoord) != 1 and checkInitial(player,piece,toCoord,board,mtype,str) != 1:
#			return toCoord,checkInitial(player,piece,toCoord,board,mtype,str)
#		else:
#			return 1

	if (len(str) == 4) and (containsAny(str[0],"abcdefgh") == 1) and (containsAny(str[1],"12345678") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "coord"
		piece = "unknown"
		toCoord = chessToCoord(str[2:])
#		if takingOwnPiece(player,board,toCoord) != 1 and checkInitial(player,piece,toCoord,board,mtype,str) != 1:
#			return toCoord,checkInitial(player,piece,toCoord,board,mtype,str)
#		else:
#			return 1

#	if (len(str) == 4) and (containsAny(str[1],"x") == 0):
#		mtype = "take"
#	if (len(str) == 4) and (containsAny(str[1:],"+") == 0):
#		mtype = "check"
#	if (len(str) == 5):
	if takingOwnPiece(player,board,toCoord) != 1 and checkInitial(player,piece,toCoord,board,mtype,str) != 1:
		return toCoord,checkInitial(player,piece,toCoord,board,mtype,str)
	else:
		return 1
#		

def checkInitial(player,piece,toCoord,board,mtype,str):

	if mtype == "pawnsimple":
		toCoord = chessToCoord(str)
		print board[toCoord[1]][toCoord[0]]
		if player in board[toCoord[1]][toCoord[0]]:
				print "You cant take your own pieces!"
		else:
			posFrom = [toCoord[0],toCoord[1]+1]
			return posFrom
	if mtype == "3":
		coords = checkWhere(player,piece)
		count = 0
		for fromCoord in coords:
			print "This is fromcoord",fromCoord
			if checkLegal(fromCoord,toCoord,board,piece) != 1:
				count = count + 1
				print 
				posFrom = fromCoord
				if count > 1:
					print "There are multiple pieces which can do that move"
					return 1
		if count == 1:
			return posFrom
		return 1
	if mtype == "coord":
		fromCoord = chessToCoord(str[:2])
		print fromCoord
		if player not in board[fromCoord[1]][fromCoord[0]]:
			print "Select your own piece"
			return 1
		piece = board[fromCoord[1]][fromCoord[0]][1]
		if checkLegal(fromCoord,toCoord,board,piece) == 1:
			return 1
		else:
			return fromCoord

def takingOwnPiece(player,board,toCoord):
	if player in board[toCoord[1]][toCoord[0]]:
		print "You can't take your own pieces!"
		return 1

def checkWhere(player, piece):
	count = 0
	coords = []
	coordx = -1
	coordy = -1
	for i in board:
		coordy = coordy + 1
		for j in i:
			coordx = coordx + 1
			if j == str(player)+piece:
				count = count + 1
				coords.append([coordx-((coordy)*8),coordy])
	return coords

#def letterToNum(str):
#	out = replace(str, "W","1")
#	return replace(out, "B","2")

def chessToCoord(str):
	coord = [0,0]
	char = str[:1]
	coord[0] = ord(char)-97
	num = str[1:]
	coord[1] = 8-int(num)
	return coord

def edgeDetect(x, y):
	if (x < 8) and (y < 8) and (x > -1) and (y > -1): # Included idiot detection
		return 0
	else:
		print "Ehmmm, that's off the board you git"
		return 1

def move(posFrom, posTo):
	piece = board[posFrom[1]][posFrom[0]]
	board[posFrom[1]][posFrom[0]] = "  "
	board[posTo[1]][posTo[0]] = piece

def checkLegal(posFrom,posTo, board, piece):
	pmove = [0,0]
	pmove[0] = posTo[0]-posFrom[0]
	pmove[1] = posTo[1]-posFrom[1]
	if "R" in piece:
		return checkPlus(posFrom,posTo,pmove,board)
	if "B" in piece:
		return checkCross(posFrom,posTo,pmove,board,piece)
	if "Q" in piece:
		if (checkCross(posFrom,posTo,pmove,board,piece)==1) and (checkPlus(posFrom,posTo,pmove,board,piece)==1):
			print "Invalid move for queen"
			return 1
	if "p" in piece:
		return checkPawn(posFrom,posTo,pmove,board,piece)
	if "N" in piece:
		return checkKnight(posFrom,posTo,pmove,board)
	if "K" in piece:
		return checkKing(pmove)

def checkingLoop(axis,pmove,posFrom,piece):
	for i in range(0,pmove[axis]-(pmove[axis]/abs(pmove[axis])),pmove[axis]/abs(pmove[axis])):
		i = i+(pmove[axis]/abs(pmove[axis]))
		if axis==0:
			if board[posFrom[1-axis]][posFrom[axis]+i] != "  ":
				print "there is a piece in the way!"
				return 1
		else:
			if board[posFrom[axis]+i][posFrom[1-axis]] != "  ":
				print "there is a piece in the way!"
				return 1
	
def checkPlus(posFrom,posTo,pmove,board):
	if (pmove[0] != 0) and (pmove[1] != 0):
		if "Q" not in piece:
			print "movement is not in a straight line"
		return 1
	if (pmove[1] == 0): 
		return checkingLoop(0,pmove,posFrom)
	else:
		return checkingLoop(1,pmove,posFrom)

def checkCross(posFrom,posTo,pmove,board,piece):
	if abs(pmove[0])!=abs(pmove[1]):
		if "Q" not in piece:	
			print "movement is not in a diagonal line"
		return 1
	for i in range(0,pmove[0]-pmove[0]/abs(pmove[0]),pmove[0]/abs(pmove[0])):
		i = i+(pmove[0]/abs(pmove[0]))
		j = abs(i)*(pmove[1]/abs(pmove[1]))
		if board[posFrom[1]+j][posFrom[0]+i] != "  ":
			print "there is a piece in the way!"
			return 1

def checkPawn(posFrom,posTo,pmove,board,piece):	# Needs en passant support
	if ("1" in piece):
		if (pmove[1] > 0):
			print "Pawns can't move backwards"
			return 1
	if ("2" in piece): 
		if (pmove[1] < 0):
			print "Pawns can't move backwards"
			return 1
	if  (abs(pmove[1]) > 2):
		print "A pawn can't move more than 2 squares in the y-direction under any circumstances"
	if (abs(pmove[1]) != 1) and (posFrom[1] != 1) and (posFrom[1] != 6):
		print "A pawn can only move 1 square in the y-direction"
		return 1
	if (pmove[0] != 0) and (abs(pmove[0]) != 1) and (abs(pmove[1]) != 1):
		print "Can't move like that"
		return 1
	if (abs(pmove[0]) == 1) and (abs(pmove[1]) == 1) and (board[posTo[1]][posTo[0]] == "  "):
		print "No piece to be taken"
		return 1
	if (abs(pmove[1]) == 2) and (pmove[0] != 0):
		return 1

def checkKnight(posFrom,posTo,pmove,board):
	nmove = [abs(pmove[0]),abs(pmove[1])]
	if (nmove != [1,2]) and (nmove != [2,1]):
		print "Invalid move for Knight"
		return 1

def checkKing(pmove):	# Needs checking to whether King is moving into check, and castling needed as well
	kmove = [abs(pmove[0]),abs(pmove[1])]
	if (kmove != [0,1]) and (kmove != [1,0]) and (kmove != [1,1]):
		print "King can only move one space at a time"
		return 1

def printBoard(board):	# Prints board obviously, colored comes from library
	#os.system("clear")
	i = True
	for row in board:
		for column in row:
			if i==True: 
				sys.stdout.write(colored(" "+column+" ", "grey","on_white"))
				i=not i
			else:
				sys.stdout.write(" "+column+" ")
				i=not i
		print ""
		i=not i

def player(board, num, history):
	print "Player",num,"turn: \n\n"
	while True:
		naturalInput = raw_input("Your move (standard chess notation):")
		if decodeNotation(num,naturalInput,board) == 1:
			print "Invalid input"
		else:
			toCoord,fromCoord = decodeNotation(num,naturalInput,board)
			break
#		else :
#			toCoord = [0,0]
#			toCoord = chessToCoord(naturalInput[2:])
#
#			break
#		while True:
#			fromCoord = chessToCoord(raw_input("Enter the piece you want to move: "))
#			if edgeDetect(fromCoord[0], fromCoord[1]) == 0:
#				piece = board[fromCoord[1]][fromCoord[0]]
#				print "Piece selected:",piece
#				if str(num) in letterToNum(piece):
#					break
#				else: 
#					print "Invalid piece!"
#		toCoord = chessToCoord(raw_input("Enter the destination to move to: "))
#		if edgeDetect(toCoord[0],toCoord[1]) == 0:
#			if str(num) in letterToNum(board[toCoord[1]][toCoord[0]]):
#				print "You cant take your own pieces!"
#			elif checkLegal(fromCoord,toCoord, board, piece) == 1:
#				print "Ilegal move!"
#			else: 
#				break
	
	Coord = [fromCoord[0], fromCoord[1], toCoord[0], toCoord[1]]
	print Coord
	history.append(Coord)
	#print history
	move(fromCoord,toCoord)
board = [									# This is the original board
["2R","2N","2B","2Q","2K","2B","2N","2R"],
["2p","2p","2p","2p","2p","2p","2p","2p"],	# I changed bishops and knights the right way round
["  ","  ","  ","  ","  ","  ","  ","  "],	# n = Knights, as in normal chess notation, "N"
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["1p","1p","1p","1p","1p","1p","1p","1p"],
["1R","1N","1B","1Q","1K","1B","1N","1R"],
]

history = []

#MAIN LOOP
quit = False
while quit == False:
	printBoard(board)
	player(board, "1", history)
	printBoard(board)
	player(board, "2", history)