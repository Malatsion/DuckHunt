import pytest
from ..Entity.Player import Player


@pytest.fixture
def player():
    """Фікстура для створення гравця перед кожним тестом"""
    return Player("TestPlayer")


def test_player_initialization(player):
    """Тестує коректність ініціалізації гравця"""
    assert player.player_name == "TestPlayer"
    assert player.points == 0
    assert player.max_points == 0


def test_points_accumulation(player):
    """Тестує послідовне накопичення очок"""
    # Перше додавання
    player.add_points(10)
    assert player.points == 10
    assert player.max_points == 10

    # Додаємо ще 5
    player.add_points(5)
    assert player.points == 15
    assert player.max_points == 15

    # Віднімаємо 3
    player.add_points(-3)
    assert player.points == 12
    assert player.max_points == 15  # Максимум залишається 15

    # Додаємо 20
    player.add_points(20)
    assert player.points == 32
    assert player.max_points == 32  # Новий максимум


def test_max_points_not_decreasing(player):
    """Тестує, що максимальний рахунок не зменшується"""
    player.add_points(10)
    assert player.max_points == 10  # points=10, max=10

    player.add_points(-5)
    assert player.max_points == 10  # points=5, max=10

    player.add_points(3)
    assert player.max_points == 10  # points=8, max=10

    player.add_points(15)
    assert player.max_points == 23  # points=23, max=23 (бо 23 > 10)


def test_negative_points(player):
    """Тестує віднімання очок"""
    player.add_points(20)
    player.add_points(-5)
    assert player.points == 15
    assert player.max_points == 20  # Максимум залишається 20


def test_multiple_operations(player):
    """Тестує комплекс операцій"""
    player.add_points(10)
    player.add_points(5)
    player.add_points(-3)
    player.add_points(20)
    player.add_points(-10)
    assert player.points == 22
    assert player.max_points == 32