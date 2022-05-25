import math
class Piece:
	def __init__(self, position, image, color, name):
		self.position = position
		self.image = image
		self.clicked = False
		self.color = color
		self.name = name
		return

	def __eq__(self, piece):
		print(self.getPosition() == piece.getPosition() and self.getName() == piece.getName() and self.getColor() == piece.getColor())
		return(self.getPosition() == piece.getPosition() and self.getName() == piece.getName() and self.getColor() == piece.getColor())

	def __ne__(self, piece):
		return (not self.__eq__(piece))

	def getColor(self):
		return self.color
	def getPosition(self):
		return self.position
	def getName(self):
		return self.name
	def getImage(self):
		return self.image

	def clickPiece(self):
		self.clicked = True

	def isClicked(self):
		return self.clicked

	def updatePosition(self, position):
		self.position = position

	def unclick(self):
		self.clicked = False

	def move(self, position, size, pieces):
		pass

class Pawn(Piece):

	def __init__ (self, position, image, color, name = "Pawn"):
		self.image = image
		self.position = position
		self.clicked = False
		self.firstMove = True
		self.color = color
		self.enPassante = False
		self.name = "Pawn"

	def getName(self):
		return self.name

	def getEnPassante(self):
		return self.enPassante

	def setEnPassante(self):
		self.enPassante = False

	def move(self, position, size, pieces):

		#Impossible moves for a pawn
		if(abs(position[0] - self.position[0]) > size or self.color*(position[1] - self.position[1]) > 2*size):
			return
		
		#Attempt to capture
		if(abs(position[0] - self.position[0]) == size and self.color*(position[1] - self.position[1]) > 0):
			for piece in pieces:
				#En Passante
				if(piece.getName() == "Pawn"):
					if(abs(piece.getPosition()[0] - position[0]) == 0 and self.color*(piece.getPosition()[1] - position[1]) == -size  and piece.getEnPassante()):
						self.firstMove = False
						self.updatePosition(position)
						break

				#Normal Capture
				if (piece.getPosition() == position and piece != self and piece.color != self.color):
					for piece in pieces:
						if(piece.getName() == "Pawn"):
							if(piece.getEnPassante()):
								piece.setEnPassante()
					self.firstMove = False
					self.updatePosition(position)
					return
			return

		#Moving 2 squares on first move
		if(self.color*(position[1] - self.position[1]) == 2*size and self.firstMove):
			for piece in pieces:
				if(piece.getName() == "Pawn"):
					if(piece.getEnPassante()):
						piece.setEnPassante()
				if(piece.getPosition() == position and piece != self):
					return
			self.enPassante = True
			self.firstMove = False
			self.updatePosition(position)
			return
		
		#Normal 1 square move
		if(self.color*(position[1] - self.position[1]) == size):
			for piece in pieces:
				if(piece.getName() == "Pawn"):
					if(piece.getEnPassante()):
						piece.setEnPassante()
				if(piece.getPosition() == position and piece != self):
					return
			self.firstMove = False
			self.updatePosition(position)
			return
	
class Rook(Piece):
	def move(self, position, size, pieces):
		#Don't allow illegal moves
		if(self.position[0] != position[0] and self.position[1] != position[1]):
			return

		#Check if something is in the way
		for i in range(int(self.position[0]/size), int(position[0]/size)):
			for piece in pieces:
				if(piece.getPosition() == (i*size, int(position[1])) and piece != self):
					#print ("illegal move")
					return

		for i in range(int(position[0]/size)+1, int(self.position[0]/size)):
			for piece in pieces:
				if(piece.getPosition() == (i*size, int(position[1])) and piece != self):
					#print ("illegal move")
					return

		for i in range(int(self.position[1]/size), int(position[1]/size)):
			for piece in pieces:
				if(piece.getPosition() == (int(position[0]), i*size) and piece != self):
					#print ("illegal move")
					return

		for i in range(int(position[1]/size)+1, int(self.position[1]/size)):
			for piece in pieces:
				if(piece.getPosition() == (int(position[0]), i*size) and piece != self):
					#print ("illegal move")
					return

		for piece in pieces:
			if(piece.position == position and self.color == piece.getColor()):
				return

		#Move the piece
		self.updatePosition(position)
		return

class Knight(Piece):
	def move(self, position, size, pieces):
		#Don't allow illegal moves
		if((abs(position[0] - self.position[0]) != size and abs(position[1] - self.position[1]) != size) or (abs(position[0] - self.position[0]) != 2*size and abs(position[1] - self.position[1]) != 2*size)):
			#print("ILLEGAL")
			return
		for piece in pieces:
			if(piece.position == position and self.color == piece.getColor()):
				return
		#Move the piece
		self.updatePosition(position)
		return

