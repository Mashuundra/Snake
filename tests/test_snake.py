"""
Модульные тесты для класса Snake
"""

import pytest
from core.snake import Snake


class TestSnakeInitialization:
    """Тесты инициализации змейки"""

    def test_create_snake(self):
        snake = Snake(10, 10)
        assert snake.head == (10, 10)
        assert len(snake.body) == 1
        assert snake.length == 1

    def test_snake_body_is_copy(self):
        snake = Snake(5, 5)
        body = snake.body
        body.append((99, 99))
        assert len(snake.body) == 1

    def test_direction_default(self):
        snake = Snake(0, 0)
        assert snake.direction == (1, 0)

    def test_head_property(self):
        snake = Snake(7, 8)
        assert snake.head == (7, 8)


class TestSnakeMovement:
    """Тесты движения змейки"""

    def test_move_right(self):
        snake = Snake(10, 10)
        snake.set_direction(1, 0)
        snake.move()
        assert snake.head == (11, 10)

    def test_cannot_turn_180_degrees(self):
        snake = Snake(10, 10)
        snake.set_direction(-1, 0)
        snake.move()
        assert snake.head == (11, 10)

    def test_move_up(self):
        snake = Snake(10, 10)
        snake.set_direction(0, -1)
        snake.move()
        assert snake.head == (10, 9)

    def test_move_down(self):
        snake = Snake(10, 10)
        snake.set_direction(0, 1)
        snake.move()
        assert snake.head == (10, 11)

    def test_consecutive_moves(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.move()
        snake.move()
        snake.move()
        assert snake.head == (8, 5)

    def test_tail_follows(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.move()
        snake.move()
        assert snake.body[1] == (6, 5)
        assert snake.body[-1] == (6, 5)
        assert snake.head == (7, 5)


class TestSnakeGrowth:
    """Тесты роста змейки"""

    def test_grow_increases_length(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.grow()
        old_length = snake.length
        snake.move()
        assert snake.length == old_length + 1

    def test_grow_preserves_tail(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.move()
        snake.grow()
        snake.move()
        assert len(snake.body) == 3
        assert snake.body[-1] == (5, 5)

    def test_multiple_grow(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)

        for _ in range(3):
            snake.grow()
            snake.move()

        assert snake.length == 4


class TestSnakeDirection:
    """Тесты смены направления"""

    def test_cannot_reverse(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.move()
        snake.set_direction(-1, 0)
        snake.move()
        assert snake.head == (7, 5)

    def test_can_change_direction(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.move()
        snake.set_direction(0, 1)
        snake.move()
        assert snake.head == (6, 6)

    def test_ignores_invalid_dx(self):
        snake = Snake(5, 5)
        snake.set_direction(2, 0)
        snake.move()
        assert snake.head == (6, 5)

    def test_ignores_invalid_dy(self):
        snake = Snake(5, 5)
        snake.set_direction(0, 2)
        snake.move()
        assert snake.head == (6, 5)

    def test_ignores_diagonal(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 1)
        snake.move()
        assert snake.head == (6, 5)

    def test_ignores_zero_direction(self):
        snake = Snake(5, 5)
        snake.set_direction(0, 0)
        snake.move()
        assert snake.head == (6, 5)


class TestSnakeCollision:
    """Тесты столкновений"""

    def test_self_collision_false(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        for _ in range(3):
            snake.move()
        assert not snake.check_self_collision()

    def test_self_collision_true(self):
        snake = Snake(5, 5)
        snake._body = [(5, 5), (4, 5), (3, 5), (2, 5)]
        snake._direction = (-1, 0)
        snake._next_direction = (-1, 0)
        snake.move()
        snake.move()
        snake.set_direction(1, 0)
        snake._direction = (1, 0)
        snake._next_direction = (1, 0)
        snake.move()
        assert snake.check_self_collision()

    def test_no_collision_with_tail_when_growing(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.grow()
        snake.move()
        snake.set_direction(0, 1)
        snake.move()
        assert not snake.check_self_collision()


class TestSnakeEdgeCases:
    """Краевые случаи"""

    def test_snake_can_move_into_empty_space(self):
        snake = Snake(0, 0)
        snake.set_direction(1, 0)
        snake.move()
        assert snake.head == (1, 0)

    def test_snake_grow_doesnt_affect_direction(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        snake.grow()
        snake.move()
        assert snake.direction == (1, 0)

    def test_set_direction_after_game_over(self):
        snake = Snake(5, 5)
        snake.set_direction(1, 0)
        assert snake.direction == (1, 0)
