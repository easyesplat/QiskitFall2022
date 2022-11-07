import qiskit
import pygame
import sys
import quantum_random
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
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        # Setting boundaries.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

def run():
     # Init display window.
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    player = Player()

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

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Fill the screen with black
        screen.fill((0, 0, 0))
        # Drawing player
        screen.blit(player.surface, player.rect)

        # Update the display
        pygame.display.flip()

def main():
    pygame.init()

    run()

    pygame.quit()

main()