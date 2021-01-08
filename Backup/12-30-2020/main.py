import tkinter
import pygame
import sys
import random
import math
 #this will be used for animation

hashSize= 1000 # this is the size of the hashTable (aka dictionary)
Dict = {} # this is the empty dictionary ; aka the hashTable

backgroundImage = pygame.image.load('TexturePacks/Backgrounds/asteroidBackGround.jpg')
#load the spaceShip image and transform it to the desired size
spaceShipImage = pygame.transform.scale(pygame.image.load('TexturePacks/Ships/defaultTextures/spaceShip.png'), (50,50))
print(spaceShipImage.get_width(), spaceShipImage.get_height())

white = [255,255,255]

pygame.init()
width = 900
height = 650
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('First Game')

spaceShipX = 420
spaceShipY = 550
spaceShipWidth = 50
spaceShipHeight = 60

acceleration = .4 #this is the upcoming spaceships speed
crash_sound = pygame.mixer.Sound("soundFiles/crashSound.mp3")

numberOfEnemyShips = 1 # this is how many enemy ships will be in the list by default
enemyImageList = []
enemyWordList = []
enemyAccelerationList = []
enemy_x_y = [[0] * 2] * numberOfEnemyShips
enemy_width_height= [[0] * 2] * numberOfEnemyShips

enemyTypes = ['enemyType1.jpg','enemyType2.jpg','enemyType3.jpg','enemyType4.jpg'] # the 4 types of ship images
imageSizes = [[68,90],[60,63],[87,98],[85,73]] # the 4 types of ships have different sizes

font = pygame.font.SysFont("Times New Roman", 22) #this is the fond we will use to display each word with each enemyship

def setHashSize(size):
    if isValidSize(size) is True:
        hashSize = size
    else:
        hashSize = getValidSize(size)
        print('Dictionary Size set to: ' + str(hashSize))

def initDictionary():
    for x in range(1000):
        Dict.setdefault(x, []) # loop through the dictionary and at each key make a list

def isValidSize(temp):
    if temp <= 1:
        return False
    if temp == 2:
        return True
    if(temp % 2 == 0):
        return False
    for i in range (3, temp, 2):
        if(i*i <= temp):
            if (temp %i == 0):
                return False
    return True
    
def getValidSize(size):
    while isValidSize(size) == False:
        size+=1
    return size

#smallWords text file has 1531 words
#largeWords text file has 25143 words
def readFile(fileName = "Data/smallWords.txt", action = "r"):
    temp = 0
    with open(fileName, action) as inputFile:
        for line in inputFile:
            temp +=1
            #print(line.strip('\n'))
            word = line.strip('\n')
            key = getHashKey(word) 
            Dict[key].append(word)
    print("Total Words Read: " + str(temp))       
        

def getHashKey(word):
    num = 131
    total = 0
    for x in word:
        total = (total*num) + ord(x)
    return (total % hashSize) # this is the hashKey that each word is stored at

def getWordInDict(key, word):
    for x in Dict[key]:
        #,print(x)
        if(x == word):
            print("word is found")

def displaySpaceShip():
    window.blit(spaceShipImage, (spaceShipX, spaceShipY))
    

def rotateEnemyAndDisplayWord(enemyImage,enemyPositionX, enemyPositionY, enemyWidth, enemyHeight, spaceShipX, spaceShipY, randomWord):
    font = pygame.font.SysFont("Times New Roman", 25) #this is the fond we will use to display each word with each enemyship
    wordPrinted = font.render(randomWord, True, (255,255,255) )

    mydegrees = math.degrees(math.atan2(spaceShipY+20-enemyPositionY, spaceShipX+20-enemyPositionX))#get the angle in radians and convert to degrees
    rotated_image, new_rect= rotateImage(enemyImage, mydegrees, enemyPositionX+enemyWidth/2, enemyPositionY+enemyHeight/2)
    window.blit(rotated_image, new_rect.topleft)

    if ((enemyPositionY > 0) and (enemyPositionY < height )):
        if((enemyPositionX > 0) and (enemyPositionX < width)):
            window.blit(wordPrinted, (enemyPositionX,enemyPositionY-30))
            

def getRandomWord(): # returns a random word from the dictionary of words
    randomKey = random.randrange(0,1000) # get a number between 0 to a 1000, this is the hashkey of each word
    randomIndexInList = random.randrange(0, len(Dict[randomKey]))
    return Dict[randomKey][randomIndexInList]

def rotateImage(image, angle, xPos, yPos):
    rotated_image = pygame.transform.rotate(image, -angle+90)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (xPos, yPos)).center)
    return rotated_image, new_rect

