import random
import os
import time
import pygame
import foodClass
import panelClass
import playClass
import statisticsClass
from buttonClass import Button
from mainConst import action, tamagotchiJump, eviltamagotchi, pixel_font, title_font
from abs_path import abs_path

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)
day = 90000
daysCount = 0
daysEvent = pygame.USEREVENT + 1
pygame.time.set_timer(daysEvent, day)

screen_width = 800
screen_height = 500
FPS = 60
timeout = 10
animCount = 0
text_timer = 0
night_timer = 0
endMenu = False
endGame = False
isSleep = False
cantClear = False
cantHelp = False
Game = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Kazekamagochi')
pygame.display.set_icon(pygame.image.load(abs_path('images/sprites/basket.png')))
clock = pygame.time.Clock()
start_time = None
game_time = None

cursor = pygame.image.load(abs_path('images/sprites/cursorHand_blue.png'))
pygame.mouse.set_visible(False)
background_menu = [pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback0.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback1.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback2.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback3.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback4.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback5.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback6.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback7.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback8.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback9.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback10.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback11.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback12.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback13.png')), (screen_width, screen_height)),
                   pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/menuback14.png')), (screen_width, screen_height))]
background = pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/room.png')), (screen_width, screen_height))
gameover_img = pygame.transform.scale(pygame.image.load(abs_path('images/backgrounds/gameover_1.png')), (screen_width, screen_height))
sleep_image = pygame.transform.scale(pygame.image.load(abs_path('images/sprites//sleep.png')), (50, 50))
day_image = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/day.png')), (50, 50))
night_image = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/night.png')), (50, 50))
kaz = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/kazsl.png')), (300, 380))
gameover_text = pixel_font.render('Маньяки...', True, (75, 255, 255))

def tamagotchiAnimation(x, y):
    global animCount
    if not isSleep:
        if animCount + 1 >= len(tamagotchiJump) * 6:
            animCount = 0
            screen.blit(tamagotchiJump[0], (x, y))
        else:
            screen.blit(tamagotchiJump[animCount // 6], (x, y))
            animCount += 1

        screen.blit(day_image, (735, 70))
    else:
        screen.blit(kaz, (x, y))


def eviltamagotchiAnimation(x, y):
    global animCount
    if not isSleep:
        if animCount + 1 >= len(eviltamagotchi) * 6:
            animCount = 0
            screen.blit(eviltamagotchi[0], (x, y))
        else:
            screen.blit(eviltamagotchi[animCount // 6], (x, y))
            animCount += 1

        screen.blit(day_image, (735, 70))
    else:
        screen.blit(kaz, (x, y))


def scoreTick():
    global start_time, timeout
    t_time = time.time() - start_time
    if t_time > timeout:
        action['satiety'] -= random.randint(1, 7)
        action['toilet'] -= random.randint(1, 5)
        action['happy'] -= random.randint(1, 5)
        action['health'] -= random.randint(1, 7)
        start_time = time.time()


def clearAfter():
    global cantClear
    if action['toilet'] + 16 <= 100:
        action['toilet'] += 16
        toilet_sound = pygame.mixer.Sound(abs_path('sounds/toilet.ogg'))
        toilet_sound.play()
    else:
        cantClear = True


def medicine():
    global cantHelp
    if action['logiki'] - 3 >= 0:
        if action['health'] + 10 <= 100:
            action['health'] += 10
            action['logiki'] -= 3
            medicine_sound = pygame.mixer.Sound(abs_path('sounds/footsteps.ogg'))
            medicine_sound.set_volume(0.9)
            medicine_sound.play()
        else:
            cantHelp = True


def game_music():
    if gameOver():
        pygame.mixer.music.load(abs_path('sounds/gameover.ogg'))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(loops=-1)
    else:
        pygame.mixer.music.load(abs_path('sounds/gamemusic.ogg'))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(loops=-1)


def spawn_coin(group):
    return playClass.Coin(random.randint(40, 760), random.randint(2, 7), abs_path('images/sprites/water.png'), group)


coins = pygame.sprite.Group()

help_menu = panelClass.Panel(400, 250, 750, 450, abs_path('images/sprites/panel_brown.png'),
                             'сделано студентом из 21-Д9-3ССА Крючковой Марией :)',
                             'Содержите Казеку в чистоте и сытости,',
                             'зарабатывая монетки починкой сети.',
                             'Удачи!', )

logika_label = Button(70, 60, 70, 70, abs_path('images/sprites/headkaz.png'))
main_label = title_font.render("The Kazekamagotchi", True, (255, 255, 255))
start_btn = Button(140, 150, 200, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Начать')
rule_btn = Button(140, 250, 200, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Помощь')
exit_btn = Button(140, 350, 200, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Выход')
menu_btn = Button(140, 450, 200, 50, abs_path('images/sprites/buttonLong_blue.png'), 'Выход')


info_health = Button(50, 50, 60, 60, abs_path('images/sprites/health.png'))
info_satiety = Button(50, 110, 50, 50, abs_path('images/sprites/apple.png'))
info_toilet = Button(50, 170, 50, 50, abs_path('images/sprites/toilet.png'))
info_happy = Button(50, 230, 50, 50, abs_path('images/sprites/smile.png'))

btn_statistic = Button(715, 40, 150, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Статистика')

btn_satiety = Button(85, 467, 140, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Покормить')
btn_toilet = Button(265, 467, 140, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Умыть')
btn_play = Button(445, 467, 150, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Чинить сеть')
btn_health = Button(670, 467, 245, 50, abs_path('images/sprites/buttonLong_brown.png'), 'Сходить к Исмаилову')


food = foodClass.FoodMenu(400, 250, 750, 450, abs_path('images/sprites/panel_brown.png'),
                          abs_path('images/sprites/buttonSquare_beige_pressed.png'),
                          abs_path('images/sprites/meat.png'), abs_path('images/sprites/coffee.png'), abs_path('images/sprites/beer.png'))

play = playClass.Play()
basket = playClass.Basket()


button_sound = pygame.mixer.Sound(abs_path('sounds/press.ogg'))
button_sound.set_volume(0.1)


def game():
    global endGame, isSleep, daysCount, night_timer, text_timer, cantClear, cantHelp, game_time, start_time
    start_time = time.time()
    pygame.mixer.music.load(abs_path('sounds/gamemusic.ogg'))
    pygame.mixer.music.play(loops=-1)

    while not endGame:
        screen.blit(background, (0, 0))
        info_satiety.blit_btn()
        satiety_text = pixel_font.render(str(action['satiety']), False, (0, 0, 0))
        screen.blit(satiety_text, (90, 90))
        info_toilet.blit_btn()
        toilet_text = pixel_font.render(str(action['toilet']), False, (0, 0, 0))
        screen.blit(toilet_text, (90, 155))
        info_happy.blit_btn()
        smile_text = pixel_font.render(str(action['happy']), False, (0, 0, 0))
        screen.blit(smile_text, (90, 215))
        health_text = pixel_font.render(str(action['health']), False, (0, 0, 0))
        screen.blit(health_text, (90, 35))
        info_health.blit_btn()

        tamagotchiAnimation(250, 70)
        if action['happy'] <= 50:
            eviltamagotchiAnimation(250, 70)

        btn_statistic.blit_btn()
        statistics = statisticsClass.Statistics(400, 250, 795, 450, abs_path('images/sprites/panel_brown.png'),
                                                str(action['logiki']) + ' монет', 'Имя: Казека', f'Дней прожито: {daysCount}')
        btn_satiety.blit_btn()
        btn_toilet.blit_btn()
        btn_play.blit_btn()
        btn_health.blit_btn()

        pos_x, pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                endGame = True
                pygame.quit()
            if event.type == daysEvent:
                isSleep = True
            if not isSleep:
                if btn_statistic.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    statisticsClass.clicked_statistics = True
                    button_sound.play()
                if btn_satiety.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    foodClass.clicked_feed = True
                    button_sound.play()
                if action['logiki'] >= 0:
                    food.pressed(pos_x, pos_y, event)
                if btn_toilet.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    clearAfter()
                if btn_play.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    game_time = time.time()
                    playClass.clicked_play = True
                    button_sound.play()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(abs_path('sounds/battlemusic.ogg'))
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play()
                if event.type == pygame.USEREVENT:
                    if playClass.clicked_play:
                        spawn_coin(coins)
                if btn_health.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                    medicine()
            if statistics.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                statisticsClass.clicked_statistics = False
                button_sound.play()
            if food.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                foodClass.clicked_feed = False
                button_sound.play()
            if play.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                playClass.clicked_play = False
                playClass.scoreCount = 0
                playClass.timeCount = 60
                playClass.seconds = 1
                button_sound.play()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(abs_path('sounds/gamemusic.ogg'))
                pygame.mixer.music.play(loops=-1)


        btn_statistic.hover(pos_x, pos_y)
        btn_satiety.hover(pos_x, pos_y)
        btn_toilet.hover(pos_x, pos_y)
        btn_play.hover(pos_x, pos_y)
        btn_health.hover(pos_x, pos_y)

        if isSleep:
            screen.blit(night_image, (735, 70))
            screen.blit(sleep_image, (440, 130))
            if night_timer > 700:
                isSleep = False
                night_timer = 0
                daysCount += 1
            night_timer += 1

        if cantClear:
            text = pixel_font.render('Не сейчас...', True, (255, 255, 255))
            screen.blit(text, (230, 400))
            if text_timer > 75:
                cantClear = False
                text_timer = 0
            text_timer += 1

        if cantHelp:
            text = pixel_font.render('Он занят...', True, (255, 255, 255))
            screen.blit(text, (660, 400))
            if text_timer > 75:
                cantHelp = False
                text_timer = 0
            text_timer += 1

        if statisticsClass.clicked_statistics:
            statistics.blit_statistics()
        if foodClass.clicked_feed:
            food.blit_food_menu()
            food.hover(pos_x, pos_y)
        if playClass.clicked_play:
            play.blit_play()
            basket.blit_basket()
            play.check_time(game_time)
            coins.draw(screen)
            coins.update(screen_height)
            if pygame.sprite.spritecollide(basket, coins, True):
                playClass.scoreCount += 1

        keys = pygame.key.get_pressed()
        play.control(keys)
        basket.control(keys)

        if pygame.mouse.get_focused():
            screen.blit(cursor, (pos_x, pos_y))

        if action['satiety'] <= 0 or action['toilet'] <= 0 or action['happy'] <= 0 or action['health'] <= 0:
            endGame = True
            gameOver()

        scoreTick()
        clock.tick(FPS)
        pygame.display.update()


def gameOver():
    global Game, endMenu, endGame
    pygame.mixer.music.load(abs_path('sounds/gameover.ogg'))
    pygame.mixer.music.play(loops=-1)
    toilet_sound = pygame.mixer.Sound(abs_path('sounds/toilet.ogg'))
    toilet_sound.play()
    while not Game:
        screen.blit(gameover_img, (0, 0))
        screen.blit(gameover_text, (60, 330))
        menu_btn.blit_btn()

        pos_x, pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if menu_btn.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                Game = True

        if pygame.mouse.get_focused():
            screen.blit(cursor, (pos_x, pos_y))

        clock.tick(FPS)
        pygame.display.update()


def menu():
    global endMenu, animCount, start_time, endGame
    pygame.mixer.music.load(abs_path('sounds/menumusic.ogg'))
    pygame.mixer.music.play(loops=-1)
    while not endMenu:
        if animCount + 1 >= len(background_menu) * 9:
            animCount = 0
            screen.blit(background_menu[0], (0, 0))
        else:
            screen.blit(background_menu[animCount // 9], (0, 0))
            animCount += 1

        logika_label.blit_btn()
        start_btn.blit_btn()
        rule_btn.blit_btn()
        exit_btn.blit_btn()
        screen.blit(main_label, (120, 40))
        # screen.blit(undermain_label, (600, 90))

        pos_x, pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                endMenu = True
                pygame.quit()
            if start_btn.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                endMenu = True
                endGame = False
                game()
            if rule_btn.rect.collidepoint(pos_x, pos_y) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                panelClass.clicked_help = True
            if help_menu.exit_rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                panelClass.clicked_help = False
            if exit_btn.rect.collidepoint((pos_x, pos_y)) and event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                pygame.mouse.set_visible(True)
                endMenu = True
                pygame.quit()

        start_btn.hover(pos_x, pos_y)
        rule_btn.hover(pos_x, pos_y)
        exit_btn.hover(pos_x, pos_y)

        if panelClass.clicked_help:
            help_menu.blit_panel()

        if pygame.mouse.get_focused():
            screen.blit(cursor, (pos_x, pos_y))

        clock.tick(FPS)
        pygame.display.update()
        
if __name__ == '__main__':       
    menu()
