import pygame
from sprite_manager import SpriteManager

pygame.init()

screen_info = pygame.display.Info() 
screen_width = screen_info.current_w 
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height - 50),  pygame.FULLSCREEN)

clock = pygame.time.Clock()
sprite_manager = SpriteManager(screen)
leaderboard = [("Player1", 100), ("Player2", 90), ("Player3", 80)]
in_main_menu = True
in_transition = False
in_game = False

duck = {"color": "black", "status": "alive", "position": (150,600), "velocity": 1, "vector": (1,-1) }

pygame.mouse.set_visible(False)

running = True
while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                sprite_manager.toggle_leaderboard()     
        #if event.type == pygame.MOUSEBUTTONDOWN and in_main_menu:
        #    in_main_menu = False
        #    in_transition = True
        #   sprite_manager.start_transition()

    # просто для тесту 
    if in_main_menu and pygame.key.get_pressed()[pygame.K_5]:
        sprite_manager.draw_game_over(15,150,19050)       
        if (pygame.mouse.get_pressed()[0]):
            if (sprite_manager.check_button_tryagain_click(pygame.mouse.get_pos())):
                print("Try again clicked") # 
            if (sprite_manager.check_button_quit_click(pygame.mouse.get_pos())):
                print("Quit clicked")
    elif in_main_menu :
        sprite_manager.move_clouds()
        sprite_manager.draw_start_screen()
        sprite_manager.draw_leaderboard(leaderboard)
    elif in_transition:
        sprite_manager.move_clouds()
        sprite_manager.move_camera_down()
        sprite_manager.draw_game_scene(None, in_transition=True)
        sprite_manager.draw_clouds()
        if not sprite_manager.transition_active:
            in_transition = False
            in_game = True
    elif in_game:
        def update_duck_position(duck): 
            # хто буде ось це робити, у вас качка не тільки літає.
            #  Вона також в залежності від статусу може на пів секунди зависіти в повітрі,
            #  потім якщо статус падає то тупо вниз падає
            x, y = duck["position"]
            vx, vy = duck["vector"]
            speed = duck["velocity"]
            duck["position"] = (x + speed * vx, y + speed * vy)

        update_duck_position(duck)
        sprite_manager.draw_game_scene(duck)

        # порядок виклику методів дуже важливий, звернути на це увагу. 
        # як правило оновити положення, перевірити колізію, потім намалювати

        if (pygame.mouse.get_pressed()[0] and duck["status"] == "alive"):
            if (sprite_manager.check_duck_collision(duck, pygame.mouse.get_pos())):
                print("Duck hit!")
                duck["status"] = "shot" 
                # має бути якась логіка зміни статусу качки.
                # Є статус alive, shot, dead, falling. 
                # Якийсь таймер запускати для зміни статусу після того як підбили, щоб адекватно змінювалась анімаційка.

        ammo = 1
        ducks = ["hit", "hit", "miss", "hit", "miss", "", "", "", "", ""]
        score = 150
        sprite_manager.draw_interface(ammo, ducks, score)


        sprite_manager.draw_new_round(4)

    
    sprite_manager.draw_cursor()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

