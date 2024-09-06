import pygame, sys, random, time, os

# Initialize Pygame
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) had {0} initializing errors, exiting....".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(!) PyGame Initialized Successfully!!!")

# Set up display
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('!!! SNAKE GAME !!!')

# Colors
red = pygame.Color(255, 0, 0)  # red color-gameover
green = pygame.Color(0, 255, 0)  # green-snake
black = pygame.Color(0, 0, 0)  # black-score
white = pygame.Color(255, 255, 255)  # white-screen
brown = pygame.Color(165, 42, 42)  # brown-food

# FPS Controller
fpsController = pygame.time.Clock()

# Variables
snakePos = [100, 50]  # initial coordinate of the snake head
snakeBody = [[100, 50], [90, 50], [80, 50]]  # snake body
foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]  # random food positioning
foodSpawn = True
direction = 'RIGHT'
changeTo = direction
score = 0
level = 15
initscore = 0
highest_score = 0

# Load or initialize high score
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        highest_score = int(f.read().strip())
else:
    with open("highscore.txt", "w") as f:
        f.write("0")

def save_high_score(new_high_score):
    with open("highscore.txt", "w") as f:
        f.write(str(new_high_score))

# Game Over function
def gameOver():
    global highest_score
    if score > highest_score:
        highest_score = score
        save_high_score(highest_score)
    
    while True:
        playSurface.fill(white)
        myFont = pygame.font.SysFont('monaco', 72)
        GOsurf = myFont.render(' GAME OVER !!!', True, red)
        GOrect = GOsurf.get_rect()
        GOrect.midtop = (360, 15)
        playSurface.blit(GOsurf, GOrect)
        showScore(0)
        showHighScore()
        showMenu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    return
                elif event.key == pygame.K_h:
                    show_highscore_screen()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def showHighScore():
    sFont = pygame.font.SysFont('monaco', 42)
    Hsurf = sFont.render('HIGH SCORE : {0}'.format(highest_score), True, black)
    Hrect = Hsurf.get_rect()
    Hrect.midtop = (360, 70)
    playSurface.blit(Hsurf, Hrect)

def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 42)
    Ssurf = sFont.render('SCORE : {0}'.format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 120)
    playSurface.blit(Ssurf, Srect)

def showMenu():
    sFont = pygame.font.SysFont('monaco', 30)
    Psurf = sFont.render('Press ENTER to Play Again', True, black)
    Prect = Psurf.get_rect()
    Prect.midtop = (360, 160)
    playSurface.blit(Psurf, Prect)

    Hsurf = sFont.render('Press H for High Score', True, black)
    Hrect = Hsurf.get_rect()
    Hrect.midtop = (360, 210)
    playSurface.blit(Hsurf, Hrect)

    Esurf = sFont.render('Press ESC to Exit', True, black)
    Erect = Esurf.get_rect()
    Erect.midtop = (360, 260)
    playSurface.blit(Esurf, Erect)

def reset_game():
    global snakePos, snakeBody, foodPos, foodSpawn, direction, changeTo, score, level, initscore
    snakePos = [100, 50]
    snakeBody = [[100, 50], [90, 50], [80, 50]]
    foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True
    direction = 'RIGHT'
    changeTo = direction
    score = 0
    level = 15
    initscore = 0

def show_highscore_screen():
    playSurface.fill(white)
    myFont = pygame.font.SysFont('monaco', 72)
    Hsurf = myFont.render('HIGH SCORE : {0}'.format(highest_score), True, red)
    Hrect = Hsurf.get_rect()
    Hrect.midtop = (360, 15)
    playSurface.blit(Hsurf, Hrect)
    pygame.display.flip()
    time.sleep(3)
    gameOver()

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Validation of direction
    if changeTo == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeTo == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeTo == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    # Value change after direction change
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10

    # Snake Body Mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    if not foodSpawn:
        foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True
    playSurface.fill(white)

    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

    # Boundary Condition
    if snakePos[0] > 710 or snakePos[0] < 0 or snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()

    # Self Body Collision
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

    showScore()
    pygame.display.flip()

    if score == initscore + 5:
        level += 5
        initscore = score
    fpsController.tick(level)
