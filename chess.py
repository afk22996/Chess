import pygame
import Piece
def drawBoard(screen, pieces):
	width = pygame.display.get_window_size()[0]
	height = pygame.display.get_window_size()[1]
	#draw board with the largest square possible for window size
	size = width/8
	if(width > height):
		size = height/8
	xoffset = 0
	yoffset = 0
	if(width > height):
		xoffset = (width-height)/2
	if(height > width):
		yoffset = (height-width)/2
	spaces = 8
	dark = (31,143,19)
	light = (254,255,232)
	wood = (115, 80, 0)
	screen.fill(wood)
	for i in range (0, spaces):
		for j in range (0, spaces):
			if((i+j)%2 == 0):
				#This is a light square
				pygame.draw.polygon(screen, light, ((i*size+xoffset, j*size+yoffset), (i*size+xoffset, (j+1)*size+yoffset), ((i+1)*size+xoffset, (j+1)*size+yoffset), ((i+1)*size+xoffset, j*size+yoffset)))
			else:
				#It must be a dark square
				pygame.draw.polygon(screen, dark, ((i*size+xoffset, j*size+yoffset), (i*size+xoffset, (j+1)*size+yoffset), ((i+1)*size+xoffset, (j+1)*size+yoffset), ((i+1)*size+xoffset, j*size+yoffset)))
	for piece in pieces:
		image = pygame.image.load(piece.getImage())
		position = piece.getPosition()
		image = pygame.transform.scale(image, (int(size), int(size)))
		screen.blit(image, position)
	pygame.display.update()

def generatePieces(screen, size):
	pieces = []
	kings = []
	#Generate Black Pieces
	
	#Rooks
	pieces.append(Piece.Rook(image = "BlackRook.png", position = (0,0), color = 1, name = "Rook"))
	pieces.append(Piece.Rook(image = "BlackRook.png", position = (size*7,0), color = 1, name = "Rook"))

	#Knights
	pieces.append(Piece.Knight(image = "BlackKnight.png", position = (size, 0), color = 1, name = "Knight"))
	pieces.append(Piece.Knight(image = "BlackKnight.png", position = (size*6, 0), color = 1, name = "Knight"))

	#Bishops
	pieces.append(Piece.Bishop(image = "BlackBishop.png", position = (2*size, 0), color = 1, name = "Bishop"))
	pieces.append(Piece.Bishop(image = "BlackBishop.png", position = (5*size, 0), color = 1, name = "Bishop"))

	#Queen
	pieces.append(Piece.Queen(image = "BlackQueen.png", position = (3*size, 0), color = 1, name = "Queen"))

	#King
	pieces.append(Piece.King(image = "BlackKing.png", position = (4*size, 0), color = 1, name = "King"))
	kings.append(Piece.King(image = "BlackKing.png", position = (4*size, 0), color = 1, name = "King"))

	#Pawns
	for i in range (0, 8):
		pieces.append(Piece.Pawn(position = (i*size, size), image = "BlackPawn.png", color = 1))

	#Generate White Pieces
	
	#Rooks
	pieces.append(Piece.Rook(image = "WhiteRook.png", position = (0,7*size), color = -1, name = "Rook"))
	pieces.append(Piece.Rook(image = "WhiteRook.png", position = (size*7,7*size), color = -1, name = "Rook"))

	#Knights
	pieces.append(Piece.Knight(image = "WhiteKnight.png", position = (size, 7*size), color = -1, name = "Knight"))
	pieces.append(Piece.Knight(image = "WhiteKnight.png", position = (size*6, 7*size), color = -1, name = "Knight"))

	#Bishops
	pieces.append(Piece.Bishop(image = "WhiteBishop.png", position = (2*size, 7*size), color = -1, name = "Bishop"))
	pieces.append(Piece.Bishop(image = "WhiteBishop.png", position = (5*size, 7*size), color = -1, name = "Bishop"))

	#Queen
	pieces.append(Piece.Queen(image = "WhiteQueen.png", position = (3*size, 7*size), color = -1, name = "Queen"))

	#King
	pieces.append(Piece.King(image = "WhiteKing.png", position = (4*size, 7*size), color = -1, name = "King"))
	kings.append(Piece.King(image = "WhiteKing.png", position = (4*size, 7*size), color = -1, name = "King"))


	#Pawns
	for i in range (0, 8):
		pieces.append(Piece.Pawn(position = (i*size, 6*size), image = "WhitePawn.png", color = -1))


	return (pieces, kings)

def main():
	turn = -1
	pygame.init()
	screen = pygame.display.set_mode((1024, 1024), pygame.RESIZABLE)
	running = True
	width = pygame.display.get_window_size()[0]
	height = pygame.display.get_window_size()[1]
	size = width/8
	if(width > height):
		size = height/8
	pieces = generatePieces(screen, size)[0]
	kings = generatePieces(screen, size)[1]
	drawBoard(screen, pieces)
	width = pygame.display.get_window_size()[0]
	height = pygame.display.get_window_size()[1]
	pygame.display.set_caption("Chess!")
	icon = pygame.image.load("BlackPawn.png")
	pygame.display.set_icon(icon)
	while running:
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.VIDEORESIZE:
				width = pygame.display.get_window_size()[0]
				height = pygame.display.get_window_size()[1]
				oldSize = width/8
				if(width > height):
					oldSize = height/8
				#User has resized the window, so the height and width need to be updated
				width = pygame.display.get_window_size()[0]
				height = pygame.display.get_window_size()[1]
				newScreen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
				newSize = width/8
				if(width > height):
					newSize = height/8
				newPieces = []
				xoffset = 0
				yoffset = 0
				if(width > height):
					xoffset = (width-height)/2
				if(height > width):
					yoffset = (height-width)/2
				for piece in pieces:
					oldPos = piece.getPosition()
					newPos = (oldPos[0]*(newSize/oldSize) + xoffset, oldPos[1]*(newSize/oldSize) + yoffset)
					newPieces.append(Piece.Piece(image = piece.getImage(), position = newPos, color = piece.getColor()))
					pieces = newPieces
				drawBoard(newScreen, newPieces)
			if event.type == pygame.MOUSEBUTTONDOWN:
				mousePOS = pygame.mouse.get_pos()
				for piece in pieces:
					piecePOS = piece.getPosition()
					if(mousePOS[0] >= piecePOS[0] and mousePOS[1] >= piecePOS[1]):
						if(mousePOS[0] - piecePOS[0] <= size and mousePOS[1] - piecePOS[1] <= size and piece.getColor() == turn):
							piece.clickPiece()
			if event.type == pygame.MOUSEBUTTONUP:
				for piece in pieces:
					if(piece.isClicked()):
						mousePOS = pygame.mouse.get_pos()
						previousPOS = piece.getPosition()
						piece.move(((int(mousePOS[0]/size))*size, (int(mousePOS[1]/size))*size), size, pieces)
						newPOS = piece.getPosition()
						if(previousPOS != newPOS):
							turn = -turn
						for otherPiece in pieces:
							if (otherPiece.getPosition() == piece.getPosition() and otherPiece != piece):
								pieces.remove(otherPiece)
						piece.unclick()

				for king in kings:
					king.isChecked(pieces, size)
				drawBoard(screen, pieces)


				

if __name__ == "__main__":
	main()