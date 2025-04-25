import pytest
from ..Entity.Dog import Dog
import pygame


@pytest.fixture
def dog():
    """Фікстура для створення екземпляру собаки перед кожним тестом"""
    pygame.init()
    pygame.display.set_mode((1, 1))  # Ініціалізація дисплею для pygame
    return Dog(800, 600)


def test_dog_initialization(dog):
    """Тестує коректність ініціалізації об'єкту Dog"""
    assert dog.screen_width == 800
    assert dog.screen_height == 600
    assert not dog.is_laughing  # Перевірка, що собака спочатку не сміється
    assert dog.animation_frame == 0  # Початковий кадр анімації
    assert dog.last_frame_update == 0  # Час останнього оновлення
    assert isinstance(dog.position, tuple)  # Позиція має бути кортежем
    assert len(dog.position) == 2  # Позиція - (x, y)


def test_dog_reset_position(dog):
    """Тестує метод reset_position()"""
    dog.reset_position()
    x, y = dog.position
    # Перевірка, що позиція в межах екрану (30%-70% ширини, 60% висоти)
    assert 240 <= x <= 560  # 0.3*800=240, 0.7*800=560
    assert y == 360  # 0.6*600=360


def test_dog_laughing_animation(dog):
    """Тестує анімацію сміху собаки"""
    dog.start_laughing()
    assert dog.is_laughing
    assert dog.animation_frame == 0

    mock_time = 1000
    dog.update(mock_time)
    assert dog.last_frame_update == mock_time

    # Через 200мс кадр змінюється
    dog.update(mock_time + 200)
    assert dog.animation_frame == 1  # Змінюємо очікування на 1
