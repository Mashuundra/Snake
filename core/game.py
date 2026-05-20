"""
Игровой движок: связывает змейку, еду, проверяет условия победы/поражения.
"""

import random
from enum import Enum
from typing import Optional, Tuple, Set

from core.snake import Snake


class GameStatus(Enum):
    """Состояния игры"""
    PLAYING = "playing"
    GAME_OVER = "game_over"
    WIN = "win"


class GameEngine:
    """Главный игровой движок"""

    def __init__(self, width: int, height: int, map_type: str = "empty"):
        """Инициализация игры"""
        self._width = width
        self._height = height
        self._map_type = map_type  # тип карты

        # Создаём змейку в центре поля
        start_x = width // 2
        start_y = height // 2
        self._snake = Snake(start_x, start_y)

        # Счёт
        self._score = 0

        # Статус игры
        self._status = GameStatus.PLAYING

        # Препятствия для карты "obstacles"
        self._obstacles: Set[Tuple[int, int]] = set()

        if map_type == "obstacles":
            self._generate_obstacles()

        # Позиция еды
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
        """Генерирует препятствия для карты obstacles"""
        self._obstacles = set()

        margin = 3
        for x in range(margin, self._width - margin):
            self._obstacles.add((x, margin))
            self._obstacles.add((x, self._height - margin - 1))
        for y in range(margin, self._height - margin):
            self._obstacles.add((margin, y))
            self._obstacles.add((self._width - margin - 1, y))

        # Убираем препятствия, которые на стартовой позиции змейки
        for segment in self._snake.body:
            self._obstacles.discard(segment)

    def _generate_food(self) -> None:
        """Генерирует еду в случайной свободной клетке"""
        # Получаем все занятые клетки
        occupied: Set[Tuple[int, int]] = set(self._snake.body)

        # Для карты с препятствиями — добавляем препятствия
        if self._map_type == "obstacles":
            occupied.update(self._obstacles)

        # Находим все свободные клетки
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
        # Игнорируем смену направления, если игра окончена
        if self._status != GameStatus.PLAYING:
            return

        self._snake.set_direction(dx, dy)

    def _check_obstacle_collision(self) -> bool:
        """Проверяет столкновение с препятствиями"""
        if self._map_type != "obstacles":
            return False
        return self._snake.head in self._obstacles

    def _check_food_collision(self) -> bool:
        """Проверяет, съела ли змейка еду"""
        return self._snake.head == self._food

    def _calculate_new_head_with_teleport(self) -> Tuple[int, int]:
        """Вычисляет новую позицию головы с учётом телепортации"""
        head_x, head_y = self._snake.head
        dx, dy = self._snake._next_direction

        new_x = head_x + dx
        new_y = head_y + dy

        # Телепортация
        if new_x < 0:
            new_x = self._width - 1
        elif new_x >= self._width:
            new_x = 0

        if new_y < 0:
            new_y = self._height - 1
        elif new_y >= self._height:
            new_y = 0

        return (new_x, new_y)

    def _handle_food_eaten(self) -> None:
        """Обрабатывает съедание еды: рост, увеличение счёта, генерация новой еды"""
        self._snake.grow()
        self._score += 1
        self._generate_food()

    def update(self) -> None:
        """Обновляет состояние игры на один шаг"""
        if self._status != GameStatus.PLAYING:
            return

        # Вычисляем новую голову с телепортацией
        new_head = self._calculate_new_head_with_teleport()

        # Применяем движение
        self._snake.move_with_teleport(new_head)

        # Проверка столкновения с препятствиями
        if self._check_obstacle_collision():
            self._status = GameStatus.GAME_OVER
            return

        # Проверка столкновения с собой
        if self._snake.check_self_collision():
            self._status = GameStatus.GAME_OVER
            return

        # Проверка съедания еды
        if self._check_food_collision():
            self._handle_food_eaten()

    def reset(self, map_type: str = None) -> None:
        """Полностью сбрасывает игру до начального состояния"""
        if map_type:
            self._map_type = map_type
            if map_type == "obstacles":
                self._obstacles = set()
                self._generate_obstacles()
            else:
                self._obstacles = set()

        # Сбрасываем змейку
        start_x = self._width // 2
        start_y = self._height // 2
        self._snake = Snake(start_x, start_y)

        # Сбрасываем счёт
        self._score = 0

        # Сбрасываем статус
        self._status = GameStatus.PLAYING

        # Генерируем новую еду
        self._generate_food()
