# core/game.py
"""
Игровой движок: связывает змейку, еду, проверяет условия победы/поражения.
"""

import random
from enum import Enum
from typing import Optional, Tuple, Set

from core.snake import Snake
import config as cfg


class GameStatus(Enum):
    """Состояния игры"""
    PLAYING = "playing"
    GAME_OVER = "game_over"
    WIN = "win"


class GameEngine:
    """Главный игровой движок"""

    def __init__(self, width: int, height: int, map_type: str = cfg.MAP_EMPTY):
        """Инициализация игры"""
        self._width = width
        self._height = height
        self._map_type = map_type

        # Создаём змейку в центре поля
        start_x = width // 2
        start_y = height // 2
        self._snake = Snake(start_x, start_y)

        self._score = 0
        self._status = GameStatus.PLAYING
        self._obstacles: Set[Tuple[int, int]] = set()

        if map_type == cfg.MAP_OBSTACLES:
            self._generate_obstacles()

        self._food: Optional[Tuple[int, int]] = None
        self._generate_food()

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def map_type(self) -> str:
        return self._map_type

    @property
    def obstacles(self) -> Set[Tuple[int, int]]:
        return self._obstacles.copy()

    @property
    def snake_body(self) -> list[tuple[int, int]]:
        return self._snake.body

    @property
    def food_position(self) -> Optional[Tuple[int, int]]:
        return self._food

    @property
    def score(self) -> int:
        return self._score

    @property
    def status(self) -> GameStatus:
        return self._status

    def _generate_obstacles(self) -> None:
        """Генерирует препятствия для карты obstacles (мало препятствий)"""
        self._obstacles = set()

        # Убедимся, что поле достаточно большое
        if self._width < 8 or self._height < 8:
            return

        import random

        # Всего 4-6 препятствий
        num_obstacles = random.randint(4, 6)

        # Начальная позиция змейки
        start_x = self._width // 2
        start_y = self._height // 2

        # Зоны, которые нельзя занимать препятствиями
        forbidden_zones = set()

        # Вся змейка
        for segment in self._snake.body:
            forbidden_zones.add(segment)

        # Окрестность вокруг головы (5x5)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                nx, ny = start_x + dx, start_y + dy
                if 0 <= nx < self._width and 0 <= ny < self._height:
                    forbidden_zones.add((nx, ny))

        # Генерируем препятствия
        attempts = 0
        while len(self._obstacles) < num_obstacles and attempts < 100:
            x = random.randint(2, self._width - 3)
            y = random.randint(2, self._height - 3)

            if (x, y) not in forbidden_zones and (x, y) not in self._obstacles:
                # Проверяем, чтобы препятствия не были рядом
                too_close = False
                for ox, oy in self._obstacles:
                    if abs(x - ox) <= 2 and abs(y - oy) <= 2:
                        too_close = True
                        break

                if not too_close:
                    self._obstacles.add((x, y))
            attempts += 1

    def _generate_food(self) -> None:
        """Генерирует еду в случайной свободной клетке"""
        occupied: Set[Tuple[int, int]] = set(self._snake.body)

        if self._map_type == cfg.MAP_OBSTACLES:
            occupied.update(self._obstacles)

        free_cells = []
        for x in range(self._width):
            for y in range(self._height):
                if (x, y) not in occupied:
                    free_cells.append((x, y))

        if free_cells:
            self._food = random.choice(free_cells)
        else:
            self._food = None
            self._status = GameStatus.WIN

    def change_direction(self, dx: int, dy: int) -> None:
        """Изменяет направление движения змейки"""
        if self._status != GameStatus.PLAYING:
            return
        self._snake.set_direction(dx, dy)

    def _check_obstacle_collision(self) -> bool:
        """Проверяет столкновение с препятствиями"""
        if self._map_type != cfg.MAP_OBSTACLES:
            return False
        return self._snake.head in self._obstacles

    def _calculate_new_head_with_teleport(self) -> Tuple[int, int]:
        """Вычисляет новую позицию головы с учётом телепортации"""
        head_x, head_y = self._snake.head
        dx, dy = self._snake._next_direction

        new_x = head_x + dx
        new_y = head_y + dy

        # Телепортация (для пустой карты)
        if new_x < 0:
            new_x = self._width - 1
        elif new_x >= self._width:
            new_x = 0

        if new_y < 0:
            new_y = self._height - 1
        elif new_y >= self._height:
            new_y = 0

        return (new_x, new_y)

    def _check_food_collision(self) -> bool:
        """Проверяет, съела ли змейка еду"""
        return self._snake.head == self._food

    def _handle_food_eaten(self) -> None:
        """Обрабатывает съедание еды"""
        self._snake.grow()
        self._score += 1
        self._generate_food()

    def update(self) -> None:
        """Обновляет состояние игры на один шаг"""
        if self._status != GameStatus.PLAYING:
            return

        new_head = self._calculate_new_head_with_teleport()
        self._snake.move_with_teleport(new_head)

        if self._check_obstacle_collision():
            self._status = GameStatus.GAME_OVER
            return

        if self._snake.check_self_collision():
            self._status = GameStatus.GAME_OVER
            return

        if self._check_food_collision():
            self._handle_food_eaten()

    def reset(self, map_type: str = None) -> None:
        """Полностью сбрасывает игру до начального состояния"""
        if map_type:
            self._map_type = map_type
            if map_type == cfg.MAP_OBSTACLES:
                self._obstacles = set()
                self._generate_obstacles()
            else:
                self._obstacles = set()

        start_x = self._width // 2
        start_y = self._height // 2
        self._snake = Snake(start_x, start_y)
        self._score = 0
        self._status = GameStatus.PLAYING
        self._generate_food()