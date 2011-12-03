import sys
from itertools import izip_longest

class Piece:
	def __init__(self, pos, color): 
		self.pos = pos
		self.color = color
		self.status = 0
	def moves(self):
		return mappingLoop(self)

class Rook(Piece): # This is a class for a piece
	def isLegal(self, move): # Piece.isLegal checks if a move is legal for th currect piece. takes 1 arg, as self is always supplied
		if move[0] == 0 or move[1] == 0:
			return 0 if checkingLoop(self, move) == 0 else 1
		else:
			return 1
class Bishop(Piece):
	def isLegal(self, move):
		if abs(move[0])==abs(move[1]):
			return 0 if checkingLoop(self, move) == 0 else 1
		else:
			return 1
class Knight(Piece):
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		move = [abs(move[0]),abs(move[1])]
		return 0 if move == [1,2] or move == [2,1] else 1
class King(Piece):
	def isLegal(self, move):
		move = [abs(move[0]),abs(move[1])]
		return 0 if move == [1,0] or move == [0,1] or move == [1,1] else 1
class Queen(Piece):
	def isLegal(self, move):
		if abs(move[0])==abs(move[1]) or move[0] == 0 or move[1] == 0:
			return 0 if checkingLoop(self, move) == 0 else 1
		else:
			return 1
class Pawn(Piece):
	def isLegal(self, move):
		global enpassant, takeenpassant
		if self.color == 1 and move[1] < 0:		 #Pawn can't go backwards
			return 1
		if self.color == 2 and move[1] > 0:		 #Pawn can't go backwards
			return 1
		if abs(move[1]) > 2:					#Pawn can't move more than 2 squares in y-direction in any circumstances
			return 1
		if abs(move[0]) > 1:					#Pawn can't move more than 1 square in x-direction under any circumstances
			return 1
		if abs(move[1]) != 1 and self.pos[1] != 1 and self.pos[1] != 6: #Pawn can only move two when haven't moved
			return 1
		if abs(move[0]) == 1 and abs(move[1]) != 1:
			return 1
		if enpassant != [[0,0],0] and board[self.pos[0]+move[0]][self.pos[1]+move[1]] == "   " and abs(move[0]) == 1 and abs(move[1]) == 1 and abs(self.pos[0]-enpassant[0][0]) == 1 and abs((self.pos[1]+move[1])-enpassant[0][1]) == 1 and (self.pos[0]+move[0])-enpassant[0][0] == 0 and self.color != enpassant[1]:
			takeenpassant = self
			return 0
		if abs(move[1]) == 2 and board[self.pos[0]+move[0]][self.pos[1]+(abs(move[1])/move[1])] != "   ":
			return 1
		if abs(move[0]) == 1 and board[self.pos[0]+move[0]][self.pos[1]+move[1]] == "   ":
			return 1
		if abs(move[0]) == 0 and board[self.pos[0]+move[0]][self.pos[1]+move[1]] != "   ":
			return 1
		return 0

def mappingLoop(piece): #produces an array of valid moves for any given piece
	valid = []
	for x in range(8):
		for y in range(8):
			if piece.isLegal([(x-piece.pos[0]),(y-piece.pos[1])]) == 0 and checkLegal(piece,[x,y]) == 0:
				valid.append([x,y])
	return valid

def checkingLoop(piece, move): # generic collision detection function
	capture = 0
	xRange = range(-1, move[0]-1, -1) if move[0] < 0 else range(1, move[0]+1, 1)
	yRange = range(-1, move[1]-1, -1) if move[1] < 0 else range(1, move[1]+1, 1)
	for x,y in izip_longest(xRange,yRange, fillvalue=0):
		if capture == 1:
			return 1
		if board[piece.pos[0]+x][piece.pos[1]+y][0] == str(piece.color):
			return 1
		if board[piece.pos[0]+x][piece.pos[1]+y] != "   ":
			capture = 1
	return 0

def containsAny(str, set):
	return 1 in [c in str for c in set]

