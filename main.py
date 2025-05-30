import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shots import *

GAME_STATE_RUNNING = 0
GAME_STATE_GAME_OVER = 1

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
    font_large = pygame.font.SysFont(None, 72)

    # game state variable
    game_state = GAME_STATE_RUNNING

    # helper function to reset the game ---
    def reset_game():
        nonlocal player, field, score, game_state # Use nonlocal to modify variables from main scope
        
        # Clear all existing sprites from groups
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()

        # Re-initialize player
        player_start_x = SCREEN_WIDTH / 2
        player_start_y = SCREEN_HEIGHT / 2
        player = Player(player_start_x, player_start_y)
        
        # Re-initialize asteroid field
        field = AsteroidField() 

        # Reset score
        score = 0
        
        # Set game state back to running
        game_state = GAME_STATE_RUNNING

    # Initial setup of player and field
    player_start_x = SCREEN_WIDTH / 2
    player_start_y = SCREEN_HEIGHT / 2
    player = Player(player_start_x, player_start_y)
    field = AsteroidField()

    # game loop
    running = True
    while running:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == GAME_STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False # quit game
                    if event.key == pygame.K_RETURN:
                        reset_game() # resets game

        if game_state == GAME_STATE_RUNNING:

            # game logic / updates
            dt = clock.tick(60) / 1000
            updatable.update(dt)
            # collision detection
            for asteroid in asteroids:
                if asteroid.collision(player) == True:
                    print(f"Game over! Score {score}")
                    game_state = GAME_STATE_GAME_OVER
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
        
        elif game_state == GAME_STATE_GAME_OVER:
            clock.tick(60)
            pass

        # rendering
        screen.fill((000, 000, 000))

        if game_state == GAME_STATE_RUNNING:
            for sprite in drawable:
                sprite.draw(screen)
        
            # display score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10,10))
        
        elif game_state == GAME_STATE_GAME_OVER:
            game_over_text = font_large.render("GAME OVER!", True, (255, 0, 0)) # Red color
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70))
            screen.blit(game_over_text, text_rect)

            # Display final score
            final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10))
            screen.blit(final_score_text, score_rect)

            # Display instructions
            instructions_text = font.render("Press ENTER to Retry or ESC to Quit", True, (0, 255, 0)) # Green color
            instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90))
            screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()

    pygame.quit()
        

if __name__ == "__main__":
    main()
