import pygame, os
from mainConst import action, screen, pixel_font
from abs_path import abs_path

pygame.init()

clicked_feed = False
coin_sound = pygame.mixer.Sound(abs_path('sounds/coin.ogg'))


class FoodMenu:
    def __init__(self, x, y, width, height, panel_path, box_path, meat_path, coffee_path, beer_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.panel = pygame.transform.scale(pygame.image.load(panel_path), (self.width, self.height))
        self.panel_rect = self.panel.get_rect(center=(self.x, self.y))

        self.box_1 = pygame.transform.scale(pygame.image.load(box_path), (150, 150))
        self.box_2 = pygame.transform.scale(pygame.image.load(box_path), (150, 150))
        self.box_3 = pygame.transform.scale(pygame.image.load(box_path), (150, 150))

        self.normal_image = self.box_1

        self.box_1_rect = self.box_1.get_rect(center=(self.x - 250, self.y))
        self.box_2_rect = self.box_2.get_rect(center=(self.x, self.y))
        self.box_3_rect = self.box_3.get_rect(center=(self.x + 250, self.y))

        self.meat = pygame.transform.scale(pygame.image.load(meat_path), (100, 100))
        self.coffee = pygame.transform.scale(pygame.image.load(coffee_path), (100, 100))
        self.beer = pygame.transform.scale(pygame.image.load(beer_path), (100, 100))

        self.meat_rect = self.meat.get_rect(center=(self.x - 250, self.y))
        self.coffee_rect = self.coffee.get_rect(center=(self.x, self.y))
        self.beer_rect = self.beer.get_rect(center=(self.x + 250, self.y))

        self.exit = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/iconCross_beige.png')), (40, 40))
        self.exit_rect = self.exit.get_rect(center=(75, 65))

    def blit_food_menu(self):
        if clicked_feed:
            screen.blit(self.panel, self.panel_rect)

            screen.blit(self.box_1, self.box_1_rect)
            screen.blit(self.box_2, self.box_2_rect)
            screen.blit(self.box_3, self.box_3_rect)

            screen.blit(self.meat, self.meat_rect)
            screen.blit(self.coffee, self.coffee_rect)
            screen.blit(self.beer, self.beer_rect)

            screen.blit(self.exit, self.exit_rect)

    def hover(self, x, y):
        if self.box_1_rect.collidepoint((x, y)):
            text = pixel_font.render('Шашлык: 5 монеток,', True, (255, 255, 255))
            screen.blit(text, (60, 95))
            text2 = pixel_font.render('"Сам готовил"', True, (255, 255, 255))
            screen.blit(text2, (60, 120))
            text3 = pixel_font.render('Эффекты: +3', True, (255, 255, 255))
            screen.blit(text3, (60, 145))
            self.box_1 = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/buttonSquare_blue.png')), (150, 150))
        else:
            self.box_1 = self.normal_image
        if self.box_2_rect.collidepoint((x, y)):
            text = pixel_font.render('Кофе: 10 монеток,', True, (255, 255, 255))
            screen.blit(text, (270, 95))
            text2 = pixel_font.render('"Для сердца"', True, (255, 255, 255))
            screen.blit(text2, (270, 120))
            text3 = pixel_font.render('Эффекты: +6', True, (255, 255, 255))
            screen.blit(text3, (270, 145))
            self.box_2 = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/buttonSquare_blue.png')), (150, 150))
        else:
            self.box_2 = self.normal_image
        if self.box_3_rect.collidepoint((x, y)):
            text = pixel_font.render('Пивко: 15 монеток,', True, (255, 255, 255))
            screen.blit(text, (480, 95))
            text2 = pixel_font.render('"Для души"', True, (255, 255, 255))
            screen.blit(text2, (480, 120))
            text2 = pixel_font.render('Эффекты: +10', True, (255, 255, 255))
            screen.blit(text2, (480, 145))
            self.box_3 = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/buttonSquare_blue.png')), (150, 150))
        else:
            self.box_3 = self.normal_image

    def pressed(self, x, y, event):
        if self.box_1_rect.collidepoint((x, y)) and event.type == pygame.MOUSEBUTTONDOWN:
            if action['satiety'] + 3 <= 100 and action['logiki'] - 5 >= 0:
                coin_sound.play()
                action['satiety'] += 3
                action['toilet'] -= 3
                action['logiki'] -= 5
        if self.box_2_rect.collidepoint((x, y)) and event.type == pygame.MOUSEBUTTONDOWN:
            if action['satiety'] + 6 <= 100 and action['logiki'] - 10 >= 0:
                coin_sound.play()
                action['satiety'] += 6
                action['toilet'] -= 6
                action['logiki'] -= 10
        if self.box_3_rect.collidepoint((x, y)) and event.type == pygame.MOUSEBUTTONDOWN:
            if action['satiety'] + 10 <= 100 and action['logiki'] - 15 >= 0:
                coin_sound.play()
                action['satiety'] += 10
                action['toilet'] -= 10
                action['logiki'] -= 15