def decodeNotation(player,str):
	global fiftymoverule, check, takeenpassant, enpassant
	inputcheck,inputcheckmate = 0,0
	if str[-2:] == "?!":
		str = str[:-2]
		print "?!?!?!?!?!"
	if str[-2:] == "!?":
		str = str[:-2]
		print "!?!?!?!?!?"
	if str[-2:] == "!!":
		str = str[:-2]
		print "Sheesh louise"
	if str[-1] == "!":
		str = str[:-1]
		print "Alright, don't get cocky"
	if str[-2:] == "??":
		str = str[:-2]
		print "Ehmmm??"
	if str[-1] == "?":
		str = str[:-1]
		print "You weirdo"
	if str[-2:] == "++":
		inputcheckmate = 1
		str = str[:-2]
	if str[-1] == "+":
		inputcheck = 1
		str = str[:-1]
	if (len(str) == 2) and (containsAny(str[0],"abcdefgh")) and (containsAny(str[1],"12345678")):
		mtype = "normal"
		pieceType = player+"p"
		posTo = chessToCoord(str)
	elif (len(str) == 3) and (containsAny(str[0],"KQRBNp") == 1) and (containsAny(str[1],"abcdefgh") == 1) and (containsAny(str[2],"12345678") == 1):
		mtype = "normal"
		pieceType = player+str[0]
		posTo = chessToCoord(str[1:])
	elif str == "0-0":
		err = checkCastling("kingside",player)
		return err
	elif str == "0-0-0":
		err = checkCastling("queenside",player)
		return err
	elif (len(str) == 4) and (containsAny(str[0],"abcdefgh") == 1) and (containsAny(str[1],"12345678") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "coord"
		posTo = chessToCoord(str[2:])
		posFrom = chessToCoord(str[:2])
		piece = board[posFrom[0]][posFrom[1]]
	elif (len(str) == 4) and (containsAny(str[0],"KQRBNp") == 1) and (containsAny(str[1],"x") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "normaltake"
		pieceType = player+str[0]
		posTo = chessToCoord(str[2:])
	elif (len(str) == 4) and (containsAny(str[0],"abcdefgh") == 1) and (containsAny(str[1],"x") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "special"
		posTo = chessToCoord(str[2:])
		x = chessToCoord(str[0]+"1")[0]
		count = 0
		for piece1 in pieceDict:
			if piece1[:2] == player+"p" and pieceDict[piece1].status != 1 and pieceDict[piece1].pos[0] == x and posTo in pieceDict[piece1].moves():
				count = count + 1
				piece = piece1
		if count == 0:
			return "There aren't any pawns on "+str[0]+"-file"
		elif count != 1:
			return "There is more than one pawn on the "+str[0]+"-file which can take that piece. Please be more specific"
	elif (len(str) == 4) and (containsAny(str[0], "RBNp") == 1) and (containsAny(str[1],"abcdefgh") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "special"
		posTo = chessToCoord(str[2:])
		x = chessToCoord(str[1]+"1")[0]
		count = 0
		for piece1 in pieceDict:
			if piece1[:2] == player+str[0] and pieceDict[piece1].status != 1 and pieceDict[piece1].pos[0] == x and posTo in pieceDict[piece1].moves():
				count = count + 1
				piece = piece1
		if count == 0:
			return "There aren't any "+piecenames[str[0]]+"s on the "+str[1]+"-file"
		elif count != 1:
			return "There is more than one "+piecenames[str[0]]+" on the "+str[1]+"-file which can take that piece. Please be more specific"
	elif (len(str) == 4) and (containsAny(str[0], "RBNp") == 1) and (containsAny(str[1],"12345678") == 1) and (containsAny(str[2],"abcdefgh") == 1) and (containsAny(str[3],"12345678") == 1):
		mtype = "special"
		posTo = chessToCoord(str[2:])
		x = chessToCoord("a"+str[1])[1]
		count = 0
		for piece1 in pieceDict:
			if piece1[:2] == player+str[0] and pieceDict[piece1].status != 1 and pieceDict[piece1].pos[1] == x and posTo in pieceDict[piece1].moves():
				count = count + 1
				piece = piece1
		if count == 0:
			return "There aren't any "+piecenames[str[0]]+"s on the "+str[1]+"-rank"
		elif count != 1:
			return "There is more than one "+piecenames[str[0]]+" on the "+str[1]+"-rank which can take that piece. Please be more specific"
	elif (len(str) == 5) and (containsAny(str[0], "KQRBNp") == 1) and (containsAny(str[1],"abcdefgh") == 1) and (containsAny(str[2],"12345678") == 1) and (containsAny(str[3],"abcdefgh") == 1) and (containsAny(str[4],"12345678") == 1):
		mtype = "coord"
		posTo = chessToCoord(str[3:])
		posFrom = chessToCoord(str[1:3])
		piece = board[posFrom[0]][posFrom[1]]
	elif (len(str) == 3) and (containsAny(str[0], "KQRBNp") == 1) and (str[1] == "x") and (containsAny(str[2], "KQRBNp") == 1):
		mtype = "specialspecial"
		listpiece1 = []
		listpiece2 = []
		for piece1 in pieceDict:
			if piece1[:2] == player+str[0] and pieceDict[piece1].status != 1:
				listpiece1.append(piece1)
			if piece1[:2] == `((not (int(player)-1))+1)`+str[2] and pieceDict[piece1].status != 1:
				listpiece2.append(piece1)
		count = 0
		for piece1 in listpiece1:
			for piece2 in listpiece2:
				if pieceDict[piece2].pos in pieceDict[piece1].moves():
					piece = piece1
					posTo = pieceDict[piece2].pos
					count = count + 1
		if count == 0:
			return "No "+piecenames[str[0]]+"s are able to take an opposition's "+piecenames[str[2]]
		elif count != 1:
			return "Be more specific"
	else:
		return "Unknown Notation"

	if mtype[:6] == "normal":
		if (mtype[6:] == "take") and (board[posTo[0]][posTo[1]] == "   "):
			print "You aren't taking anything"
		count = 0
		for i in pieceDict:
			if i[:2] == pieceType and checkLegal(pieceDict[i],posTo) == 0 and pieceDict[i].status != 1:
				count = count + 1
				piece = i
		if count == 0:
			return "Piece can't move there"
		if count != 1:
			return "More than one piece can move there"
	if checkLegal(pieceDict[piece],posTo) == 0:
		if piece[1] == "p" and abs(posTo[1]-pieceDict[piece].pos[1]) == 2:
			enpassant = [pieceDict[piece].pos,pieceDict[piece].color]
		oldPos = pieceDict[piece].pos
		movePiece(pieceDict[piece].pos,posTo)
		pieceDict[piece].pos = posTo
		if takeenpassant == pieceDict[piece]:
			if player == "1":
				if board[posTo[0]][posTo[1]-1] != "   "
					oldenpassant = pieceDict[board[posTo[0]][posTo[1]-1]]
					pieceDict[board[posTo[0]][posTo[1]-1]].status = 1
				board[posTo[0]][posTo[1]-1] = "   "
			elif player == "2":
				if board[posTo[0]][posTo[1]+1] != "   ":
					oldenpassant = pieceDict[board[posTo[0]][posTo[1]+1]]
					pieceDict[board[posTo[0]][posTo[1]+1]].status = 1
				board[posTo[0]][posTo[1]+1] = "   "
		if int(player) == check:
			if isCheck(int(player)) == True:
				print "You are still in check!"
				pieceDict[piece].pos = oldPos
				movePiece(posTo,oldPos)
				if takeenpassant == pieceDict[piece]:
					if player == "1":
						pieceDict[board[posTo[0]][posTo[1]-1]] = oldenpassant
						pieceDict[board[posTo[0]][posTo[1]-1]].status = 0
					elif player == "2":
						pieceDict[board[posTo[0]][posTo[1]+1]] = oldenpassant
						pieceDict[board[posTo[0]][posTo[1]+1]].status = 0
					takeenpassant = 0
				return "Move not Legal"
			else:
				check = 0
		if isCheck(int(player)) == True:
			print "You are moving into check"
			pieceDict[piece].pos = oldPos
			movePiece(posTo,oldPos)
			if takeenpassant == pieceDict[piece]:
				if player == "1":
					pieceDict[board[posTo[0]][posTo[1]-1]] = oldenpassant
					pieceDict[board[posTo[0]][posTo[1]-1]].status = 0
				elif player == "2":
					pieceDict[board[posTo[0]][posTo[1]+1]] = oldenpassant
					pieceDict[board[posTo[0]][posTo[1]+1]].status = 0
				takeenpassant = 0
			return "Move not Legal"
		if piece[1] == "p":
			fiftymoverule = 0
			if posTo[1] == 0 or posTo[1] == 7:
				piece = promotePawn(posTo)
		Coord = [pieceDict[piece].pos[0], pieceDict[piece].pos[1], posTo[0], posTo[1]]
		history.append(Coord)
		if isCheck((not (int(player)-1))+1) == True:
			if isCheckmate((not (int(player)-1))+1) == True:
				return "That's checkmate"
			elif inputcheckmate != 0:
				print "That wasn't checkmate"
		else:
			if isCheckmate((not (int(player)-1))+1) == True:
				return "That's stalemate, BAHAHAHAHA"
			if inputcheck == 1:
				print "That isn't check"
			check = 0
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

def checkLegal(piece, posTo):
	move = [posTo[0]-piece.pos[0],posTo[1]-piece.pos[1]]
	if piece.isLegal(move) != 0:
		return 1
	if board[posTo[0]][posTo[1]] == "   ":
		return 0
	if pieceDict[board[posTo[0]][posTo[1]]].color != piece.color and piece.isLegal(move) == 0:
		return 0
	else:
		return 1

def isCheck(color):
	global check
	for piece in pieceDict:
		if pieceDict[piece].color != color and pieceDict[piece].status != 1:
			if pieceDict[str(color)+"K1"].pos in pieceDict[piece].moves():
				check = color
				return True
	return False

def isCheckmate(color):
	for piece in pieceDict:
		if pieceDict[piece].color == color and pieceDict[piece].status != 1:
			for move in pieceDict[piece].moves():
				oldPos = pieceDict[piece].pos
				pieceDict[piece].pos = move
				oldPiece = board[move[0]][move[1]]
				movePiece(oldPos, move)
				if isCheck(color) == False:
					movePiece(move, oldPos)
					if oldPiece != "   ":
						pieceDict[oldPiece].status = 0
					board[move[0]][move[1]] = oldPiece
					pieceDict[piece].pos = oldPos
					return False
				movePiece(pieceDict[piece].pos, oldPos)
				if oldPiece != "   ":
					pieceDict[oldPiece].status = 0
				board[move[0]][move[1]] = oldPiece
				pieceDict[piece].pos = oldPos
	return True

def checkCastling(str,player):
	if isCheck(int(player)) == True:
		return "Castling not permitted due to you being in check"
	global check
	piece = player+"R"
	king = player+"K1"
	oldPos = pieceDict[king].pos
	if checkHistory(str,player) != 0:
		return checkHistory(str,player)
	if player == "1":
		y = 0
	elif player == "2":
		y = 7
	if str == "kingside":
		piece = piece + "2"
		checkx,bx,cx,dx = -2,6,7,5
	elif str == "queenside":
		piece = piece + "1"
		checkx,bx,cx,dx = 3,1,0,2
	if checkingLoop(pieceDict[piece],[checkx,0]) == 1:
		return "There is a piece in the way"
	xRange = range(-1, bx-5, -1) if bx-4 < 0 else range(1, bx-3, 1)
	for x in xRange:
		movePiece(pieceDict[king].pos,[oldPos[0]+x,pieceDict[king].pos[1]])
		pieceDict[king].pos = [oldPos[0]+x,pieceDict[king].pos[1]]
		if isCheck(int(player)) == True:
			movePiece(pieceDict[king].pos,oldPos)
			pieceDict[king].pos = oldPos
			check = 0
			return "Castling is not permitted due to you moving through or into check"
	pieceDict[piece].pos = [dx,y]
	movePiece([cx,y],[dx,y])
	return 0

def checkHistory(str,player):
	if player == "1":
		a,c,d = 0,1,0
	elif player == "2":
		a,c,d = 2,3,7
	if str == "kingside":
		b = [4,7]
	elif str == "queenside":
		b = [4,0]
	while b != []:
		for i in history:
			if (i[a] == b[0]) and (i[c] == d):
				if (b[0] == 4):
					return "You've already moved your king"
				else:
					return "You've already moved your rook"
		b = b[1:]
	return 0

def promotePawn(pos):
	global pieceDict
	input = 0
	while input == 0:
		pieceType = raw_input("Choose a piece: ")
		if pieceType == "Q" or pieceType == "R" or pieceType == "B" or pieceType == "N":
			input = 1
		else:
			print "Invalid piece. Type in Q, R, B or N"
	del pieceDict[board[pos[0]][pos[1]]]
	count = 1
	for piece1 in pieceDict:
		if piece1[:2] == board[pos[0]][pos[1]][0]+pieceType:
			count = int(piece1[-1])+1
	piece = board[pos[0]][pos[1]][0]+pieceType+`count`
	board[pos[0]][pos[1]] =  piece
	pieceDict[piece] = pieces[pieceType]([pos[0], pos[1]],int(board[pos[0]][pos[1]][0]))
	return piece

def movePiece(posFrom, posTo):
	global fiftymoverule
	if board[posTo[0]][posTo[1]] != "   ":
		pieceDict[board[posTo[0]][posTo[1]]].status = 1
		fiftymoverule = 0
	board[posTo[0]][posTo[1]] = board[posFrom[0]][posFrom[1]]
	board[posFrom[0]][posFrom[1]] = "   "
	return 0

def printBoard(board):  # Prints board 
	i = True
	for j in reversed(range(len(board))):
		for k in range(len(board[j])):
			if i==True: 
				sys.stdout.write('\033[47m\033[30m '+board[k][j][:-1]+' \033[0m')
			else:
				sys.stdout.write(" "+board[k][j][:-1]+" ")
			i=not i
		print ""
		i=not i

def setupPieces(board): # this is an init type function, sets up all the pieces on the board by calling them shortcode given on the board
	for x in range(len(board)):
		for y in range(len(board[x])):
			if board[x][y] != "   ":
				pieceDict[board[x][y]] = (pieces[board[x][y][1]])([x, y],int(board[x][y][0]))

def player(num):
	global fiftymoverule, quit, turn
	turn = int(not(turn-1))+1
	boardsave = ""
	for i in board:
		for j in i:
			boardsave += j
	threeboard.append(boardsave)
	if threeboard.count(boardsave) == 3:
		print "DRAW"
		print "Due to threefold repitition"
		quit = True
		return 1
	print "Player",num,"turn: \n\n"
	if check == int(num):
		print "you are in CHECK"
	while True:
		naturalInput = raw_input("Your move (standard chess notation):")
		result = decodeNotation(num,naturalInput)
		if result == 0:
			fiftymoverule += 1
			break
		else:
			print result
			if result == "That's checkmate" or result == "That's stalemate, BAHAHAHAHA":
				printBoard(board)
				quit = True
				break
	if fiftymoverule == 100:
		print "DRAW"
		print "There have been fifty moves without a pawn moving or a piece being taken"
		quit = True

board = [
["1R1","1p1","   ","   ","   ","   ","2p1","2R1"],
["1N1","1p2","   ","   ","   ","   ","2p2","2N1"],
["1B1","1p3","   ","   ","   ","   ","2p3","2B1"],
["1Q1","1p4","   ","   ","   ","   ","2p4","2Q1"],
["1K1","1p5","   ","   ","   ","   ","2p5","2K1"],
["1B2","1p6","   ","   ","   ","   ","2p6","2B2"],
["1N2","1p7","   ","   ","   ","   ","2p7","2N2"],
["1R2","1p8","   ","   ","   ","   ","2p8","2R2"]
]

fiftymoverule = 0
pieces = {'R':Rook,'N':Knight,'B':Bishop,'Q':Queen,'K':King, 'p':Pawn} # A dictionary for translating piece short codes to piece classes
piecenames = {'R':"Rook",'N':"Knight",'B':"Bishop",'Q':"Queen",'K':"King", 'p':"pawn"}
pieceDict = {}
colors = {1:'White',2:'Black'}
history = []
check = 0 
enpassant = [[0,0],0]
threeboard = []
takeenpassant = 0
turn = 1
#MAIN LOOP
quit = False
setupPieces(board)
while quit == False:
	printBoard(board)
	print fiftymoverule
	if turn == enpassant[1]:
		enpassant = [[0,0],0]
	player(str(turn))