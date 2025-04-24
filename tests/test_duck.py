import pytest
from Entity.Duck import Duck

@pytest.fixture
def duck():
    """Фікстура для створення екземпляру качки перед кожним тестом"""
    return Duck((100, 100), 800, 600)

@pytest.mark.parametrize("initial_pos,expected_status", [
    ((100, 100), "alive"),  # Качка в межах екрану
    ((-100, 100), "escaped"),  # Качка за лівою межею
    ((900, 100), "escaped"),  # Качка за правою межею
    ((100, -100), "escaped"),  # Качка за верхньою межею
    ((100, 700), "escaped"),  # Качка за нижньою межею
])
def test_duck_escape(initial_pos, expected_status):
    """Параметризований тест для перевірки вильоту за межі екрану"""
    duck = Duck(initial_pos, 800, 600)
    duck.update(0)  # Оновлення стану
    assert duck.status == expected_status  # Перевірка очікуваного статусу

def test_duck_initialization(duck):
    """Тестує коректність ініціалізації об'єкту Duck"""
    assert duck.position == [100, 100]  # Початкова позиція
    assert duck.screen_width == 800  # Ширина екрану
    assert duck.is_alive  # Качка жива
    assert duck.status == "alive"  # Статус "жива"
    assert not duck.bounce_mode  # Режим відскоку вимкнено
    assert duck.animation_frame == 0  # Початковий кадр анімації

def test_duck_movement(duck):
    """Тестує рух качки"""
    initial_x, initial_y = duck.position
    duck.update(0)  # Оновлення позиції
    # Перевірка, що позиція змінилася
    assert duck.position[0] != initial_x or duck.position[1] != initial_y

def test_duck_unalive(duck):
    """Тестує метод unalive() (коли качку збивають)"""
    duck.unalive()
    assert not duck.is_alive  # Качка нежива
    assert duck.status == "shot"  # Статус "збита"
    assert duck.speed_x == 0  # Рух по X зупинено
    assert duck.speed_y > 0  # Качка падає вниз