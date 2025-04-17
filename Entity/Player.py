class Player:
    """Клас гравця, який зберігає інформацію про ім'я та очки"""

    def __init__(self, name: str = "Player"):
        self.player_name = name  # Ім'я гравця
        self.points = 0  # Поточні очки
        self.max_points = 0  # Максимальні очки за сесію

    def add_points(self, amount: int) -> None:
        """Додає очки гравцю та оновлює максимальний рахунок"""
        self.points += amount
        self.check_max_points()

    def check_max_points(self) -> None:
        """Оновлює максимальний рахунок, якщо поточний більший"""
        if self.points > self.max_points:
            self.max_points = self.points