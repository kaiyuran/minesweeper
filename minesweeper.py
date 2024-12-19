import pygame
import random
gridDimensions = int(input("Enter the grid dimensions(suggested 10): "))
# gridDimensions = 10
gridCellSize = 40

difficulty = input("Enter the difficulty (easy(e), medium(m), hard(h): ")

if difficulty == "e":
    numBombs = int(gridDimensions ** 2 // 5)
elif difficulty == "m":
    numBombs = int(gridDimensions ** 2 // 4.5)
else:
    numBombs = int(gridDimensions ** 2 // 3.5)

numFlags = numBombs
usedFlags = 0
userClickGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]
flagGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]
clickGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]
bombGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]

pygame.init()
pygame.font.init()
window = pygame.display.set_mode((gridDimensions * gridCellSize, gridDimensions * gridCellSize+40))
clock = pygame.time.Clock()
boxFont = pygame.font.SysFont('Comic Sans MS', 30)
endFont = pygame.font.SysFont('Comic Sans MS', 30)
uiFont = pygame.font.SysFont('Comic Sans MS', 20)
bombImg = pygame.image.load('res/bomb.png')
flagImg = pygame.image.load('res/flag.png')






gameOver = False
win = False
clickedBomb = False

def generateMap(dimensions, startPoint, numBombs = 10):
    grid = [[False for x in range(dimensions)] for y in range(dimensions)]
    numBombsPlaced = 0
    while numBombsPlaced < numBombs:
        x = random.randint(0, dimensions-1)
        y = random.randint(0, dimensions-1)
        if not grid[y][x] and (y, x) != startPoint:
            grid[y][x] = True
            numBombsPlaced += 1
    # print(grid)
    return grid
    
def checkFlags(flagGrid, bombGrid):
    for yLoc, rowOfCells in enumerate(flagGrid):
        for xLoc, cell in enumerate(rowOfCells):
            if cell:
                if bombGrid[yLoc][xLoc]:
                    flagGrid[yLoc][xLoc] = False
    return flagGrid

def checkCell(position, bombGrid):
    positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    bombsCount = 0
    for pos in positions:
        try:
            if bombGrid[position[0]+pos[0]][position[1]+pos[1]] and position[0]+pos[0] >= 0 and position[1]+pos[1] >= 0 and position[0]+pos[0] < len(bombGrid) and position[1]+pos[1] < len(bombGrid[1]):
                bombsCount += 1
        except:
            pass
    return bombsCount


def expand(clickGrid, bombGrid, flagGrid, position):
    positions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    possiblePositions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    expansionPositions = [position]
    for pos in expansionPositions:
        try:
            for deltaPos in positions:
                if bombGrid[pos[0]+deltaPos[0]][pos[1]+deltaPos[1]] == False and flagGrid[pos[0]+deltaPos[0]][pos[1]+deltaPos[1]] == False and checkCell([pos[0]+deltaPos[0], pos[1]+deltaPos[1]], bombGrid) == 0:
                    clickGrid[pos[0]+deltaPos[0]][pos[1]+deltaPos[1]] = True
                    if [pos[0]+deltaPos[0], pos[1]+deltaPos[1]] not in expansionPositions:
                        expansionPositions.append([pos[0]+deltaPos[0], pos[1]+deltaPos[1]])
        except:
            pass
    for pos in expansionPositions:
        for deltaPos in possiblePositions:
            if pos[0]+deltaPos[0] >= 0 and pos[1]+deltaPos[1] >= 0 and pos[0]+deltaPos[0] < len(bombGrid) and pos[1]+deltaPos[1] < len(bombGrid[1]):
                if bombGrid[pos[0]+deltaPos[0]][pos[1]+deltaPos[1]] == False and flagGrid[pos[0]+deltaPos[0]][pos[1]+deltaPos[1]] == False:
                    clickGrid[pos[0]+deltaPos[0]][pos[1]+deltaPos[1]] = True

    for pos in expansionPositions:
        clickGrid[pos[0]][pos[1]] = True
    return clickGrid


