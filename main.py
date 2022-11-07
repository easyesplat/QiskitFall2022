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
        self.surface = pygame.Surface((20, 10))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
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
                cont = False

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
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.fill(0, 0, 0)

def main():
    pygame.init()
    
   # title_screen()
    run()
   # end_screen()

    pygame.quit()

main()