import random #For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * #Basic pygame imports

# Global Variables for the game
FPS = 32 # Frame per second
SCREENWIDTH = 289 # 289-width and 511-height (mobile version width and height)
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # pygame will give a display
GROUNDY = SCREENHEIGHT * 0.8 # 80% of screen height I have taken for GROUNDY
GAME_SPRITES = {} # images which is used in game
GAME_SOUNDS = {} # sounds which is used in game
PLAYER = 'C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/bird.png' # Player image (i.e. flappy_bird) location
BACKGROUND = 'C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/background.png' # Game background location
PIPE = 'C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/pipe.png' # pipe image location

# Game sprites and game sounds will be the heart of the game

def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5) # 20% of position from starting on X-axis will be excluded
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user click on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # List of Upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    # Variables for moving pipes so that we can realise that bird is moving
    pipeVelX = -4
    
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # Velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return

        # Check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery -playerHeight)

        # Move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # If the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))            
        
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in  list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y' : -y1}, # Upper Pipe
        {'x': pipeX, 'y' : y2} #Lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # initialise all pygame's module
    FPSCLOCK = pygame.time.Clock() # This clock controls game's FPS
    pygame.display.set_caption('Flappy bird by LEGEND_VK') # set titles for our game
    GAME_SPRITES['numbers'] = (
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/0.png').convert_alpha(), # convert_alpha() is used for control blitting of image and alpha on screen
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), # pygame.transform.rotate is used to show reversed pipe i.e. the upper pipe
        pygame.image.load(PIPE).convert_alpha() # for obtaining lower pipe  
    )    
    
    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/audio/hit.wav')    
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:/Users/LENOVO/Desktop/Vs Code Projects/Flappy-Bird-Game/gallery/audio/wing.wav')
    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True: # Game loop
        welcomeScreen() # Shows welcome screen until any button is pressed
        mainGame() # This is the main game function

#.............................................................Completed.....................................................................#
