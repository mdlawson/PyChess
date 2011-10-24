import sys
import os
from string import replace

def containsAny(str, set):
	return 1 in [c in str for c in set]

def decodeNotation(player,str):
	if (len(str) == 2) and (containsAny(str[:1],"abcdefgh")) and (containsAny(str[1:],"12345678")):
		piece = "p"
		mtype = "normal"
		toCoord = chessToCoord(str)

	elif (len(str) == 3) and (containsAny(str[0],"KQRBNp") == 1) and (containsAny(str[1],"abcdefgh") == 1) and (containsAny(str[2],"12345678") == 1):
		piece = str[0]
		mtype = "normal"
		toCoord = chessToCoord(str[1:])
	
	elif str == "0-0":
		err,toCoord,fromCoord = checkCastling("kingside",player)
		if err == 0:
			return toCoord,fromCoord
		else:
			print err
			print "Can't castle"
			return 1,1

	elif str == "0-0-0":
		err,toCoord,fromCoord = checkCastling("queenside",player)
		if err == 0:
			return toCoord,fromCoord
		else:
			print err
			print "Can't castle"
			return 1,1

	elif (len(str) == 4) and (containsAny(str[0],"abcdefgh") == 1) and (containsAny(str[1],"12345678") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		piece = "unknown"
		mtype = "coord"
		toCoord = chessToCoord(str[2:])

	elif (len(str) == 4) and (containsAny(str[0],"KQRBNp") == 1) and (containsAny(str[1],"x") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "normaltake"
		piece = str[0]
		toCoord = chessToCoord(str[2:])

#	elif (len(str) == 4) and (containsAny(str[1:],"+") == 0):
#		mtype = "check"

#	elif (len(str) == 5):

	else: # This could be refactored
		return 1,1
	if takingOwnPiece(player,toCoord) == None and workOutPosFrom(player,piece,toCoord,mtype,str) != 1:
		return toCoord,workOutPosFrom(player,piece,toCoord,mtype,str)
	else:
		return 1,1	

def workOutPosFrom(player,piece,toCoord,mtype,str):
	if mtype[:6] == "normal":
		if (mtype[6:] == "take") and (board[toCoord[1]][toCoord[0]] == "  "):
			print "You aren't taking anything"
		coords = checkWhere(player,piece)
		count = 0
		for fromCoord in coords:
			if checkLegal(fromCoord,toCoord,piece) == None:
				count = count + 1
				posFrom = fromCoord
				if count > 1:
					print "There are multiple pieces which can do that move"
					return 1
		if count == 1:
			return posFrom
		return 1
	elif mtype == "coord":
		fromCoord = chessToCoord(str[:2])
		if player not in board[fromCoord[1]][fromCoord[0]]:
			print "Select your own piece"
			return 1
		piece = board[fromCoord[1]][fromCoord[0]][1]
		if checkLegal(fromCoord,toCoord,piece) != None:
			print checkLegal(fromCoord,toCoord,piece)
			return 1
		else:
			return fromCoord

def takingOwnPiece(player,toCoord):
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

def checkLegal(posFrom,posTo, piece):
	pmove = [0,0]
	pmove[0] = posTo[0]-posFrom[0]
	pmove[1] = posTo[1]-posFrom[1]
	if "R" in piece:
		return checkPlus(posFrom,posTo,pmove)
	if "B" in piece:
		return checkCross(posFrom,posTo,pmove,piece)
	if "Q" in piece:
		if (checkCross(posFrom,posTo,pmove,piece)==1) and (checkPlus(posFrom,posTo,pmove,piece)==1):
			print "Invalid move for queen"
			return 1
	if "p" in piece:
		return checkPawn(posFrom,posTo,pmove,piece)
	if "N" in piece:
		return checkKnight(posFrom,posTo,pmove)
	if "K" in piece:
		return checkKing(pmove)

def checkingLoop(axis,pmove,posFrom):
	for i in range(0,pmove[axis]-(pmove[axis]/abs(pmove[axis])),pmove[axis]/abs(pmove[axis])):
		i = i+(pmove[axis]/abs(pmove[axis]))
		if axis==0:
			if board[posFrom[1-axis]][posFrom[axis]+i] != "  ":
				return "there is a piece in the way!"
		else:
			if board[posFrom[axis]+i][posFrom[1-axis]] != "  ":
				return "there is a piece in the way!"
	
def checkPlus(posFrom,posTo,pmove):
	if (pmove[0] != 0) and (pmove[1] != 0):
		if "Q" not in piece:
			return "movement is not in a straight line"
		return 1
	if (pmove[1] == 0): 
		return checkingLoop(0,pmove,posFrom)
	else:
		return checkingLoop(1,pmove,posFrom)

def checkCross(posFrom,posTo,pmove,piece):
	if abs(pmove[0])!=abs(pmove[1]):
		if "Q" not in piece:	
			return "movement is not in a diagonal line"
		return 1
	for i in range(0,pmove[0]-pmove[0]/abs(pmove[0]),pmove[0]/abs(pmove[0])):
		i = i+(pmove[0]/abs(pmove[0]))
		j = abs(i)*(pmove[1]/abs(pmove[1]))
		if board[posFrom[1]+j][posFrom[0]+i] != "  ":
			return "there is a piece in the way!"

def checkPawn(posFrom,posTo,pmove,piece):	# Needs en passant support
	if ("1" in piece):
		if (pmove[1] > 0): 
			return "Pawns can't move backwards"
	if ("2" in piece): 
		if (pmove[1] < 0):
			return "Pawns can't move backwards"
	if (abs(pmove[1]) > 2):
		return "A pawn can't move more than 2 squares in the y-direction under any circumstances"
	if (abs(pmove[1]) != 1) and (posFrom[1] != 1) and (posFrom[1] != 6):
		return "A pawn can only move 1 square in the y-direction"
	if (pmove[0] != 0) and (abs(pmove[0]) != 1) and (abs(pmove[1]) != 1):
		return "Can't move like that"
	if (abs(pmove[0]) == 1) and (abs(pmove[1]) == 1) and (board[posTo[1]][posTo[0]] == "  "):
		return "No piece to be taken"
	if (abs(pmove[1]) == 2) and (pmove[0] != 0):
		return "Can't move like that"
	if (abs(pmove[0]) == 0) and (board[posTo[1]][posTo[0]] != "  "):
		return "Can't take moving directly forward"
	if (abs(pmove[0]) >1):
		return "Can't move like that"

def checkKnight(posFrom,posTo,pmove):
	nmove = [abs(pmove[0]),abs(pmove[1])]
	if (nmove != [1,2]) and (nmove != [2,1]):
		return "Invalid move for Knight"

def checkKing(pmove):	# Needs checking to whether King is moving into check, and castling needed as well
	kmove = [abs(pmove[0]),abs(pmove[1])]
	if (kmove != [0,1]) and (kmove != [1,0]) and (kmove != [1,1]):
		return "King can only move one space at a time"

def checkCastling(str,player):
	if checkHistory(str,player) != None:
		return checkHistory(str,player),1,1
	if player == "1":
		if str == "kingside":
			if checkingLoop(0,[2,0],[4,7]) != None:
				return "There is a piece in the way",1,1
			move([4,7],[6,7])
			return 0,[5,7],[7,7]
		elif str == "queenside":
			print "ola"
			if checkingLoop(0,[-3,0],[4,7]) != None:
				print "allah"
				return "There is a piece in the way",1,1
			move([4,7],[1,7])
			return 0,[2,7],[0,7]
	elif player == "2":
		if str == "kingside":
			if checkingLoop(0,[2,0],[4,0]) != None:
				return "There is a piece in the way",1,1
			move([4,0],[6,0])
			return 0,[5,0],[7,0]
		elif str == "queenside":
			if checkingLoop(0,[-3,0],[4,0]) != None:
				return "There is a piece in the way",1,1
			move([4,0],[1,0])
			return 0,[2,0],[0,0]

def checkHistory(str,player):
	if player == "1":
		for i in history:
			if (i[0] == 4) and (i[1] == 7):
				print i[0],i[1]
				return "You've already moved your king"
		if str == "kingside":
			for i in history:
				if (i[0] == 7) and (i[1] == 7):
					return "You've already moved your rook"
		if str == "queenside":
			for i in history:
				if (i[0] == 0) and (i[1] == 7):
					return "You've already moved your rook"
	if player == "2":
		for i in history:
			if (i[2] == 4) and (i[3] == 0):
				return "You've already moved your king"
		if str == "kingside":
			for i in history:
				if (i[2] == 7) and (i[3] == 0):
					return "You've already moved your rook"
		if str == "queenside":
			for i in history:
				if (i[2] == 0) and (i[3] == 0):
					return "You've already moved your rook"

def printBoard(board):	# Prints board obviously, colored comes from library
	#os.system("clear")
	i = True
	for row in board:
		for column in row:
			if i==True: 
				sys.stdout.write('\033[47m\033[30m '+column+' \033[0m')
				i=not i
			else:
				sys.stdout.write(" "+column+" ")
				i=not i
		print ""
		i=not i

def player(num):
	print "Player",num,"turn: \n\n"
	while True:
		naturalInput = raw_input("Your move (standard chess notation):")
		toCoord,fromCoord = decodeNotation(num,naturalInput)
		if toCoord !=1:
			break
		else:
			print "Invalid input"
	
	Coord = [fromCoord[0], fromCoord[1], toCoord[0], toCoord[1]]
	history.append(Coord)
	print history
	move(fromCoord,toCoord)
board = [									# This is the original board
["2R","2N","2B","2Q","2K","2B","2N","2R"],
["2p","2p","2p","2p","2p","2p","2p","2p"],	# I changed bishops and knights the right way round
["  ","  ","  ","  ","  ","  ","  ","  "],	# N = Knights, as in normal chess notation, "N"
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
	player("1")
	printBoard(board)
	player("2")