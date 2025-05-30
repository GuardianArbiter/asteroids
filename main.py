import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shots import *

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    # initialize groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # assigned containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    
    # fps and screen
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    # initialize player
    player = Player(x,y)
    field = AsteroidField()

    # scoring variables
    score = 0
    font = pygame.font.SysFont(None, 48)

    # game loop
    running = True
    while running:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # game logic / updates
        dt = clock.tick(60) / 1000
        updatable.update(dt)
        # collision detection
        for asteroid in asteroids:
            if asteroid.collision(player) == True:
                print(f"Game over! Score {score}")
                running = False
                break
            for shot in list(shots):
                if asteroid.collision(shot):
                    if asteroid.radius > ASTEROID_MIN_RADIUS:
                        score += 2
                    else:
                        score += 1
                    asteroid.split()
                    shot.kill()
                    break

        # rendering
        screen.fill((000, 000, 000))
        for sprite in drawable:
            sprite.draw(screen)
        
        # display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10,10))

        pygame.display.flip()

    pygame.quit()
        

if __name__ == "__main__":
    main()
