import pygame, numpy, noise, game, sys, time, os
from random import randint

try:
    if sys.argv[1] == "debug=true":
        Debug = True
    else:
        Debug = False
except:
    Debug = False

# Get seed 
try:
    seed = int(sys.argv[2])
except:
    seed = randint(1,10000)

# Set standard tile size
tilesize = 10

# Game font for FPS
clock = pygame.time.Clock()
def update_fps():
    font = pygame.font.SysFont("Arial", 24)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

# Init Game Class
game = game.Game(seed,errorLog=Debug)
game.log("Playing on seed: " + str(seed))

# Init game window (Fullscreen)
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
running = True

frameTime = time.time()

# Save Function
def save():
    game.log("Saving game...")
    if game.debug == False:
        os.system("taskkill /f /im cmd.exe")
    game.log("Saved!")

#detect game running
while running:
    # Delta time calculation
    currentTime = time.time()
    dt = currentTime - frameTime
    frameTime = time.time()

    # Event Handeler
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        

    # Camera Movement
    keys=pygame.key.get_pressed()
    if keys[pygame.K_w]:
        game.camY += game.speed * (dt * 100)
    if keys[pygame.K_s]:
        game.camY -= game.speed * (dt * 100)
    if keys[pygame.K_a]:
        game.camX += game.speed * (dt * 100)
    if keys[pygame.K_d]:
        game.camX -= game.speed * (dt * 100)
    if keys[pygame.K_ESCAPE]:
        running = False

    screen.fill((0,0,0))

    w, h = pygame.display.get_surface().get_size()
    game.tryChunkGen()
    game.render(screen, tilesize, w, h)
    
    # Draw FPS in top right
    screen.blit(update_fps(), (10,0))

    # Update display
    pygame.display.update()
    clock.tick()

save()

game.log("Game Ended")
game.log("")
game.log("---=====================---")