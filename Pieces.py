class Rook:
	def isLegal(move):
		if move[0] or move[1] =0:
			return 0
		else:
			return 1
class Bishop:
	def isLegal(move):
		if abs(move[0])==abs(move[1]):
			return 0
		else:
			return 1
class Knight:
	def isLegal(move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,2] or [2,1]:
			return 0
		else:
			return 1
class King:
	def isLegal(move):
		move = [abs(move[0]),abs(move[1])]
		if move == [1,0] or [0,1] or [1,1]:
			return 0
		else:
			return 1
class Queen:
	def isLegal(move):
		if Bishop.isLegal(move) or Rook.isLegal(move):
			return 0
		else:
			return 1
class Pawn:


	



		