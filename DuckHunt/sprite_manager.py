import pygame
import random

class SpriteManager:
    def __init__(self, screen):
        self.screen = screen # Посилання на екран, передане з головного циклу
  
        # Параметри для роботи з відображенням головного меню
        self.leaderboard_toggled = False # Чи показувати список лідерів
        self.leaderboard_x = -1500  # Початкове положення панелі
        self.clouds = [] # Список хмаринок які існують на екрані
        self.max_clouds = 6
        self.font_main_color = (255, 255, 255)
        self.leaderboard_bg_color = (50, 50, 50)    
        self.sky_color = (15, 175, 255) # G - 135 for cloud bg

        # Параметри для роботи з анімацією переходу в гру
        self.transition_active = False
        self.transition_speed = 10
        self.camera_y = 0
        self.ground_y = 0
         # Параметри для роботи з анімаціями
        self.dog_animation_timer = 0
        self.dog_frame = 0
        self.duck_animation_timer = 0
        self.duck_frame = 0

        # Завантаження ресурсів
        self.load_fonts() # Завантаження шрифтів
        self.load_clouds() # Завантаження зображень хмар
        self.load_crown() # Завантаження зображення корони
        self.load_game_scene() # Завантаження зображення гри
        self.load_interface() # Завантаження інтерфейсу
        self.load_cursor() # Завантаження курсора
        self.load_buttons() # Завантаження кнопок
        self.load_dog() # Завантаження собаки
        self.load_all_ducks() # Завантаження зображень качок


        # Створення початкового набору хмар
        self.init_clouds()

    ####### loading resources
    def load_fonts(self):
        self.font_game_name = pygame.font.Font("DuckHunt\\Fonts\\m29.TTF", 72)
        self.font_main = pygame.font.Font("DuckHunt\\Fonts\\m29.TTF", 24)
        self.font_leaderboard = pygame.font.Font("DuckHunt\\Fonts\\m29.TTF", 20)
        self.font_game_over_panel = pygame.font.Font("DuckHunt\\Fonts\\m29.TTF", 40)
    
    def load_clouds(self):
        self.cloud_images = [pygame.image.load(f"DuckHunt\\Images\\cloud_{i}_alpha.png").convert_alpha() for i in range(1, 8)]
    
    def load_crown(self):
        self.crown_image = pygame.image.load("DuckHunt\\Images\\crown_2_alpha.png").convert_alpha()
        width, height = self.screen.get_size()
        self.crown_image = pygame.transform.scale(self.crown_image, (int(width * 0.03), int(height * 0.05)))

    def load_game_scene(self):
        self.ground_image = pygame.image.load("DuckHunt\\Images\\ground_dh_3_aplha.png").convert_alpha()
        self.ground_image = pygame.transform.scale(self.ground_image, (self.screen.get_width(), self.screen.get_width() * 0.2))

    def load_interface(self):
        self.ammo_box = pygame.image.load("DuckHunt\\Images\\ammo.png").convert_alpha()
        self.ducks_box = pygame.image.load("DuckHunt\\Images\\ducks.png").convert_alpha()
        self.score_box = pygame.image.load("DuckHunt\\Images\\score.png").convert_alpha()
        self.ammo_box = pygame.transform.scale(self.ammo_box, (int(self.screen.get_width() * 0.2), int(self.screen.get_height() * 0.1)))
        self.ducks_box = pygame.transform.scale(self.ducks_box, (int(self.screen.get_width() * 0.4), int(self.screen.get_height() * 0.1)))
        self.score_box = pygame.transform.scale(self.score_box, (int(self.screen.get_width() * 0.2), int(self.screen.get_height() * 0.1)))
        
        self.bullet_image = pygame.image.load("DuckHunt\\Images\\bullet.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.bullet_image, (int(self.ammo_box.get_width() * 0.16), int(self.ammo_box.get_height() * 0.33)))
        
        duck_scale_x = int(self.ducks_box.get_width() * 0.06)
        duck_scale_y = int(self.ducks_box.get_height() * 0.43)
        self.white_duck_image = pygame.image.load("DuckHunt\\Images\\white_duck.png").convert_alpha()
        self.white_duck_image = pygame.transform.scale(self.white_duck_image, (duck_scale_x, duck_scale_y))
        self.red_duck_image = pygame.image.load("DuckHunt\\Images\\red_duck.png").convert_alpha()
        self.red_duck_image = pygame.transform.scale(self.red_duck_image, (duck_scale_x, duck_scale_y))
        self.black_duck_image = pygame.image.load("DuckHunt\\Images\\black_duck.png").convert_alpha()
        self.black_duck_image = pygame.transform.scale(self.black_duck_image, (duck_scale_x, duck_scale_y))

        sprite_sheet = pygame.image.load("DuckHunt\\Images\\numbers_spritesheet.png")
        NUM_COLS = 5 
        NUM_ROWS = 2  
        SPRITE_WIDTH = sprite_sheet.get_width() // NUM_COLS 
        SPRITE_HEIGHT = sprite_sheet.get_height() // NUM_ROWS 

        digits = []
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                x = col * SPRITE_WIDTH
                y = row * SPRITE_HEIGHT
                digit = sprite_sheet.subsurface(pygame.Rect(x, y, SPRITE_WIDTH, SPRITE_HEIGHT))
                digit = pygame.transform.scale(digit, (int(self.score_box.get_width() * 0.155), int(self.score_box.get_height() * 0.4)))
                digits.append(digit)
        self.digits_images = digits

    def load_cursor(self):
        self.cursor_image = pygame.image.load("DuckHunt\\Images\\PES_cursor_alpha.png").convert_alpha()
        self.cursor_image = pygame.transform.scale(self.cursor_image, (self.cursor_image.get_width() * 0.75, self.cursor_image.get_height() * 0.75))
        self.cursor_image = pygame.transform.flip(self.cursor_image, True, False)

    def load_buttons(self):
        try_again_text = self.font_game_over_panel.render("TRY AGAIN", True, self.font_main_color)
        self.button_try_again_rect = pygame.Rect(
            (self.screen.get_width() * 0.5 - try_again_text.get_width()) // 2,
            self.screen.get_height() * 0.56,
            try_again_text.get_width(), 
            try_again_text.get_height()
        )
        margin = try_again_text.get_width() * 0.1
        self.button_try_again_rect.inflate_ip(margin, margin)

        self.button_exit_rect = pygame.Rect(
            (self.screen.get_width() * 0.5 - try_again_text.get_width()) // 2,
            self.screen.get_height() * 0.70,
            try_again_text.get_width(), 
            try_again_text.get_height()
        )
        self.button_exit_rect.inflate_ip(margin, margin)

    def load_dog(self):
        x_mod, y_mod = 0.33, 0.33
        dog_laugh_1_image = pygame.image.load("DuckHunt\\Images\\dog_laugh_1.png").convert_alpha()
        self.dog_laugh_1_image = pygame.transform.scale(dog_laugh_1_image, (int(self.screen.get_width() * x_mod), int(self.screen.get_height() * y_mod)))
        dog_laugh_2_image = pygame.image.load("DuckHunt\\Images\\dog_laugh_2.png").convert_alpha()
        self.dog_laugh_2_image = pygame.transform.scale(dog_laugh_2_image, (int(self.screen.get_width() * x_mod), int(self.screen.get_height() * y_mod)))

    def load_all_ducks(self):
        def scale_image(image):
            width, height = image.get_size()
            return pygame.transform.scale(image, (width * 2, height * 2))

        self.duck_sprites = {
            "black": {
                "fly": [
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_black_fly_1.png")),
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_black_fly_2.png")),
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_black_fly_3.png")),
                ],
                "shot": scale_image(pygame.image.load("DuckHunt\\Images\\duck_black_shot.png")),
                "falling": scale_image(pygame.image.load("DuckHunt\\Images\\duck_black_fall_left.png")),
            },
            "red": {
                "fly": [
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_red_fly_1.png")),
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_red_fly_2.png")),
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_red_fly_3.png")),
                ],
                "shot": scale_image(pygame.image.load("DuckHunt\\Images\\duck_red_shot.png")),
                "falling": scale_image(pygame.image.load("DuckHunt\\Images\\duck_red_fall_right.png")),
            },
            "blue": {
                "fly": [
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_blue_fly_1.png")),
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_blue_fly_2.png")),
                    scale_image(pygame.image.load("DuckHunt\\Images\\duck_blue_fly_3.png")),
                ],
                "shot": scale_image(pygame.image.load("DuckHunt\\Images\\duck_blue_shot.png")),
                "falling": scale_image(pygame.image.load("DuckHunt\\Images\\duck_blue_fall_left.png")),
            },
        }


    ####### main menu logic
    def init_clouds(self):
        """Створення початкового набору хмар, розміщених по центру"""
        cloud_1_image = pygame.image.load("DuckHunt\\Images\\cloud_2_alpha.png").convert_alpha()
        cloud_1 = {
            "x": 800,
            "y": 500,
            "speed": 0.7,
            "image": pygame.transform.scale(cloud_1_image, (cloud_1_image.get_width(), cloud_1_image.get_height())),
        }
        self.clouds.append(cloud_1)

        cloud_3_image = pygame.image.load("DuckHunt\\Images\\cloud_3_alpha.png").convert_alpha()
        cloud_3 = {
            "x": 1100,
            "y": 50,
            "speed": 0.6,
            "image": pygame.transform.scale(cloud_3_image, (cloud_3_image.get_width(), cloud_3_image.get_height())),
        }
        self.clouds.append(cloud_3)

        cloud_4_image = pygame.image.load("DuckHunt\\Images\\cloud_4_alpha.png").convert_alpha()
        cloud_4 = {
            "x": 500,
            "y": 200,  # Нехай хмара починається згорі
            "speed": 0.7,
            "image": pygame.transform.scale(cloud_4_image, (cloud_4_image.get_width(), cloud_4_image.get_height())),
        }
        self.clouds.append(cloud_4)

        cloud_8_image = pygame.image.load("DuckHunt\\Images\\cloud_8_alpha.png").convert_alpha()
        cloud_8 = {
            "x": 25,
            "y": 25,
            "speed": 0.6,
            "image": pygame.transform.scale(cloud_8_image, (cloud_8_image.get_width(), cloud_8_image.get_height())),
        }
        self.clouds.append(cloud_8)

        for _ in range(self.max_clouds - 4):
            self.spawn_cloud()

    def spawn_cloud(self):
        """Додає нову хмаринку в список"""
        cloud_image = random.choice(self.cloud_images)
        cloud = {
            "x": -cloud_image.get_width(),
            "y": random.randint(0, self.screen.get_size()[1]),
            "speed": random.uniform(0.5, 1.25),
            "image": pygame.transform.scale(cloud_image, (cloud_image.get_width(), cloud_image.get_height())),
        }
        self.clouds.append(cloud)
    
    def move_clouds(self):
        """Оновлює положення хмар і додає нові за потреби"""
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > self.screen.get_width():
                self.clouds.remove(cloud)
                self.spawn_cloud()

    def draw_clouds(self):
        """Малює всі хмари"""
        for cloud in self.clouds:
            self.screen.blit(cloud["image"], (cloud["x"], cloud["y"] - self.camera_y))

    def draw_start_screen(self):
        """Малює стартовий екран"""
        width, height = self.screen.get_size()
        
        # Небо
        self.screen.fill(self.sky_color)
        
        # Хмари
        self.draw_clouds()

        # Тексти
        title = self.font_game_name.render("Duck Hunt", True, self.font_main_color)
        start_text = self.font_main.render("TAP the screen to start", True, self.font_main_color)
        leaderboard_text = self.font_main.render("Press TAB to show leaderboards", True, self.font_main_color)

        title_rect_margin = 10
        title_rect =  (((width - title.get_width()) // 2) - title_rect_margin,
                  height * 0.2 - title_rect_margin,
                  title.get_width() + title_rect_margin * 2,
                  title.get_height() + title_rect_margin * 2)
        pygame.draw.rect(self.screen, self.leaderboard_bg_color, title_rect)
        self.screen.blit(title, ((width - title.get_width()) // 2, height * 0.2 - self.camera_y))

        self.screen.blit(start_text, ((width - start_text.get_width()) // 2, height * 0.33 - self.camera_y))
        self.screen.blit(leaderboard_text, ((width - leaderboard_text.get_width()) // 2, height * 0.93 - self.camera_y))

    def draw_leaderboard(self, leaderboard):
        """Малює панель списку лідерів. Ми її завжди промальовуємо,
          але можемо методом toggle_leaderboard() вимкнути. Той метод не прям вимикає панель,
          а просто змінює флаг який вказує чи буде панелька двигатись вправо чи вліво"""
        width, height = self.screen.get_size()
        panel_width = int(width * 0.3)

        # Плавна зміна положення панелі
        if self.leaderboard_toggled:
            self.leaderboard_x = min(self.leaderboard_x + 10, 0) # 0 - кінцеве положення
        else:
            self.leaderboard_x = max(self.leaderboard_x - 10, -panel_width) # -panel_width - кінцеве положення, щоб не було видно

        # Промальовуємо панель
        pygame.draw.rect(self.screen, self.leaderboard_bg_color, (self.leaderboard_x, 0, panel_width, height))

        # Промальовуємо заголовок
        title = self.font_main.render("Leaderboards", True, (200, 200, 200))
        self.screen.blit(title, (self.leaderboard_x + panel_width * 0.12, height * 0.03))

        # Промальовуємо список лідерів
        top_scores = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:10]
        for i in range(10):
            text = f"{i+1} {top_scores[i][0]} - {top_scores[i][1]}" if i < len(top_scores) else f"{i+1} No record"
            line = self.font_leaderboard.render(text, True, (200, 200, 200))
            self.screen.blit(line, (self.leaderboard_x + panel_width * 0.045, height * (0.1 + i * 0.05)))

        # Промальовуємо корону для лідера (якщо він є)
        if len(top_scores) > 0:
            crown_x = self.leaderboard_x + panel_width * 0.013
            crown_y = height * 0.05
            self.screen.blit(self.crown_image, (crown_x, crown_y))
    
    def toggle_leaderboard(self):
        """Вмикає або вимикає список лідерів.
        Цей метод викликати при натисканні клавіші TAB (увімкнення таблиці лідерів)
        Метод промальовування панелі виконувати завжди"""
        self.leaderboard_toggled = not self.leaderboard_toggled

    ####### transition to game scene logic
    def start_transition(self):
        """Запускає анімацію спуску"""
        self.transition_active = True
        self.camera_y = 0

    def move_camera_down(self):
        """Оновлює положення камери під час спуску"""
        if self.transition_active:
            self.camera_y += self.transition_speed
            if self.camera_y >= self.screen.get_height() - self.ground_image.get_height():
                self.ground_y += self.transition_speed
            if self.camera_y >= self.screen.get_height():
                self.ground_y = self.ground_image.get_height()
                self.transition_active = False
                self.camera_y = self.screen.get_height()

    def draw_game_scene(self, duck, in_transition = False):
        width, height = self.screen.get_size()
        self.screen.fill(self.sky_color)
        if not (in_transition):
            self.animate_duck(duck)
        self.screen.blit(self.ground_image, (0, height - self.ground_y), area=(0, 0, width, self.ground_y))

    ####### stupid shit nobody cares about
    def draw_cursor(self):
        pos = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_image, pos)

    def get_digits(number, max_digits=6):
        str_number = str(number).zfill(max_digits) # додаємо нулі зліва
        return [int(digit) for digit in str_number]
    
    ####### game scene logic
    # draw_game_scene() from transitioning is used in game scene logic too

    def draw_interface(self, ammo, ducks, score):
        width, height = self.screen.get_size()

        # Промальовуємо бокси з патронами, качками та рахунком
        boxes_y = height * 0.89
        ammo_box_x = width * 0.05
        ducks_box_x = width * 0.3
        score_box_x = width * 0.75

        self.screen.blit(self.ammo_box, (ammo_box_x, boxes_y))
        self.screen.blit(self.ducks_box, (ducks_box_x, boxes_y))
        self.screen.blit(self.score_box, (score_box_x, boxes_y))

        # Промальовуємо патрони
        bullet_first_x = ammo_box_x + self.ammo_box.get_width() * 0.19
        bullets_y = boxes_y + self.ammo_box.get_height() * 0.15

        bullet_x_skip = 0
        for _ in range(ammo):
            self.screen.blit(self.bullet_image, (bullet_first_x + bullet_x_skip, bullets_y))
            bullet_x_skip += self.bullet_image.get_width() + self.bullet_image.get_width() * 0.5

        # Промальовуємо качок
        ducks_first_x = ducks_box_x + self.ducks_box.get_width() * 0.3
        ducks_y = boxes_y + self.ducks_box.get_height() * 0.3

        ducks_x_skip = 0
        for i in range(len(ducks)):
            if ducks[i] == "hit":
                self.screen.blit(self.red_duck_image, (ducks_first_x + ducks_x_skip, ducks_y))
            elif ducks[i] == "miss":
                self.screen.blit(self.black_duck_image, (ducks_first_x + ducks_x_skip, ducks_y))
            else:
                self.screen.blit(self.white_duck_image, (ducks_first_x + ducks_x_skip, ducks_y))
            ducks_x_skip += self.white_duck_image.get_width() + self.white_duck_image.get_width() * 0.15
        


        # Промальовуємо рахунок
        score_first_x = score_box_x + self.score_box.get_width() * 0.06
        score_y = boxes_y + self.score_box.get_height() * 0.16
        score_x_skip = 0
        digit_width = self.digits_images[0].get_width()

        score_digits = SpriteManager.get_digits(score)
        for i in range(len(score_digits)):
            self.screen.blit(self.digits_images[score_digits[i]], (score_first_x + score_x_skip, score_y))
            score_x_skip += digit_width

    def draw_new_round(self, round):
        width, height = self.screen.get_size()
        round_text = self.font_game_name.render(f"ROUND {round}", True, (255,255,255))
        self.screen.blit(round_text, ((width - round_text.get_width()) // 2, height * 0.1))

    def animate_duck(self, duck):
        # Отримуємо параметри качки
        color = duck["color"]  # "black", "red", "blue"
        status = duck["status"]  # "alive", "shot", "falling"

        # Обираємо потрібний набір спрайтів качки
        frames = self.duck_sprites[color]  # {"fly": [...], "shot": [...], "falling": [...]}

        if pygame.time.get_ticks() - self.duck_animation_timer > 150:  # Кожні 150 мс змінювати кадр
            self.duck_animation_timer = pygame.time.get_ticks()
            self.duck_frame = (self.duck_frame + 1) % 3  # Лише 3 кадри для польоту

        # Вибір спрайту качки залежно від статусу
        if status == "alive":
            duck_sprite = frames["fly"][self.duck_frame]  # Летить (3 кадри)
        elif status == "shot":
            duck_sprite = frames["shot"]  # Підбита (1 кадр)
        elif status == "falling":
            duck_sprite = frames["falling"]  # Падає (1 кадр)

        # Малюємо качку на екрані
        self.screen.blit(duck_sprite, duck["position"])

    ####### game over scene logic

    def animate_dog_laugh(self, dog_x, dog_y):
        if pygame.time.get_ticks() - self.dog_animation_timer > 300:  # Перемикати кадр кожні 300 мс
            self.dog_animation_timer = pygame.time.get_ticks()
            self.dog_frame = (self.dog_frame + 1) % 2  # Перемикати між 0 і 1
        
        dog_sprite = self.dog_laugh_1_image if self.dog_frame == 0 else self.dog_laugh_2_image
        self.screen.blit(dog_sprite, (dog_x, dog_y))

    def draw_game_over(self, max_round, score, highest_score):
        width, height = self.screen.get_size()
        panel_width = int(width * 0.5)

        # Небо
        self.screen.fill(self.sky_color)

        # Пес анімація
        dog_x = ((width + panel_width) - self.dog_laugh_1_image.get_width()) // 2
        dog_y = height * 0.5
        self.animate_dog_laugh(dog_x, dog_y)

        # ЗЕмля
        self.screen.blit(self.ground_image, (0, height - self.ground_image.get_height()))

        # Панелька з результатами
        pygame.draw.rect(self.screen, self.leaderboard_bg_color, (0, 0, panel_width, height))

        game_over_text = self.font_game_name.render("GAME OVER", True, self.font_main_color)
        round_text = self.font_game_over_panel.render(f"ROUND {max_round}", True, self.font_main_color)
        score_text = self.font_game_over_panel.render(f"SCORE {score}", True, self.font_main_color)
        highest_score_text = self.font_game_over_panel.render(f"HIGHEST {highest_score}", True, self.font_main_color)

        panel_text_x = panel_width * 0.1
        self.screen.blit(game_over_text, (panel_width * 0.015, height * 0.04))
        self.screen.blit(round_text, (panel_text_x, height * 0.2))
        self.screen.blit(score_text, (panel_text_x, height * 0.3))
        self.screen.blit(highest_score_text, (panel_text_x, height * 0.4))

        try_again_text = self.font_game_over_panel.render("TRY AGAIN", True, self.font_main_color)
        exit_text = self.font_game_over_panel.render("EXIT", True, self.font_main_color)
 
        pygame.draw.rect(self.screen, self.font_main_color, self.button_try_again_rect, width = 3, border_radius=10)
        pygame.draw.rect(self.screen, self.font_main_color, self.button_exit_rect, width = 3, border_radius=10)

        self.screen.blit(try_again_text, ((panel_width - try_again_text.get_width()) // 2, height * 0.56))
        self.screen.blit(exit_text, ((panel_width - exit_text.get_width()) // 2, height * 0.70))



    

