import pygame
import random


class Dog:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_laughing = False
        self.animation_frame = 0
        self.last_frame_update = 0
        self.position = (0, 0)
        self.reset_position()

    def reset_position(self) -> None:
        """Встановлює початкову позицію"""
        self.position = (
            random.randint(int(self.screen_width * 0.3), int(self.screen_width * 0.7)),
            int(self.screen_height * 0.6)
        )

    def update(self, current_time: int) -> None:
        """Оновлює анімацію"""
        if self.is_laughing and current_time - self.last_frame_update > 300:
            self.last_frame_update = current_time
            self.animation_frame = (self.animation_frame + 1) % 2

    def start_laughing(self) -> None:
        """Починає анімацію сміху"""
        self.is_laughing = True
        self.animation_frame = 0
        self.last_frame_update = pygame.time.get_ticks()

    def stop_laughing(self) -> None:
        """Зупиняє анімацію сміху"""
        self.is_laughing = False
        self.animation_frame = 0