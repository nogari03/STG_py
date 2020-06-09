import pygame
import sys
import random
from time import sleep

# BLACK = (0,0,0)
padWidth = 480
padHeight = 640
rockImage = ['source/rock01.png', 'source/rock02.png', 'source/rock03.png', 'source/rock04.png',
             'source/rock05.png', 'source/rock06.png', 'source/rock07.png', 'source/rock08.png',
             'source/rock09.png', 'source/rock10.png', 'source/rock11.png', 'source/rock12.png',
             'source/rock13.png', 'source/rock14.png', 'source/rock15.png', 'source/rock16.png',
             'source/rock17.png', 'source/rock18.png', 'source/rock19.png', 'source/rock20.png',
             'source/rock21.png', 'source/rock22.png', 'source/rock23.png', 'source/rock24.png',
             'source/rock25.png', 'source/rock26.png', 'source/rock27.png', 'source/rock28.png',
             'source/rock29.png', 'source/rock30.png']
explosionSound = ['source/explosion01.wav', 'source/explosion02.wav', 'source/explosion03.wav', 'source/explosion04.wav']
gameOverSound = ['source/gameover.wav']

def writeScore(count):
    global gamePad
    font = pygame.font.Font('source/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수:'+str(count), True, (255, 255, 255))
    gamePad.blit(text, (10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('source/NanumGothic.ttf', 20)
    text = font.render('놓친 운석 수:'+str(count), True, (255, 0, 0))
    gamePad.blit(text, (340,0))

def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('source/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage('전투기 파괴')

def gameOver():
    global gamePad
    writeMessage('게임 오버!')

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth,padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('source/background.png')
    fighter = pygame.image.load('source/fighter.png')
    missile = pygame.image.load('source/missile.png')
    explosion = pygame.image.load('source/explosion.png')
    pygame.mixer.music.load('source/music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('source/missile.wav')
    gameOverSound = pygame.mixer.Sound('source/gameover.wav')
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosionSound, missileSound, gameOverSound

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)

        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                    (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()

        drawObject(fighter, x, y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)

        rockY += rockSpeed

        if rockY > padHeight:

            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            gameOver()

        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY)
            destroySound.play()

            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False

            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)

        # gamePad.fill(BLACK)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

initGame()
runGame()