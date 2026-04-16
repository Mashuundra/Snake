"""
Модель змейки: движение, рост, проверка столкновений.
"""

from typing import List, Tuple


class Snake:
    """Класс, управляющий поведением змейки"""

    def __init__(self, start_x: int, start_y: int):
        """Инициализация змейки"""
        self._body: List[Tuple[int, int]] = [(start_x, start_y)]
        self._direction: Tuple[int, int] = (1, 0)
        self._next_direction: Tuple[int, int] = (1, 0)
        self._grow_flag: bool = False

    @property
    def body(self) -> List[Tuple[int, int]]:
        """Возвращает копию тела змейки (для безопасного доступа извне)"""
        return self._body.copy()

    @property
    def head(self) -> Tuple[int, int]:
        """Возвращает координаты головы змейки"""
        return self._body[0]

    @property
    def direction(self) -> Tuple[int, int]:
        """Возвращает текущее направление движения"""
        return self._direction

    @property
    def length(self) -> int:
        """Возвращает длину змейки"""
        return len(self._body)

    def move(self) -> None:
        """Перемещает змейку на один шаг в текущем направлении."""
        self._direction = self._next_direction
        dx, dy = self._direction
        head_x, head_y = self.head
        new_head = (head_x + dx, head_y + dy)

        self._body.insert(0, new_head)

        if self._grow_flag:
            self._grow_flag = False
        elif len(self._body) > 2:
            self._body.pop()

    def set_direction(self, dx: int, dy: int) -> None:
        """Устанавливает новое направление движения змейки"""
        if not self._is_valid_direction(dx, dy):
            return

        new_dir = (dx, dy)
        current_dir = self._direction

        if (new_dir[0] == -current_dir[0] and new_dir[1] == -current_dir[1]):
            return

        self._next_direction = new_dir

    def _is_valid_direction(self, dx: int, dy: int) -> bool:
        """Проверяет, является ли направление допустимым"""
        if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
            return False

        if dx != 0 and dy != 0:
            return False

        if dx == 0 and dy == 0:
            return False

        return True

    def grow(self) -> None:
        """Увеличивает длину змейки"""
        self._grow_flag = True

    def check_self_collision(self) -> bool:
        """Проверяет, столкнулась ли голова змейки с её телом"""
        return self.head in self._body[1:]
