import pygame
import random
import time

# gridDimensions = int(input("Enter the grid dimensions(suggested 10): "))
gridDimensions = 5
gridCellSize = 30
numApples = 40
speed = 3
# numApples = int(input("Enter the number of apples(suggested 5): "))

# snakePos = [[gridDimensions//2, gridDimensions//2], [(gridDimensions//2)-1, (gridDimensions//2)]]
snakePos = [[0,0], [1,0]]
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

appleImg = pygame.image.load('res/snake/apple.png')

#heads
headLeftImg = pygame.image.load('res/snake/snakeHead.png')
headDownImg = pygame.transform.rotate(headLeftImg, 90)
headRightImg = pygame.transform.flip(headLeftImg, True, False)
headUpImg = pygame.transform.rotate(headRightImg, 90)




#bodies
bodyHorizontalImg = pygame.image.load('res/snake/snakeStraight.png')
bodyVerticalImg = pygame.transform.rotate(bodyHorizontalImg, 90)

#tails
tailRightImg = pygame.image.load('res/snake/snakeTail.png')
tailUpImg = pygame.transform.rotate(tailRightImg, 90)
tailLeftImg = pygame.transform.rotate(tailUpImg, 90)
tailDownImg = pygame.transform.rotate(tailLeftImg, 90)
#curves
curveAImg = pygame.image.load('res/snake/snakeCurve.png')
curveBImg = pygame.transform.rotate(curveAImg, 90)
curveDImg = pygame.transform.rotate(curveBImg, 90)
curveCImg = pygame.transform.rotate(curveDImg, 90)



gameStart = False
gameOver = False
win = False

def makeApple(snakePos, gridDimensions, applesList):
    global gameOver
    global win
    done = False
    # print(len(applesList) - (gridDimensions ** 2 - len(snakePos)))
    if gridDimensions ** 2 - len(applesList) - len(snakePos) < 1:
        # print("You Win!")
        # gameOver = True
        # win = True
        return [-5,-5]

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

    # print(newHead)
    # print(applesList)
    if newHead not in applesList:
        snakePos.pop()
    else:
        applesList.remove(newHead)
        applesList.append(makeApple(snakePos, gridDimensions, applesList))

    return snakePos, applesList
    
def getDirection(snakePosback, curSnakePos, snakePosfront): #return up, down, curveup, curvedown, 
    back = [snakePosback[0] - curSnakePos[0], snakePosback[1] - curSnakePos[1]]
    front = [snakePosfront[0] - curSnakePos[0], snakePosfront[1] - curSnakePos[1]]

    if back[0] == front[0]:
        return "vertical"
    if back[1] == front[1]:
        return "horizontal"
    
    # curveAList = [[0,-1], [1,0]]
    # curveBList = [[0,1], [-1,0]]
    # curveCList = [[0,-1], [-1,0]]
    # curveDList = [[0,1], [1,0]]

    curveAList = [[0,1], [-1,0]]
    curveBList = [[0,1], [1,0]]
    curveCList = [[0,-1], [-1,0]]
    curveDList = [[0,-1], [1,0]]

    if back in curveAList and front in curveAList:
        return "ca"
    if back in curveBList and front in curveBList:
        return "cb"
    if back in curveCList and front in curveCList:
        return "cc"
    if back in curveDList and front in curveDList:
        return "cd"
    






for x in range(numApples):
    applesList.append(makeApple(snakePos, gridDimensions, applesList))


nextDir = "r"
curDir = "r"
run = True
while run:
    clock.tick(speed)

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




    # window.blit(tailLeftImg, (0,0))
    # window.blit(tailDownImg, (40,0))
    # window.blit(tailRightImg, (80,0))
    # window.blit(tailUpImg, (120,0))

    # window.blit(bodyHorizontalImg, (0,0))
    # window.blit(bodyVerticalImg, (40,0))
    # window.blit(curveAImg, (80,0))
    # window.blit(curveBImg, (120,0))
    # window.blit(curveCImg, (160,0))
    # window.blit(curveDImg, (200,0))

    #body
    for num, pos in enumerate(snakePos):
        if num !=0 and pos != snakePos[-1]:
            direction = getDirection(snakePos[num-1], pos, snakePos[num+1])

            if direction == "horizontal":
                window.blit(bodyHorizontalImg, (pos[0]*gridCellSize, pos[1]*gridCellSize))
            
            elif direction == "vertical":
                window.blit(bodyVerticalImg, (pos[0]*gridCellSize, pos[1]*gridCellSize))
            
            elif direction == "ca":
                window.blit(curveAImg, (pos[0]*gridCellSize, pos[1]*gridCellSize))

            elif direction == "cb":
                window.blit(curveBImg, (pos[0]*gridCellSize, pos[1]*gridCellSize))

            elif direction == "cc":
                window.blit(curveCImg, (pos[0]*gridCellSize, pos[1]*gridCellSize))

            elif direction == "cd":
                window.blit(curveDImg, (pos[0]*gridCellSize, pos[1]*gridCellSize))



    #tail
    tailDif = [snakePos[-2][0] - snakePos[-1][0], snakePos[-2][1] - snakePos[-1][1]]
    if tailDif == [1, 0]:
        window.blit(tailRightImg, (snakePos[-1][0]*gridCellSize, snakePos[-1][1]*gridCellSize))

    if tailDif == [-1, 0]:
        window.blit(tailLeftImg, (snakePos[-1][0]*gridCellSize, snakePos[-1][1]*gridCellSize))

    if tailDif == [0, 1]:
        window.blit(tailDownImg, (snakePos[-1][0]*gridCellSize, snakePos[-1][1]*gridCellSize))

    if tailDif == [0, -1]:
        window.blit(tailUpImg, (snakePos[-1][0]*gridCellSize, snakePos[-1][1]*gridCellSize))

    #head

    headDif = [snakePos[1][0] - snakePos[0][0], snakePos[1][1] - snakePos[0][1]]
    if headDif == [-1, 0]:
        window.blit(headRightImg, (snakePos[0][0]*gridCellSize, snakePos[0][1]*gridCellSize))
        # print("right")

    if headDif == [1, 0]:
        window.blit(headLeftImg, (snakePos[0][0]*gridCellSize, snakePos[0][1]*gridCellSize))
        # print("left")

    if headDif == [0, -1]:
        window.blit(headDownImg, (snakePos[0][0]*gridCellSize, snakePos[0][1]*gridCellSize))
        # print("down")

    if headDif == [0, 1]:
        window.blit(headUpImg, (snakePos[0][0]*gridCellSize, snakePos[0][1]*gridCellSize))
        # print("up")


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