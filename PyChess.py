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
	pmove[0] = posTo[0]-posFrom[0]
	pmove[1] = posTo[1]-posFrom[1]
	if "r" in piece:
		return checkPlus(posFrom,posTo,pmove,board)

def checkingLoop(axis,pmove,posFrom):
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
		print "movement is not in a straight line"
		return 1
	if (pmove[1] == 0): 
		return checkingLoop(0,pmove,posFrom)
	else:
		return checkingLoop(1,pmove,posFrom)

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

def player(board, num):
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
["Br","Bn","Bb","BQ","BK","Bb","Bn","Br"],	# W means player 1
["Bp","Bp","Bp","Bp","Bp","Bp","Bp","Bp"],	# I changed bishops and knights the right way round
["  ","  ","  ","  ","  ","  ","  ","  "],	# n = Knights, as in normal chess notation, "N"
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["  ","  ","  ","  ","  ","  ","  ","  "],
["Wp","Wp","Wp","Wp","Wp","Wp","Wp","Wp"],
["Wr","Wn","Wb","WQ","WK","Wb","Wn","Wr"],
]

#MAIN LOOP
quit = False
while quit == False:
	printBoard(board)		# Print
	player(board, 1)		# Player 1
	printBoard(board)		# Print
	player(board, 2)		# Player 2