import pygame, os
from abs_path import abs_path

pygame.init()

width = 300
height = 380
action = {'satiety': 100, 'toilet': 100, 'happy': 100, 'health': 100, 'logiki': 50}
screen = pygame.display.set_mode((800, 500))
pixel_font = pygame.font.Font(abs_path('font/EpilepsySans.ttf'), 27)
title_font = pygame.font.Font(abs_path('font/EpilepsySansBold.ttf'), 55)
tamagotchiJump = [pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz0.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz1.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz2.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz3.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz4.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz5.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz6.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz7.png')), (width, height))]

eviltamagotchi = [pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz0zlo.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz1zlo.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz2zlo.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz3zlo.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz4zlo.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz5zlo.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz6zlo.png')), (width, height)),
                  pygame.transform.scale(pygame.image.load(abs_path('images/sprites/tamagotchi animation/kaz7zlo.png')), (width, height))]