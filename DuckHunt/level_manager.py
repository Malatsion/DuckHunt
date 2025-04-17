class LevelManager:
    def __init__(self, fast_ducks_mode=False, no_reload_mode=False):
        self.level = 1  # Початковий рівень
        self.speed_multiplier = 1.0  # Початковий коефіцієнт швидкості
        self.fast_ducks_mode = fast_ducks_mode  # Режим пришвидшених качок
        self.no_reload_mode = no_reload_mode #Режим без перезарядки
        self.increment = 0.1  # Збільшення швидкості на рівень
        self.set_mode(fast_ducks_mode, no_reload_mode)  # Використовуємо метод для встановлення режиму

    def set_mode(self, fast_ducks_mode, no_reload_mode):
        """Змінює режим гри та скидає параметри."""
        self.fast_ducks_mode = fast_ducks_mode
        self.no_reload_mode = no_reload_mode
        self.reset() #метод reset() допомагає встановити бажану швидкість. якщо обрано відповідний режим

    def next_level(self):
        """Підвищує рівень та збільшує швидкість качки."""
        self.level += 1
        self.speed_multiplier += self.increment

    def reset(self):
        """Скидає рівень та швидкість до початкових значень."""
        self.level = 1
        self.speed_multiplier = 1.2 if self.fast_ducks_mode or self.no_reload_mode else 1.0
        self.increment = 0.2 if self.fast_ducks_mode or self.no_reload_mode else 0.1

    def get_level(self):
        """Повертає поточний рівень."""
        return self.level

    def get_speed_multiplier(self):
        """Повертає поточний коефіцієнт швидкості."""
        return self.speed_multiplier

    def check_no_reload_mode(self):
        """Перевірка на увімкнення no_reload_mode для подальшої логіки у файлі main_cycle"""
        return self.no_reload_mode
