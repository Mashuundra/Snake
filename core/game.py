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

    def __init__(self, width: int, height: int):
        """Инициализация игры"""
        self._width = width
        self._height = height

        # Создаём змейку в центре поля
        start_x = width // 2
        start_y = height // 2
        self._snake = Snake(start_x, start_y)

        # Счёт
        self._score = 0

        # Статус игры
        self._status = GameStatus.PLAYING

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

    def _generate_food(self) -> None:
        """Генерирует еду в случайной свободной клетке"""
        # Получаем все занятые клетки
        occupied: Set[Tuple[int, int]] = set(self._snake.body)

        # Находим все свободные клетки
        free_cells = []
        for x in range(1, self._width - 1):
            for y in range(1, self._height - 1):
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

    def _check_wall_collision(self) -> bool:
        """Проверяет столкновение со стенами"""
        head_x, head_y = self._snake.head
        return (head_x <= 0 or head_x >= self._width - 1 or
                head_y <= 0 or head_y >= self._height - 1)

    def _check_food_collision(self) -> bool:
        """Проверяет, съела ли змейка еду"""
        return self._snake.head == self._food

    def _handle_food_eaten(self) -> None:
        """Обрабатывает съедание еды: рост, увеличение счёта, генерация новой еды"""
        self._snake.grow()
        self._score += 1
        self._generate_food()

    def update(self) -> None:
        """Обновляет состояние игры на один шаг"""
        if self._status != GameStatus.PLAYING:
            return

        # Двигаем змейку
        self._snake.move()

        # Проверка столкновения со стенами
        if self._check_wall_collision():
            self._status = GameStatus.GAME_OVER
            return

        # Проверка столкновения с собой
        if self._snake.check_self_collision():
            self._status = GameStatus.GAME_OVER
            return

        # Проверка съедания еды
        if self._check_food_collision():
            self._handle_food_eaten()

    def reset(self) -> None:
        """Полностью сбрасывает игру до начального состояния"""
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
