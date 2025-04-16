import pygame
from Entity import Duck, Dog, Player
from DuckHunt.sprite_manager import SpriteManager
from datetime import datetime
import random

# Ініціалізація Pygame
pygame.init()

# Налаштування екрану
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h - 50
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Duck Hunt")
pygame.mouse.set_visible(False)

# Ініціалізація менеджера спрайтів та годинника
clock = pygame.time.Clock()
sprite_manager = SpriteManager(screen)

# Стани гри
STATE_MAIN_MENU = "main_menu"
STATE_TRANSITION = "transition"
STATE_GAME = "game"
STATE_GAME_OVER = "game_over"
current_state = STATE_MAIN_MENU

# Ігрові змінні
current_round = 1
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
base_velocity = random.uniform(3, 7) * (1 + 0.1 * current_round)  # Базова швидкість для раунду

# Ігрові об’єкти
player = Player.Player(name="Player" + str(random.randint(1000, 9999)))  # Унікальне ім’я
duck = Duck.Duck((screen_width // 2, screen_height // 2), screen_width, screen_height)
duck_color = random.choice(duck_colors)  # Випадковий колір качки
duck.velocity = base_velocity  # Встановлюємо швидкість для першої качки
dog = Dog.Dog(screen_width, screen_height)
leaderboard = []  # Список лідерів: [(ім’я, рахунок), ...]

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
                    duck_dict = {
                        "color": duck_color,
                        "status": duck.status,
                        "position": tuple(duck.position)
                    }
                    if sprite_manager.check_duck_collision(duck_dict, mouse_pos):
                        duck.unalive()  # Збиваємо качку
                        duck.status = "falling"  # Переходимо до падіння
                        is_falling = True
                        fall_start_time = current_time
                        player.add_points(100)  # Додаємо очки
                        ducks_status[duck_index] = "hit"
                    else:
                        duck.register_shot_nearby()  # Реєструємо постріл поруч
                        ducks_status[duck_index] = "miss"

            elif current_state == STATE_GAME_OVER:
                if sprite_manager.check_button_tryagain_click(mouse_pos):
                    # Скидання гри
                    screen.fill((0, 0, 0))  # Очищаємо екран
                    for _ in range(10):  # Багаторазовий виклик для скидання хмар
                        sprite_manager.move_clouds()
                    sprite_manager.draw_start_screen()  # Малюємо стартовий екран
                    pygame.display.update()  # Оновлюємо екран негайно
                    current_state = STATE_MAIN_MENU
                    ammo = 3
                    ducks_status = ["", "", "", "", "", "", "", "", "", ""]
                    player.points = 0
                    current_round = 1
                    duck_index = 0
                    highest_score = player.max_points
                    base_velocity = random.uniform(3, 7) * (1 + 0.1 * current_round)
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
        sprite_manager.move_clouds()
        sprite_manager.draw_start_screen()
        sprite_manager.draw_leaderboard(leaderboard)

    elif current_state == STATE_TRANSITION:
        screen.fill((0, 0, 0))  # Очищаємо екран
        for _ in range(10):  # Багаторазовий виклик для скидання хмар
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
        # Оновлення качки
        if not is_falling:
            duck.update(current_time)
        elif current_time - fall_start_time < 500:
            duck.position[1] += duck.velocity * 2  # Рух вниз для анімації падіння
        # Перевірка втечі, закінчення патронів або завершення падіння
        if duck.status == "escaped" or ammo == 0 or (is_falling and current_time - fall_start_time >= 500):
            duck_index += 1
            if duck.status == "escaped":
                ducks_status[duck_index - 1] = "miss"  # Позначити качку як пропущену
            if duck_index >= 10:
                if sum(1 for status in ducks_status if status == "miss") >= 4:
                    current_state = STATE_GAME_OVER
                    max_round = current_round
                    leaderboard.append((player.player_name, player.points))
                    leaderboard.sort(key=lambda x: x[1], reverse=True)
                    dog.start_laughing()
                else:
                    # Новий раунд
                    current_round += 1
                    ammo = 3
                    duck_index = 0
                    ducks_status = ["", "", "", "", "", "", "", "", "", ""]
                    base_velocity = random.uniform(3, 7) * (1 + 0.1 * current_round)  # Нова швидкість для раунду
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
        sprite_manager.draw_new_round(current_round)

    elif current_state == STATE_GAME_OVER:
        dog.update(current_time)  # Оновлення анімації собаки
        sprite_manager.draw_game_over(max_round, player.points, highest_score)

    # Промальовка курсору
    sprite_manager.draw_cursor()

    # Оновлення екрану
    pygame.display.update()
    clock.tick(60)

# Завершення гри
pygame.quit()