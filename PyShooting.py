import pygame
import sys
from time import sleep

padWidth = 480
padHeight = 640

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, fighter
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('STG')
    background = pygame.image.load('source/background.png')
    fighter = pygame.image.load('source/fighter.png')
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.9
    figtherX = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

        drawObject(background, 0, 0)

        drawObject(fighter, x, y)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()


initGame()

runGame()



