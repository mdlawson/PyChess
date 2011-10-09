import sys
import os
from string import replace
from termcolor import colored

def letterToNum(str):
	out = replace(str, "W","1")
	return replace(out, "B","2")
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
	pmove[0] = abs(posTo[0]-posFrom[0])
	pmove[1] = abs(posTo[1]-posFrom[1])
	if "r" in piece:
		return checkPlus(posFrom,posTo,pmove,board)

def checkingLoop(dist, yfunc, xfunc, posy, posx):
	for i in range(dist):
		if board[posy+eval(yfunc)][posx+eval(xfunc)] != "  ":
			print "there is a piece in the way!"
			return 1
	
def checkPlus(posFrom,posTo,pmove,board):
	if (pmove[0] != 0) and (pmove[1] != 0):
		print "movement is not in a straight line"
		return 1
	if (pmove[1] == 0): 
		return checkingLoop(pmove[0],"0","+i+1",posFrom[1],posFrom[0])
	else:
		return checkingLoop(pmove[1],"+i+1","0",posFrom[0],posFrom[1])

def checkCross(posFrom,posTo,pmove,board):
	if abs(pmove[0])!=abs(pmove[1]):
		print "movement is not in a diagonal line"
		return 1
	for i in range(pmove[0]):
		if board[posFrom[0]+i+1][posFrom[1]+i+1] != "  ":
			print "there is a piece in the way!"
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

def player(board, num):	# I made this bloody difficult but there are no bugs whatsoever so I'm happy
	print "Player",num,"turn: \n\n"
	while True:
		while True:
			fromCoord = chessToCoord(raw_input("Enter the piece you want to move: "))
			if edgeDetect(fromCoord[0], fromCoord[1]) == 0:
				piece = board[fromCoord[1]][fromCoord[0]]
				print "Piece selected:",piece
				if str(num) in letterToNum(piece):
					break
				else: 
					print "Invalid piece!"
		toCoord = chessToCoord(raw_input("Enter the destination to move to: "))
		if edgeDetect(toCoord[0],toCoord[1]) == 0:
			if str(num) in letterToNum(board[toCoord[1]][toCoord[0]]):
				print "You cant take your own pieces!"
			elif checkLegal(fromCoord,toCoord, board, piece) == 1:
				print "Ilegal move!"
			else: 
				break
	move(fromCoord,toCoord) 
board = [									# This is the original board
["Wr","Wn","Wb","WK","WQ","Wb","Wn","Wr"],	# W means player 1
["Wp","Wp","Wp","Wp","Wp","Wp","Wp","Wp"],	# I changed bishops and knights the right way round
["  ","  ","  ","  ","  ","  ","  ","  "],	# n = Knights, as in normal chess notation, "N"
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["Bp","Bp","Bp","Bp","Bp","Bp","Bp","Bp"],
["Br","Bn","Bb","BK","BQ","Bb","Bn","Br"],
]

#MAIN LOOP
quit = False
while quit == False:
	printBoard(board)		# Print
	player(board, 1)		# Player 1
	printBoard(board)		# Print
	player(board, 2)		# Player 2