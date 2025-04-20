import pygame
import pytest
from unittest.mock import MagicMock, patch
from DuckHunt.sprite_manager import SpriteManager  

@pytest.fixture
def mock_screen():
    # Створюємо фейковий екран для тестування
    screen = MagicMock()
    screen.get_size.return_value = (800, 600)
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    return screen

@pytest.fixture
def sprite_manager(mock_screen):
    # Патчимо методи, які завантажують зображення, щоб не завантажувати їх насправді
    with patch.object(SpriteManager, 'load_fonts'), \
         patch.object(SpriteManager, 'load_clouds'), \
         patch.object(SpriteManager, 'load_crown'), \
         patch.object(SpriteManager, 'load_game_scene'), \
         patch.object(SpriteManager, 'load_interface'), \
         patch.object(SpriteManager, 'load_cursor'), \
         patch.object(SpriteManager, 'load_buttons'), \
         patch.object(SpriteManager, 'load_dog'), \
         patch.object(SpriteManager, 'load_all_ducks'), \
         patch.object(SpriteManager, 'init_clouds'):
        return SpriteManager(mock_screen)

def test_toggle_leaderboard(sprite_manager):
    initial_state = sprite_manager.leaderboard_toggled
    sprite_manager.toggle_leaderboard()
    
    # Перевіряємо, що стан змінився
    assert sprite_manager.leaderboard_toggled == (not initial_state)

def test_start_transition(sprite_manager):
    sprite_manager.transition_active = False
    sprite_manager.camera_y = 100
    sprite_manager.start_transition()

    # Перевіряємо, що активовано перехід
    assert sprite_manager.transition_active is True
    # Перевіряємо, що камера перемістилася
    assert sprite_manager.camera_y == 0

def test_move_camera_down(sprite_manager):
    sprite_manager.transition_active = True
    sprite_manager.camera_y = 0
    sprite_manager.ground_y = 0

    mock_ground_image = MagicMock()
    mock_ground_image.get_height.return_value = 100
    sprite_manager.ground_image = mock_ground_image

    sprite_manager.move_camera_down()
    
    # Перевіряємо, що камера перемістилася вниз
    assert sprite_manager.camera_y == sprite_manager.transition_speed

    # Повертаємося до початкового стану для тесту if 2,3
    sprite_manager.camera_y = 0

    mock_screen = MagicMock()
    mock_screen.get_height.return_value = 500
    sprite_manager.screen = mock_screen

    # Переміщаємо камеру до значення, яке дозволить пройти через другий if
    sprite_manager.camera_y = 400  
    sprite_manager.move_camera_down()

    # ground_y має бути збільшено на transition_speed
    assert sprite_manager.ground_y == sprite_manager.transition_speed  

    # Переміщаємо камеру до значення, яке дозволить пройти через третій if
    # Тепер camera_y має бути на рівні висоти екрану
    sprite_manager.camera_y = 500  
    sprite_manager.move_camera_down()

    # ground_y має бути рівним висоті зображення землі
    assert sprite_manager.ground_y == mock_ground_image.get_height.return_value  
    # transition_active має стати False
    assert not sprite_manager.transition_active  
    # camera_y має дорівнювати висоті екрану
    assert sprite_manager.camera_y == mock_screen.get_height.return_value  

def test_spawn_cloud(sprite_manager):
    pygame.init()
    
    fake_surface = pygame.Surface((50, 30))
    sprite_manager.cloud_images = [fake_surface]

    sprite_manager.spawn_cloud()

    # Перевіряємо, що хмара була створена
    assert len(sprite_manager.clouds) == 1
    cloud = sprite_manager.clouds[0]

    # Перевіряємо, що хмара має правильні атрибути
    assert cloud["x"] == -fake_surface.get_width()
    assert 0 <= cloud["y"] <= sprite_manager.screen.get_height()
    assert 0.5 <= cloud["speed"] <= 1.25 # параметри швидкості в межах 0.5 і 1.25 - описані в класі

def test_move_clouds_removes_and_spawns_new(sprite_manager):
    pygame.init()

    # Створюємо зображення хмари
    fake_surface = pygame.Surface((50, 30))
    sprite_manager.cloud_images = [fake_surface]

    # Встановлюємо хмаринку за межами екрану, щоб вона мала бути видалена
    sprite_manager.clouds = [{
        "x": 801,  # екран шириною 800
        "y": 100,
        "speed": 1,
        "image": fake_surface
    }]

    sprite_manager.move_clouds()

    # Має бути створено нову хмару (видалили стару - додали нову)
    assert len(sprite_manager.clouds) == 1
    new_cloud = sprite_manager.clouds[0]

    # Перевіримо, що координата x нового зображення = -ширина зображення
    assert new_cloud["x"] == -fake_surface.get_width()
    
@pytest.mark.parametrize(
    "number, max_digits, expected",
    [
        (123, None, [0, 0, 0, 1, 2, 3]),
        (789456, 3, [7, 8, 9, 4, 5, 6]),
        (789456, 8, [0, 0, 7, 8, 9, 4, 5, 6])
    ]
)
def test_get_digits(number, max_digits, expected):
    # Якщо max_digits передано, то функція має повертати max_digits цифр.
    # Якщо в числі менше ,ax_digits цифр, то на початку мають бути нул
    if max_digits is not None:
        result = SpriteManager.get_digits(number, max_digits=max_digits)
    # Якщо max_digits не передано, то функція має повертати 6 цифр.
    # Якщо в числі менше 6 цифр, то на початку мають бути нулі
    else:
        result = SpriteManager.get_digits(number)
    assert result == expected
