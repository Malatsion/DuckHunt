import pygame
from Entity import Duck, Dog, Player
from DuckHunt.sprite_manager import SpriteManager
from DuckHunt.level_manager import  LevelManager
#from datetime import datetime
import random

import argparse

parser = argparse.ArgumentParser(description="Input parameters for Duck Hunt game")
parser.add_argument('--nickname', type=str, required=False, help='Your nickname')
parser.add_argument('--fast_ducks_mode', action='store_true', help='Enable fast ducks mode')
parser.add_argument('--no_reload_mode', action='store_true', help='Enable no reload mode')

args = parser.parse_args()
# Використання аргументів - 
# args.nickname :string
# args.fast_ducks_mode :bool
# args.no_reload_mode :bool

args.nickname = args.nickname if args.nickname else "Player"  # Якщо ім’я не вказано, використовуємо "Player"
#args.no_reload_mode = True 
#args.fast_ducks_mode = True

# Ініціалізація Pygame
pygame.init()

pygame.mixer.init()

# Налаштування екрана
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h - 50
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Duck Hunt")
pygame.mouse.set_visible(False)

# Ініціалізація менеджера спрайтів та годинника
clock = pygame.time.Clock()
sprite_manager = SpriteManager(screen)
level_manager = LevelManager(args.fast_ducks_mode, args.no_reload_mode)