class Bishop(Piece):
	def move(self, position, size, pieces):
		#This piece was terrible to try to program so this is probably unreadable, sorry future me
		if(self.position[0] == position[0] or self.position[1] == position[1]):
			return
		#Calculating which direction in the x and y the piece is travelling
		signX = -(self.position[0] - position[0])/abs(self.position[0] - position[0])
		signY = -(self.position[1] - position[1])/abs(self.position[1] - position[1])
		#Calculating the path length
		path = int(max(abs(self.position[0] - position[0]), abs(self.position[1] - position[1]))/size)
		for k in range(0, path+1):
			#Checking to make sure that there isn't a piece in the way that cannot be taken
			for piece in pieces:
				if(signX*k + self.position[0]/size == piece.getPosition()[0]/size and signY*k+ self.position[1]/size == piece.getPosition()[1]/size and piece != self):
					if(k == path and self.color != piece.getColor()):
						continue
					return
			#Making sure that the desired position lies in the correct diagonal
			if((position[0]/size - (signX*k + self.position[0]/size) == 0 and position[1]/size - (signY*k+ self.position[1]/size) == 0)):
				self.updatePosition(position)
				continue
		return

class Queen(Piece):
	def moveDiagonally(self, position, size, pieces):
		#This piece was terrible to try to program so this is probably unreadable, sorry future me
		if(self.position[0] == position[0] or self.position[1] == position[1]):
			return
		#Calculating which direction in the x and y the piece is travelling
		signX = -(self.position[0] - position[0])/abs(self.position[0] - position[0])
		signY = -(self.position[1] - position[1])/abs(self.position[1] - position[1])
		#Calculating the path length
		path = int(max(abs(self.position[0] - position[0]), abs(self.position[1] - position[1]))/size)
		for k in range(0, path+1):
			#Checking to make sure that there isn't a piece in the way that cannot be taken
			for piece in pieces:
				if(signX*k + self.position[0]/size == piece.getPosition()[0]/size and signY*k+ self.position[1]/size == piece.getPosition()[1]/size and piece != self):
					if(k == path and self.color != piece.getColor()):
						continue
					return
			#Making sure that the desired position lies in the correct diagonal
			if((position[0]/size - (signX*k + self.position[0]/size) == 0 and position[1]/size - (signY*k+ self.position[1]/size) == 0)):
				self.updatePosition(position)
				continue
		return

	def moveVertially(self, position, size, pieces):
		#Don't allow illegal moves
		if(self.position[0] != position[0] and self.position[1] != position[1]):
			return

		#Check if something is in the way
		for i in range(int(self.position[0]/size), int(position[0]/size)):
			for piece in pieces:
				if(piece.getPosition() == (i*size, int(position[1])) and piece != self):
					#print ("illegal move")
					return

		for i in range(int(position[0]/size)+1, int(self.position[0]/size)):
			for piece in pieces:
				if(piece.getPosition() == (i*size, int(position[1])) and piece != self):
					#print ("illegal move")
					return

		for i in range(int(self.position[1]/size), int(position[1]/size)):
			for piece in pieces:
				if(piece.getPosition() == (int(position[0]), i*size) and piece != self):
					#print ("illegal move")
					return

		for i in range(int(position[1]/size)+1, int(self.position[1]/size)):
			for piece in pieces:
				if(piece.getPosition() == (int(position[0]), i*size) and piece != self):
					#print ("illegal move")
					return#

		for piece in pieces:
			if(piece.position == position and self.color == piece.getColor()):
				return

		#Move the piece
		self.updatePosition(position)
		return
	def move(self, position, size, pieces):
		self.moveDiagonally(position, size, pieces)
		self.moveVertially(position, size, pieces)
		return


class King:

	def __init__(self, position, image, color, name, isChecked = False):
		self.position = position
		self.image = image
		self.clicked = False
		self.color = color
		self.name = name
		return

	def getColor(self):
		return self.color
	def getPosition(self):
		return self.position
	
	def getName(self):
		return self.name

	def getImage(self):
		return self.image

	def clickPiece(self):
		self.clicked = True

	def isClicked(self):
		return self.clicked

	def updatePosition(self, position):
		self.position = position

	def unclick(self):
		self.clicked = False

	def getName(self):
		pass

	def check(self):
		self.isChecked = True

	def uncheck(self):
		self.isChecked = False

	def isChecked(self, pieces, size):
		for piece in pieces:
			print(piece == self)
			if(piece != self):
				tempPosition = piece.getPosition()
				tempColor = piece.getColor()
				tempName = piece.getName()
				evalString = "(" + str(tempPosition) + ", None" + "," + str(tempColor) + "," + str(tempName) + ")"
				tempPiece = eval(tempName +  evalString)
				tempPieces = []
				for piece in pieces:
					if (piece!= tempPiece):
						tempPieces.append(piece)
				tempPieces.append(tempPiece)
				tempPiece.move(self.getPosition(), size, tempPieces)
				if (tempPiece.getPosition() == self.getPosition()):
					return True
		return False


	def getName(self):
		return self.name

	def move(self, position, size, pieces):
		if(abs(self.position[0] - position[0])/size > 1 or abs(self.position[1] - position[1])/size > 1):
			return
		for piece in pieces:
			if(piece.getPosition() == position and piece.getColor() == self.color):
				return
		self.updatePosition(position)
		return