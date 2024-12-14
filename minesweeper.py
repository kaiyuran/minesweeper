#idea of classes from 

import pygame
import random
gridDimensions = 10
gridCellSize = 40

numBombs = 10
numFlags = gridDimensions ** 2 - numBombs
flagGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]
clickGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]
bombGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]

pygame.init()
window = pygame.display.set_mode((10 * gridCellSize, 10 * gridCellSize))
clock = pygame.time.Clock()

def generateMap(dimensions, startPoint, numBombs = 10):
    grid = [[False for x in range(dimensions)] for y in range(dimensions)]
    numBombsPlaced = 0
    while numBombsPlaced < numBombs:
        x = random.randint(0, dimensions-1)
        y = random.randint(0, dimensions-1)
        if not grid[y][x] and (y, x) != startPoint:
            grid[y][x] = True
            numBombsPlaced += 1
    print(grid)
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
            if not bombGrid[position[0]+pos[0]][position[1]+pos[1]]:
                bombsCount += 1
        except:
            pass
    return bombsCount



firstClickDone = False
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:    #1=left, 2=middle, 3=right
            row = event.pos[1] // gridCellSize
            col = event.pos[0] // gridCellSize
            if not firstClickDone:
                bombGrid = generateMap(gridDimensions, (row, col), numBombs)
                firstClickDone = True


            if event.button == 1 and not flagGrid[row][col]:
                clickGrid[row][col] = True
                


            elif event.button == 3 and not clickGrid[row][col]:
                flagGrid[row][col] = not flagGrid[row][col]
                
                

            else:
                flagGrid = checkFlags(flagGrid, bombGrid)
                clickGrid = [[True for x in range(gridDimensions)] for y in range(gridDimensions)]


    window.fill('green')
    for yLoc, rowOfCells in enumerate(clickGrid):
        for xLoc, cell in enumerate(rowOfCells):
            colour = "#1cef09"
            if cell == True:
                if bombGrid[yLoc][xLoc]:
                    colour = "#ff0000"
                else:
                    colour = "#1bafc6"
                # colour = "#1bafc6"
            cell_rect = pygame.Rect(xLoc*gridCellSize+1, yLoc*gridCellSize+1, gridCellSize-2, gridCellSize-2)
            pygame.draw.rect(window, colour, cell_rect)

    for yLoc, rowOfCells in enumerate(flagGrid):
        for xLoc, cell in enumerate(rowOfCells):
            if cell:
                cell_rect = pygame.Rect(xLoc*gridCellSize+1, yLoc*gridCellSize+1, gridCellSize-2, gridCellSize-2)
                pygame.draw.rect(window, "#fe7700", cell_rect)

    pygame.display.flip()



pygame.quit()
exit()