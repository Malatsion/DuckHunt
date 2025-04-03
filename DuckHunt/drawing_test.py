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
        if event.type == pygame.MOUSEBUTTONDOWN and in_main_menu:
            in_main_menu = False
            in_transition = True
            sprite_manager.start_transition()

    if in_main_menu and pygame.key.get_pressed()[pygame.K_5]:
        sprite_manager.draw_game_over(15,150,19050)
    elif in_main_menu :
        sprite_manager.move_clouds()
        sprite_manager.draw_start_screen()
        sprite_manager.draw_leaderboard(leaderboard)
    elif in_transition:
        sprite_manager.move_clouds()
        sprite_manager.move_camera_down()
        sprite_manager.draw_game_scene()
        sprite_manager.draw_clouds()
        if not sprite_manager.transition_active:
            in_transition = False
            in_game = True
    elif in_game:
        sprite_manager.draw_game_scene()
        ammo = 1
        ducks = ["hit", "hit", "miss", "hit", "miss", "", "", "", "", ""]
        score = 150
        sprite_manager.draw_interface(ammo, ducks, score)
        sprite_manager.draw_new_round(4)

    
    sprite_manager.draw_cursor()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

