import pygame
import random
import time

gridDimensions = int(input("Enter the grid dimensions(suggested 10): "))
# gridDimensions = 10
gridCellSize = 30
# numApples = 2
numApples = int(input("Enter the number of apples(suggested 5): "))

snakePos = [[gridDimensions//2, gridDimensions//2], [(gridDimensions//2)-1, (gridDimensions//2)]]
snakeGrid = [[False for x in range(gridDimensions)] for y in range(gridDimensions)]
applesList = []



start = time.time()
endTime = time.time()

pygame.init()
pygame.font.init()
window = pygame.display.set_mode((gridDimensions * gridCellSize, gridDimensions * gridCellSize+40))
clock = pygame.time.Clock()
boxFont = pygame.font.SysFont('Comic Sans MS', 30)
endFont = pygame.font.SysFont('Comic Sans MS', 30)
uiFont = pygame.font.SysFont('Comic Sans MS', 20)

appleImg = pygame.image.load('res/apple.png')


gameStart = False
gameOver = False
win = False

def makeApple(snakePos, gridDimensions, applesList):
    global gameOver
    global win
    done = False
    print(len(applesList) - (gridDimensions ** 2 - len(snakePos)))
    if len(applesList) - (gridDimensions ** 2 - len(snakePos)) == 0:
        print("You Win!")
        gameOver = True
        win = True
        return [gridDimensions, gridDimensions]

    while not done:
        apple = [random.randint(0, gridDimensions-1), random.randint(0, gridDimensions-1)]
        if apple not in snakePos and apple not in applesList:
            done = True
    return apple

def checkDir(curDir, nextDir):
    wrongDirs = [["l", "r"], ["r", "l"], ["u", "d"], ["d", "u"]]
    if [curDir, nextDir] in wrongDirs:
        return curDir
    return nextDir

def checkCollision(snakePos, gridDimensions):
    # gridDimensions += 1
    if snakePos[0][0] < 0 or snakePos[0][0] >= gridDimensions or snakePos[0][1] < 0 or snakePos[0][1] >= gridDimensions:
        return True
    if snakePos[0] in snakePos[1:]:
        return True
    return False

def moveSnake(snakePos, direction, applesList):
    if direction == "l":
        newHead = [snakePos[0][0]-1, snakePos[0][1]]
    if direction == "r":
        newHead = [snakePos[0][0]+1, snakePos[0][1]]
    if direction == "u":
        newHead = [snakePos[0][0], snakePos[0][1]-1]
    if direction == "d":
        newHead = [snakePos[0][0], snakePos[0][1]+1]
    snakePos.insert(0, newHead)

    print(newHead)
    print(applesList)
    if newHead not in applesList:
        snakePos.pop()
    else:
        applesList.remove(newHead)
        applesList.append(makeApple(snakePos, gridDimensions, applesList))

    return snakePos, applesList
    

for x in range(numApples):
    applesList.append(makeApple(snakePos, gridDimensions, applesList))


nextDir = "r"
curDir = "r"
run = True
while run:
    clock.tick(4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        
            if not gameOver:
                if event.key == pygame.K_LEFT:
                    nextDir = "l"
                    gameStart = True
                    # print("left")
                if event.key == pygame.K_RIGHT:
                    nextDir = "r"
                    gameStart = True
                    # print("right")
                if event.key == pygame.K_UP:
                    nextDir = "u"
                    gameStart = True
                    # print("up")
                if event.key == pygame.K_DOWN:
                    nextDir = "d"
                    
                    # print("down")


    window.fill('white')
    # print(curDir, nextDir)
    nextDir = checkDir(curDir, nextDir)
    curDir = str(nextDir)

    if not gameStart:
        start = time.time()


    for x in range(gridDimensions):
        for y in range(gridDimensions):
            cell_rect = pygame.Rect(x*gridCellSize, y*gridCellSize, gridCellSize, gridCellSize)
            pygame.draw.rect(window, "black", cell_rect)



    for apple in applesList:
        cell_rect = pygame.Rect(apple[0]*gridCellSize, apple[1]*gridCellSize+1, gridCellSize-2, gridCellSize-2)
        # pygame.draw.rect(window, "red", cell_rect)
        window.blit(appleImg, (apple[0]*gridCellSize, apple[1]*gridCellSize))

    for pos in snakePos:
        cell_rect = pygame.Rect(pos[0]*gridCellSize, pos[1]*gridCellSize+1, gridCellSize-2, gridCellSize-2)
        pygame.draw.rect(window, "green", cell_rect)


    if not gameOver and gameStart:
        snakePos, applesList = moveSnake(snakePos, nextDir, applesList)

    if len(snakePos) == gridDimensions ** 2:
        gameOver = True
        win = True

    if checkCollision(snakePos, gridDimensions):
        gameOver = True
        win = False





    #ui
    if not gameOver: #timer
        endTime = time.time()
    timeText = uiFont.render("Time: " + str(round(endTime - start, 2)), False, "#000000")
    window.blit(timeText, (gridDimensions * gridCellSize - 100, gridDimensions * gridCellSize + 5))

    if gameOver:
        if win:
            # print("You Win!")
            endText = endFont.render("You Win!", False, "#00ff00", "#000000")
        else:
            # print("Game Over")
            endText = endFont.render("Game Over", False, "#ff0000", "#000000")
        window.blit(endText, (gridDimensions * gridCellSize // 2 - 70 , gridDimensions * gridCellSize ))

    pygame.display.flip()

pygame.quit()
exit()