def crash():
    pygame.mixer.Sound.play(crash_sound).set_volume(.1)
    print("crashed")

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()

def startSound():
    pygame.mixer.init() 
    pygame.mixer.music.load("soundFiles/spaceNoise.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play() 

def displayStats():
    distance = font.render("Nearest Ship:", True, (255,255,255))
    trajectory = font.render("Angle of Trajectory:", True, (255,255,255))
    dangerLevel = font.render("Danger Level:", True, (255,255,255))
    lives = font.render("Lives Left:", True, (255,255,255))
    score = font.render("Score:", True, (255,255,255))

    window.blit(lives, (10,510))
    window.blit(dangerLevel, (10, 540))
    window.blit(trajectory, (10, 570))
    window.blit(distance, (10, 600))
    window.blit(score, (720,600))
    

# need rectangle's center, the speed traveling at , and the angle in radians
def calculat_new_xy(old_x, old_y,speed,angle_in_radians):
    new_x = old_x + (speed*math.cos(angle_in_radians))
    new_y = old_y + (speed*math.sin(angle_in_radians))
    return new_x, new_y

def quitGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def updateFPS(fps):
    frames = font.render("FPS: " +str(fps), True, (255,255,255))
    window.blit(frames, (720, 570))

def initializeEnemyShips():
    for x in range(numberOfEnemyShips):
        randomIndex = random.randrange(0,4) # since there are only 4 types of ships with each unique sizes
        enemyImage = pygame.transform.scale(pygame.image.load("TexturePacks/Ships/defaultTextures/"+enemyTypes[randomIndex]), (imageSizes[randomIndex]))
        enemyImageList.append(enemyImage)
        enemyWordList.append(getRandomWord()) # put six randomwords in the enemyWordList
        enemy_x_y[x]=[random.randrange(0,1200), random.randrange(100,300)*-1] # append the x value
        enemy_width_height[x]=[enemyImage.get_width(),enemyImage.get_height() ] # append the width
        enemyAccelerationList.append(random.randrange(1,4)/10)


def addNewEnemyShips():
    global enemy_x_y
    global enemy_width_height
    global enemyWordList
    global enemyAccelerationList
    global enemyImageList

    enemy_x_y = [[0] * 2] * numberOfEnemyShips
    enemy_width_height= [[0] * 2] * numberOfEnemyShips
    
    for x in range(numberOfEnemyShips):
        print(x)
        randomIndex = random.randrange(0,4) # since there are only 4 types of ships with each unique sizes
        enemyImage = pygame.transform.scale(pygame.image.load("TexturePacks/Ships/defaultTextures/"+enemyTypes[randomIndex]), (imageSizes[randomIndex]))
        enemyImageList.append(enemyImage)
        enemyWordList.append(getRandomWord()) # put six randomwords in the enemyWordList
        enemy_x_y[x]=[random.randrange(0,1200), random.randrange(100,300)*-1] # append the x value
        enemy_width_height[x]=[enemyImage.get_width(),enemyImage.get_height() ] # append the width
        enemyAccelerationList.append(random.randrange(1,4)/10)
    """
    print(enemyWordList)
    print("\n")
    print(enemy_x_y)
    print("\n")
    print(enemy_width_height)
    print("\n")
    print(enemyAccelerationList)
    print("\n")"""

def startGame():
    global numberOfEnemyShips
    randomWord = getRandomWord()
    #print("This is the random Word:", randomWord)
    gameRunning = True

    #[[50,50],[50,50],[50,50],[50,50]] # the 4 types of ships have different sizes
    #[[68,90],[60,63],[87,98],[85,73]] # the 4 types of ships have different sizes
    enemyImage = pygame.transform.scale(pygame.image.load("TexturePacks/Ships/defaultTextures/"+enemyTypes[random.randrange(0,4)]), (imageSizes[0]))

    enemyXPos = random.randrange(0, width-100)
    enemyYPos = -100
    enemyWidth = enemyImage.get_width()
    enemyHeight = enemyImage.get_height()

    time= pygame.time.Clock()
    ticks = 0

    backgroundXPos = 0
    backgroundShiftSpeed = .05
    goRight = True
    gotLeft = False
    startSound()

    currentWord = ""
    indexOfOriginal = -1
    while gameRunning:
        window.blit(backgroundImage, (backgroundXPos,0)) # cover the sceen with the backgroundImage
        if(goRight == True):
            backgroundXPos -= backgroundShiftSpeed
            if(backgroundXPos <= -200):
                goRight = False
                goLeft = True
        elif(goLeft  == True):
            backgroundXPos += backgroundShiftSpeed
            if(backgroundXPos >= 0):
                goLeft = False
                goRight = True

        displaySpaceShip()
        displayStats()

        what=str(int(time.get_fps()))
        updateFPS(what)

        if(len(enemyImageList) == 0):
            numberOfEnemyShips += 1
            addNewEnemyShips()
            print(len(enemyWordList))


        for x in range(len(enemy_x_y)):
            enemyXPos = enemy_x_y[x][0] # the x position
            enemyYPos = enemy_x_y[x][1] # the y position
            enemyWidth = enemy_width_height[x][0] # the width
            enemyHeight = enemy_width_height[x][1] # the heidght

            enemyImage = enemyImageList[x]
            randomWord = enemyWordList[x]
            acceleration = enemyAccelerationList[x]


            # here we will try to detect if the enemyShip has crashed in to our homeShip
            # we can use the pygame collideRect method to see if the enemy spaceSihp collides with the homespaceship
            enemyRect = pygame.Rect(enemyXPos, enemyYPos, enemyWidth, enemyHeight)
            spaceShipRect  = pygame.Rect(spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight)
            if (enemyRect.colliderect(spaceShipRect)):

                #the crash animation goes here

                pause()
                crash()
                quitGame()

            #event handling used to be here
            
            angleInRadians= math.atan2(spaceShipY+20-enemyYPos, spaceShipX+20-enemyXPos)
            enemyXPos, enemyYPos = calculat_new_xy(enemyXPos, enemyYPos, acceleration, angleInRadians)
            enemy_x_y[x][0] = enemyXPos
            enemy_x_y[x][1] = enemyYPos

            #print(enemyXPos, enemyYPos, enemyWidth, enemyHeight, spaceShipX, spaceShipY, randomWord)
            rotateEnemyAndDisplayWord(enemyImage, enemyXPos, enemyYPos, enemyWidth, enemyHeight, spaceShipX, spaceShipY, randomWord)#display the word
            
            if(indexOfOriginal == x and (len(randomWord) == 0)):  
                indexOfOriginal = -1
                currentWord = ""                 
                del enemyWordList[x]
                del enemy_width_height[x]
                del enemy_x_y[x]
                del enemyImageList[x]
                del enemyAccelerationList[x]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                if event.type == pygame.KEYDOWN: # key down is for if a key is pressed ; pygame.key.name(event.key)
                    print("this is the currentWord length", len(currentWord), currentWord)
                    if(pygame.key.name(event.key) == enemyWordList[x][0:1] and len(currentWord) == 0):# if the first letter typed is the randomword and currentWOrd is empty
                        currentWord = randomWord # basically making a copy of the randomWord
                        currentWord = currentWord[1:]
                        indexOfOriginal = x #get the index of where this word is
                        print("current word is set to",currentWord)
                        randomWord = currentWord 
                        enemyWordList[x] = currentWord
                    if((indexOfOriginal == x) and (pygame.key.name(event.key) == currentWord[0:1])): # if the index matches and the key typed matches 
                        currentWord = currentWord[1:]
                        print("currentWOrd is now:",currentWord)
                        randomWord = currentWord 
                        enemyWordList[x] = randomWord                  
                          
                rotateEnemyAndDisplayWord(enemyImage, enemyXPos, enemyYPos, enemyWidth, enemyHeight, spaceShipX, spaceShipY, randomWord)#display the word
                pygame.display.update()
        pygame.display.update()
        ticks = time.tick(300) # framerate, the lower the number the slower the objects move
        

def main():
    setHashSize(50000) # set the hash size to roughly 50,000
    initDictionary() # loop through the dictionary and initialize the lists
    readFile("Data/largeWords.txt", "r") # read in the file
    initializeEnemyShips()
    startGame()
    

main()

"""
    print("collision detected")
    #print(spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight)
    #print(enemyXPos, enemyYPos, enemyWidth, enemyHeight)
    
    
    #gameOver screen Fade out
    s = pygame.Surface((1000,750))
    s.set_alpha(128)                
    s.fill((255,255,255))          
    window.blit(s, (0,0)) 

    s = pygame.Surface((spaceShipWidth,spaceShipHeight))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((255,255,255))           # this fills the entire surface
    window.blit(s, (spaceShipX,spaceShipY)) 

    q = pygame.Surface((enemyWidth,enemyHeight))  # the size of your rect
    q.set_alpha(128)                # alpha level
    q.fill((255,255,0))           # this fills the entire surface
    window.blit(q, (enemyXPos,enemyYPos)) 
    #pygame.draw.rect(window, pygame.Color(255, 255, 255), (spaceShipX, spaceShipY, spaceShipWidth, spaceShipHeight))
    pygame.display.update()
    """