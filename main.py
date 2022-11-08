import qiskit
import pygame
import sys
import quantum_random
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = pygame.Surface((25, 25))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(
            center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10)
        )

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surface = pygame.Surface((10, 20))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect(
            center=(
                quantum_random.QRandom(-150, SCREEN_WIDTH+30, 3),
                5,
            )
        )
        #self.speed = random.randint(5, 20)
        self.speed = 10

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def run():
    # Init display window.
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Custom event
    ENEMY_ADDITION = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_ADDITION, 250)

    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    clock = pygame.time.Clock()

    cont = True
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
        
        for entity in all_sprites:
            screen.blit(entity.surface, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            cont = False

        # Update the display
        pygame.display.flip()

        clock.tick(60)

def title_screen():
    white = (255, 255, 255)
    black = (0, 0, 0)
    white_grey = (242, 243, 245)
    
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    
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

def end_screen():
    red = (255, 0, 0)
    black = (0, 0, 0)
    
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    
    pygame.display.set_caption('Quantum Dodger')
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('YOU DIED', True, red)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    cont = True
    while cont:
        screen.fill(black)
        screen.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                cont = False
            pygame.display.update()

def main():
    pygame.init()
    
    title_screen()
    run()
    end_screen()

    pygame.quit()

main()