# Завантаження зображень
sound_title = pygame.mixer.Sound("DuckHunt\Sounds\Title.mp3")
sound_game_over = pygame.mixer.Sound("DuckHunt\Sounds\8 - Game Over.mp3")
sound_gun_shot = pygame.mixer.Sound("DuckHunt\Sounds/10 - SFX Gun Shot.mp3")
sound_duck_quack = pygame.mixer.Sound("DuckHunt\Sounds/13 - SFX Duck Quack.mp3")
sound_duck_fall = pygame.mixer.Sound("DuckHunt\Sounds/14 - SFX Dead Duck Falls.mp3")
sound_bg_ingame = pygame.mixer.Sound("DuckHunt\\Sounds\\bg_music.mp3")
pygame.mixer.music.load("DuckHunt/Sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)

gunshot_channel = pygame.mixer.Channel(0) 
duckquack_channel = pygame.mixer.Channel(1)  
duck_fall_channel = pygame.mixer.Channel(2)  
bg_music_channel = pygame.mixer.Channel(3)

# Встановимо гучність (опціонально)
sound_title.set_volume(0.2)
sound_game_over.set_volume(0.2)
sound_gun_shot.set_volume(0.2)
sound_duck_quack.set_volume(0.8)
sound_duck_fall.set_volume(0.3)
sound_bg_ingame.set_volume(0.5)

# Стани гри
STATE_MAIN_MENU = "main_menu"
STATE_TRANSITION = "transition"
STATE_GAME = "game"
STATE_GAME_OVER = "game_over"
current_state = STATE_MAIN_MENU

# Ігрові змінні
#current_round = 1 #це не треба, бо є level_manager.get_level
duck_index = 0  # Індекс поточної качки в раунді (0-9)
ammo = 3  # Початкові патрони
ducks_status = ["", "", "", "", "", "", "", "", "", ""]  # Статуси качок для інтерфейсу
max_round = 1
highest_score = 0
last_shot_time = 0  # Для затримки між пострілами
shot_cooldown = 500  # 500 мс затримка
fall_start_time = 0  # Час початку падіння качки
is_falling = False  # Чи качка в стані падіння
duck_colors = ["black", "red", "blue"]  # Доступні кольори качок
base_velocity = random.uniform(3, 7) * level_manager.get_speed_multiplier() # Базова швидкість для раунду

# Ігрові об’єкти
player = Player.Player(name=args.nickname)  # Унікальне ім’я
duck = Duck.Duck((screen_width // 2, screen_height // 2), screen_width, screen_height)
duck_color = random.choice(duck_colors)  # Випадковий колір качки
duck.velocity = base_velocity  # Встановлюємо швидкість для першої качки
dog = Dog.Dog(screen_width, screen_height)
leaderboard = []  # Список лідерів: [(ім’я, рахунок), ...]

sprite_width = sprite_manager.duck_sprites["black"]["shot"].get_width()  # Розмір спрайта качки
sprite_height = sprite_width  # Розмір спрайта качки

# Головний цикл гри
running = True
while running:
    current_time = pygame.time.get_ticks()

    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB and current_state == STATE_MAIN_MENU:
                sprite_manager.toggle_leaderboard()
            elif event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if current_state == STATE_MAIN_MENU:
                # Перехід до гри
                current_state = STATE_TRANSITION
                sprite_manager.start_transition()

            elif current_state == STATE_GAME and current_time - last_shot_time > shot_cooldown:
                last_shot_time = current_time
                if ammo > 0:
                    ammo -= 1
                    gunshot_channel.play(sound_gun_shot)
                    duck_dict = {
                        "color": duck_color,
                        "status": duck.status,
                        "position": tuple(duck.position)
                    }
                    if sprite_manager.check_duck_collision(duck_dict, mouse_pos):   
                        duckquack_channel.play(sound_duck_quack)
                        duck_fall_channel.play(sound_duck_fall)
                        duck.unalive()  # Збиваємо качку
                        duck.status = "falling"  # Переходимо до падіння
                        is_falling = True
                        fall_start_time = current_time
                        player.add_points(100)  # Додаємо очки
                        ducks_status[duck_index] = "hit"
                    else:
                        duck.register_shot_nearby()  # Реєструємо постріл поруч
                        ducks_status[duck_index] = "miss"
                        # if ammo == 0:
                        #     print(f"Ammo depleted, waiting for duck to escape: {duck.status}")

            elif current_state == STATE_GAME_OVER:
                if sprite_manager.check_button_tryagain_click(mouse_pos):
                    # Скидання гри
                    sprite_manager = SpriteManager(screen)  # Перестворюємо SpriteManager
                    # print("SpriteManager recreated for TRY AGAIN")
                    screen.fill((0, 0, 0))  # Очищаємо екран
                    sprite_manager.draw_start_screen()  # Малюємо стартовий екран
                    pygame.display.update()  # Оновлюємо екран негайно
                    current_state = STATE_MAIN_MENU
                    ammo = 3
                    ducks_status = ["", "", "", "", "", "", "", "", "", ""]
                    player.points = 0
                    level_manager.reset()
                    base_velocity = random.uniform(3, 7) * level_manager.get_speed_multiplier()
                    duck_index = 0
                    highest_score = player.max_points
                    duck = Duck.Duck(
                        (screen_width // 2, screen_height // 2),
                        screen_width,
                        screen_height
                    )
                    duck_color = random.choice(duck_colors)
                    duck.velocity = base_velocity
                    is_falling = False
                    dog.stop_laughing()
                elif sprite_manager.check_button_quit_click(mouse_pos):
                    running = False

    # Оновлення стану гри
    if current_state == STATE_MAIN_MENU:
        duck_fall_channel.play(sound_title)
        sprite_manager.move_clouds()
        sprite_manager.draw_start_screen()
        sprite_manager.draw_leaderboard(leaderboard)
        

    elif current_state == STATE_TRANSITION:
        screen.fill((0, 0, 0))  # Очищаємо екран
        sprite_manager.move_clouds()
        sprite_manager.draw_start_screen()  # Встановлюємо фон
        sprite_manager.move_camera_down()
        sprite_manager.draw_game_scene(
            {"color": duck_color, "status": duck.status, "position": tuple(duck.position)},
            in_transition=True
        )
        sprite_manager.draw_clouds()
        if not sprite_manager.transition_active:
            current_state = STATE_GAME

    elif current_state == STATE_GAME:
        if not bg_music_channel.get_busy():
            bg_music_channel.play(sound_bg_ingame)  # Відтворення фонової музики
        # Оновлення качки
        if not is_falling:
            # Фіксуємо швидкість качки
            if duck.velocity != base_velocity:
                # print(f"Velocity corrected from {duck.velocity} to {base_velocity}")
                duck.velocity = base_velocity
            duck.update(current_time)
            # Примусова перевірка виходу спрайта за межі екрана
            if (duck.position[0] + sprite_width <= 0 or
                    duck.position[0] >= screen_width or
                    duck.position[1] + sprite_height <= 0 or
                    duck.position[1] >= screen_height):
                duck.status = "escaped"
            #     print(f"Duck escaped at position: {duck.position}")
            # print(f"Duck sprite bounds: [{duck.position[0]}, {duck.position[0] + sprite_width}, "
            #       f"{duck.position[1]}, {duck.position[1] + sprite_height}], status: {duck.status}, ammo: {ammo}")
        elif is_falling:
            duck.position[1] += duck.velocity * 2  # Рух вниз для анімації падіння
            # print(f"Falling duck position: {duck.position[1]}")  # Діагностика
        # Перевірка втечі або завершення падіння
        if duck.status == "escaped" or (is_falling and duck.position[1] >= screen_height):
            duck_index += 1
            if duck.status == "escaped":
                ducks_status[duck_index - 1] = "miss"  # Позначити качку як пропущену
            if duck_index >= 10 or (level_manager.check_no_reload_mode() and ammo == 0 and ducks_status[duck_index - 1] == "miss"):
                if (not level_manager.check_no_reload_mode() and sum(1 for status in ducks_status if status == "miss") >= 4) or (level_manager.check_no_reload_mode() and duck.status == "escaped"):
                    gunshot_channel.play(sound_game_over)
                    # Оновлення рекорду перед GAME_OVER
                    if player.max_points > highest_score:
                        # player.max_points = player.points
                        highest_score = player.max_points
                        # print(f"New high score: {highest_score}")
                    current_state = STATE_GAME_OVER
                    max_round = level_manager.get_level()
                    leaderboard.append((player.player_name, player.points))
                    leaderboard.sort(key=lambda x: x[1], reverse=True)
                    dog.start_laughing()
                else:
                    # Новий раунд
                    level_manager.next_level()
                    ammo = 3
                    duck_index = 0
                    ducks_status = ["", "", "", "", "", "", "", "", "", ""]
                    base_velocity += random.uniform(3, 7) * level_manager.get_speed_multiplier()  # Нова швидкість для раунду
                    duck = Duck.Duck(
                        (screen_width // 2, screen_height // 2),
                        screen_width,
                        screen_height
                    )
                    duck_color = random.choice(duck_colors)
                    duck.velocity = base_velocity
                    is_falling = False
            else:
                # Нова качка в межах раунду
                if level_manager.check_no_reload_mode() and ammo < 3 and ducks_status[duck_index - 1] == "hit":
                    ammo += 1
                elif not level_manager.check_no_reload_mode():
                    ammo = 3
                duck = Duck.Duck(
                    (screen_width // 2, screen_height // 2),
                    screen_width,
                    screen_height
                )
                duck_color = random.choice(duck_colors)
                duck.velocity = base_velocity  # Використовуємо швидкість раунду
                is_falling = False
        else:
            sprite_manager.draw_game_scene(
                {"color": duck_color, "status": duck.status, "position": tuple(duck.position)}
            )
        sprite_manager.draw_interface(ammo, ducks_status, player.points)
        sprite_manager.draw_new_round(level_manager.get_level())

    elif current_state == STATE_GAME_OVER:
        bg_music_channel.stop()  # Зупинка фонової музики
        dog.update(current_time)  # Оновлення анімації собаки
        sprite_manager.draw_game_over(max_round, player.points, highest_score)

    # Промальовка курсора
    sprite_manager.draw_cursor()

    # Оновлення екрана
    pygame.display.update()
    clock.tick(30)

# Завершення гри
pygame.quit()