from json import load
import qiskit
import pygame
import sys
import quantum_random
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT

# Macros for key inputs
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# User controlled sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Player size
        self.surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))

        # Player starting position
        self.rect = self.surface.get_rect(
            center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - PLAYER_HEIGHT-30)
        )

        # Sprite image
        self.image = pygame.image.load("./images/bear_1_15.png")

    # Move sprite based on inputs.
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Setting boundaries.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # Enemy size
        self.surface = pygame.Surface((20, 28))

        # Enemy starting position, randomized by quantum computing
        self.rect = self.surface.get_rect(
            center=(
                quantum_random.QRandom(-150, SCREEN_WIDTH+30, 3),
                5,
            )
        )

        # Horizontal and vertical velocity, randomized by quantum computing
        self.vspeed = quantum_random.QRandom(0, 10, 3)
        self.hspeed = quantum_random.QRandom(-5, 5, 3)

        # Image of enemy sprite
        self.image = pygame.image.load("./images/Fireball_15.png")

    # Update position based on velocities
    def update(self):
        self.rect.move_ip(self.hspeed, self.vspeed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        elif self.rect.left > SCREEN_WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()

def run():
    # Init display window.
    white = (255, 255, 255)

    # Start time
    time_init = pygame.time.get_ticks()

    # Game screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Custom event
    ENEMY_ADDITION = pygame.USEREVENT + 1

    # Add enemy sprite every 200ms
    pygame.time.set_timer(ENEMY_ADDITION, 200)

    # Create sprites
    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Font, timer, and music
    font = pygame.font.Font('freesansbold.ttf', 32)
    clock = pygame.time.Clock()
    pygame.mixer.music.load("./sounds/gamemusic.mp3")
    pygame.mixer.music.play(-1)

    cont = True

    # Game loop
    while cont:
        for event in pygame.event.get():
            # User hits key
            if event.type == KEYDOWN:
                # Escape Key
                if event.key == K_ESCAPE:
                    cont = False

            # User clicks close button
            elif event.type == QUIT:
                pygame.quit()
                quit()

            elif event.type == ENEMY_ADDITION:
                # Create the new enemy and add it to sprite groups
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

        keys = pygame.key.get_pressed()
        player.update(keys)
        enemies.update()

        # Fill the screen with black
        screen.fill((0, 0, 0))

        
        # Count score based on time alive
        time_elapsed = pygame.time.get_ticks()
        text = font.render(str((time_elapsed-time_init)//1000), True, white)
        textRect = text.get_rect()
        textRect.center = (40, 40)
        screen.blit(text, textRect)
        
        # Add sprites to screen
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)


        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            pygame.mixer.music.load("./sounds/hq-explosion-6288.mp3")
            pygame.mixer.music.play(1)
            cont = False

        # Update the display
        pygame.display.flip()

        clock.tick(60)

    # Return score
    return str((time_elapsed-time_init)//1000)

# Title screen of game
def title_screen():
    white = (255, 255, 255)
    black = (0, 0, 0)
    white_grey = (242, 243, 245)
    
    # Display screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    
    # Display text on screen
    pygame.display.set_caption('Quantum Dodger')
    font = pygame.font.Font('freesansbold.ttf', 32)
    instruction_font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render('Quantum Dodger', True, white)
    instruction = instruction_font.render('Press any key to play.', True, white_grey)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    instructionRect= instruction.get_rect()
    instructionRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
    
    cont = True
    # Loop for title screen
    while cont:
        screen.fill(black)
        screen.blit(text, textRect)
        screen.blit(instruction, instructionRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                cont = False
            pygame.display.update()

# End screen after game
def end_screen(score):
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    # End screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    
    # Display text and ending score
    pygame.display.set_caption('Quantum Dodger')
    font = pygame.font.Font('freesansbold.ttf', 32)
    font2 = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render('YOU DIED', True, red)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    text2 = font2.render("Score: " + score, True, white)
    text2Rect = text2.get_rect()
    text2Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT //2 +40)
    
    cont = True
    # Loop to display end screen
    while cont:
        screen.fill(black)
        screen.blit(text, textRect)
        screen.blit(text2, text2Rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                cont = False
            pygame.display.update()

# Running game
def main():
    pygame.init()
    
    title_screen()
    score = run()
    end_screen(score)

    pygame.quit()

main()