firstClickDone = False
run = True
while run:
    clock.tick(60)

    flagsLeft = numFlags - usedFlags


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if not gameOver:
            if event.type == pygame.MOUSEBUTTONDOWN:    #1=left, 2=middle, 3=right
                try:
                    row = event.pos[1] // gridCellSize
                    col = event.pos[0] // gridCellSize
                    # print(event.button)
                    if not firstClickDone:
                        bombGrid = generateMap(gridDimensions, (row, col), numBombs)
                        firstClickDone = True


                    if event.button == 1 and not flagGrid[row][col]:
                        clickGrid[row][col] = True
                        userClickGrid[row][col] = True
                        if not bombGrid[row][col] and checkCell([row, col], bombGrid) == 0:
                            clickGrid = expand(clickGrid, bombGrid, flagGrid, [row, col])
                            # userClickGrid = expand(userClickGrid, bombGrid, flagGrid, [row, col])



                    elif event.button == 3 and not clickGrid[row][col]:

                        if not flagGrid[row][col] and flagsLeft > 0:
                            flagGrid[row][col] = not flagGrid[row][col]
                        elif flagGrid[row][col]:
                            flagGrid[row][col] = not flagGrid[row][col]


                        usedFlags = 0
                        for yLoc, rowOfCells in enumerate(flagGrid):
                            for xLoc, cell in enumerate(rowOfCells):
                                if cell:
                                    usedFlags += 1
                        # print("flags left:", (numFlags - usedFlags))
                        
                        

                    elif event.button == 2:
                        # flagGrid = checkFlags(flagGrid, bombGrid)
                        clickGrid = [[True for x in range(gridDimensions)] for y in range(gridDimensions)]
                except:
                    pass
        
    if gameOver:
        for yPos, y in enumerate(flagGrid):
            for xPos, x in enumerate(y):
                if not bombGrid[yPos][xPos]:
                    flagGrid[yPos][xPos] = False        

        for yPos, y in enumerate(flagGrid):
            for xPos, x in enumerate(y):
                clickGrid[yPos][xPos] = not x

    window.fill('green')
    for yLoc, rowOfCells in enumerate(clickGrid):
        for xLoc, cell in enumerate(rowOfCells):
            colour = "#1cef09"
            boxText = boxFont.render("", False, "#000000")
            if cell == True:
                if bombGrid[yLoc][xLoc]:
                    # print("bomb clicked")
                    # colour = "#ff0000"
                    # window.blit(bombImg, (xLoc*gridCellSize+1, yLoc*gridCellSize+1))
                    gameOver = True
                    
                else:
                    colour = "#1bafc6"
                    boxText = boxFont.render(str(checkCell([yLoc,xLoc], bombGrid)), False, "#000000")
                    

                # colour = "#1bafc6"
            cell_rect = pygame.Rect(xLoc*gridCellSize+1, yLoc*gridCellSize+1, gridCellSize-2, gridCellSize-2)
            pygame.draw.rect(window, colour, cell_rect)
            window.blit(boxText, (xLoc*gridCellSize+1, yLoc*gridCellSize+1))

    if gameOver:
        for yLoc, rowOfCells in enumerate(bombGrid):
            for xLoc, cell in enumerate(rowOfCells):
                if cell:
                    window.blit(bombImg, (xLoc*gridCellSize+1, yLoc*gridCellSize+1))

    for yLoc, rowOfCells in enumerate(flagGrid):
        for xLoc, cell in enumerate(rowOfCells):
            if cell:
                cell_rect = pygame.Rect(xLoc*gridCellSize+1, yLoc*gridCellSize+1, gridCellSize-2, gridCellSize-2)
                # pygame.draw.rect(window, "#fe7700", cell_rect)
                window.blit(flagImg, (xLoc*gridCellSize+1, yLoc*gridCellSize+1))

    checkGameOver = True
    for yLoc in range(gridDimensions):
            # print(clickGrid[yLoc][xLoc], bombGrid[yLoc][xLoc])
            if not clickGrid[yLoc][xLoc] and not bombGrid[yLoc][xLoc]:
                checkGameOver = False
    if checkGameOver:
        gameOver = True


    # win = True
    # print(clickGrid)
    # print(bombGrid)
    for yLoc, rowOfCells in enumerate(bombGrid):
        for xLoc, cell in enumerate(rowOfCells):
            if cell and userClickGrid[yLoc][xLoc]:
                clickedBomb = True
                break
    
    #ui
    window.blit(flagImg, (0, gridDimensions * gridCellSize + 5))
    
    flagsText = uiFont.render("= " + str(flagsLeft), False, "#000000")
    window.blit(flagsText, (50, gridDimensions * gridCellSize + 5))

    if gameOver:
        if not clickedBomb:
            # print("You Win!")
            endText = endFont.render("You Win!", False, "#00ff00", "#000000")
        else:
            # print("Game Over")
            endText = endFont.render("Game Over", False, "#ff0000", "#000000")
        window.blit(endText, (gridDimensions * gridCellSize // 2 - 70 , gridDimensions * gridCellSize ))

    pygame.display.flip()

pygame.quit()
exit()