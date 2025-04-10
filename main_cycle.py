import pygame
from sprite_manager import SpriteManager

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height - 50), pygame.FULLSCREEN)
leaderboard = []

clock = pygame.time.Clock()
sprite_manager = SpriteManager(screen)
in_main_menu = True
in_transition = False
in_game = False

duck = {"color": "black", "status": "alive", "position": (150, 600), "velocity": 5, "vector": (1, -1)}
ducks = ["", "", "", "", "", "", "", "", "", ""]

pygame.mouse.set_visible(False)

round_num = 1
ammo = 3
score = 0

running = True
while running:
    #screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            sprite_manager.toggle_leaderboard()
        if event.type == pygame.MOUSEBUTTONDOWN and in_main_menu:
            in_main_menu = False
            in_transition = True
            sprite_manager.start_transition()

    if in_main_menu and pygame.key.get_pressed()[pygame.K_5]:
        sprite_manager.draw_game_over(15, 150, 19050)
    elif in_main_menu:
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
            x, y = duck["position"]
            vx, vy = duck["vector"]
            speed = duck["velocity"]
            duck["position"] = (x + speed * vx, y + speed * vy)


        update_duck_position(duck)
        sprite_manager.draw_game_scene(duck)

        #TODO

        #ammo = 1
        #ducks = ["", "", "", "hit", "hit", "hit", "", "", "", ""]
        #score = 150
        sprite_manager.draw_interface(ammo, ducks, score)
        sprite_manager.draw_new_round(round_num)

    sprite_manager.draw_cursor()
    pygame.display.update()
    clock.tick(30)

pygame.quit()
