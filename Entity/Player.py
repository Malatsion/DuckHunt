class Player:
    def __init__(self, name: str = "Player"):
        self.name = name
        self.score = 0
        self.max_score = 0
        self.ammo = 3
        self.ducks_shot = 0
        self.round = 1

    def add_score(self, points: int) -> None:
        """Додає очки до рахунку"""
        self.score += points
        if self.score > self.max_score:
            self.max_score = self.score

    def use_ammo(self) -> None:
        """Використовує один патрон"""
        if self.ammo > 0:
            self.ammo -= 1

    def reload(self) -> None:
        """Перезаряджає зброю"""
        self.ammo = 3

    def duck_shot(self) -> None:
        """Збільшує лічильник збитих качок"""
        self.ducks_shot += 1
