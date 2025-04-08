import random
import math
from typing import Tuple

class Duck:
    def __init__(self, color: str, position: Tuple[int, int], screen_width: int, screen_height: int):
        self.color = color  # "black", "red", "blue"
        self.position = list(position)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 50
        self.height = 50
        self.velocity = random.uniform(3, 7)
        self.direction = random.uniform(0, 2*math.pi)
        self.speed_x = math.cos(self.direction) * self.velocity
        self.speed_y = math.sin(self.direction) * self.velocity
        self.is_alive = True
        self.status = "alive"  # "alive", "shot", "escaped"
        self.bounce_mode = False
        self.shots_nearby = 0
        self.animation_frame = 0
        self.last_frame_update = 0

    def update(self, current_time: int) -> None:
        """Оновлює стан качки"""
        if not self.is_alive:
            return

        # Анімація польоту
        if current_time - self.last_frame_update > 150:  # 150ms між кадрами
            self.last_frame_update = current_time
            self.animation_frame = (self.animation_frame + 1) % 3

        # Випадкові зміни траєкторії
        if random.random() < (0.1 if self.bounce_mode else 0.05):
            self._change_direction()

        # Рух
        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

        # Обробка меж екрану
        if self.bounce_mode:
            self._handle_bouncing()
        elif self._is_escaped():
            self.escape()

    def _change_direction(self, intensity: float = 0.5) -> None:
        """Змінює напрямок польоту"""
        angle_change = random.uniform(-intensity, intensity)
        self.direction += angle_change
        self.speed_x = math.cos(self.direction) * self.velocity
        self.speed_y = math.sin(self.direction) * self.velocity

    def _handle_bouncing(self) -> None:
        """Обробка відскоків від країв екрану"""
        x, y = self.position
        bounced = False

        if x <= 0 or x >= self.screen_width - self.width:
            self.speed_x *= -1
            bounced = True
        if y <= 0 or y >= self.screen_height - self.height:
            self.speed_y *= -1
            bounced = True

        if bounced:
            self.direction = math.atan2(self.speed_y, self.speed_x)

    def _is_escaped(self) -> bool:
        """Перевіряє чи вилетіла за межі екрану"""
        x, y = self.position
        return (x < -self.width or x > self.screen_width + self.width or
                y < -self.height or y > self.screen_height + self.height)

    def register_shot_nearby(self) -> None:
        """Реєструє постріл поруч"""
        self.shots_nearby += 1
        if self.shots_nearby >= 2 and not self.bounce_mode:
            self.activate_bounce_mode()

    def activate_bounce_mode(self) -> None:
        """Активує режим відскоків"""
        self.bounce_mode = True
        self.velocity *= 1.3
        self._change_direction(1.0)

    def escape(self) -> None:
        """Качка втекла"""
        self.is_alive = False
        self.status = "escaped"

    def unalive(self) -> None:
        """Качка збита"""
        self.is_alive = False
        self.status = "shot"
        self.speed_x = 0
        self.speed_y = abs(self.velocity)