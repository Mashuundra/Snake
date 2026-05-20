"""
Модульные тесты для класса GameEngine
"""

import pytest
import random
from core.game import GameEngine, GameStatus


class TestGameInitialization:
    """Тесты инициализации игры"""

    def test_create_game_empty_map(self):
        game = GameEngine(20, 20, map_type="empty")
        assert game.width == 20
        assert game.height == 20
        assert game.score == 0
        assert game.status == GameStatus.PLAYING
        assert game.food_position is not None
        assert game.map_type == "empty"

    def test_create_game_obstacles_map(self):
        game = GameEngine(20, 20, map_type="obstacles")
        assert game.map_type == "obstacles"
        assert len(game.obstacles) > 0

    def test_snake_in_center(self):
        game = GameEngine(10, 10)
        center_x = 10 // 2
        center_y = 10 // 2
        assert game.snake_body[0] == (center_x, center_y)

    def test_food_not_on_snake(self):
        game = GameEngine(10, 10)
        assert game.food_position not in game.snake_body

    def test_minimal_field_size(self):
        game = GameEngine(5, 5)
        assert game.width == 5
        assert game.height == 5

    def test_large_field_size(self):
        game = GameEngine(50, 50)
        assert game.width == 50
        assert game.height == 50


class TestGameTeleportation:
    """Тесты телепортации через границы"""

    def test_teleport_right_wall(self):
        game = GameEngine(10, 10, map_type="empty")
        game._snake._body = [(9, 5)]
        game._snake._direction = (1, 0)
        game._snake._next_direction = (1, 0)
        game.update()
        assert game.snake_body[0] == (0, 5)
        assert game.status == GameStatus.PLAYING

    def test_teleport_left_wall(self):
        game = GameEngine(10, 10, map_type="empty")
        game._snake._body = [(0, 5)]
        game._snake._direction = (-1, 0)
        game._snake._next_direction = (-1, 0)
        game.update()
        assert game.snake_body[0] == (9, 5)
        assert game.status == GameStatus.PLAYING

    def test_teleport_up_wall(self):
        game = GameEngine(10, 10, map_type="empty")
        game._snake._body = [(5, 0)]
        game._snake._direction = (0, -1)
        game._snake._next_direction = (0, -1)
        game.update()
        assert game.snake_body[0] == (5, 9)
        assert game.status == GameStatus.PLAYING

    def test_teleport_down_wall(self):
        game = GameEngine(10, 10, map_type="empty")
        game._snake._body = [(5, 9)]
        game._snake._direction = (0, 1)
        game._snake._next_direction = (0, 1)
        game.update()
        assert game.snake_body[0] == (5, 0)
        assert game.status == GameStatus.PLAYING


class TestGameObstacles:
    """Тесты карты с препятствиями"""

    def test_obstacles_exist(self):
        game = GameEngine(15, 15, map_type="obstacles")
        assert len(game.obstacles) > 0

    def test_obstacle_collision(self):
        game = GameEngine(15, 15, map_type="obstacles")
        obstacle = list(game.obstacles)[0]
        obstacle_x, obstacle_y = obstacle
        game._snake._body = [(obstacle_x - 1, obstacle_y)]
        game._snake._direction = (1, 0)
        game._snake._next_direction = (1, 0)
        game.update()
        assert game.status == GameStatus.GAME_OVER

    def test_empty_map_no_obstacles(self):
        game = GameEngine(15, 15, map_type="empty")
        assert len(game.obstacles) == 0

    def test_food_not_on_obstacles(self):
        game = GameEngine(10, 10, map_type="obstacles")
        assert game.food_position not in game.obstacles


class TestGameMovement:
    """Тесты движения в игре"""

    def test_move_right(self):
        game = GameEngine(20, 20)
        old_head = game.snake_body[0]
        game.change_direction(1, 0)
        game.update()
        new_head = game.snake_body[0]
        assert new_head == (old_head[0] + 1, old_head[1])

    def test_cannot_reverse_direction(self):
        game = GameEngine(20, 20)
        old_head = game.snake_body[0]
        game.change_direction(-1, 0)
        game.update()
        new_head = game.snake_body[0]
        assert new_head == (old_head[0] + 1, old_head[1])

    def test_move_up(self):
        game = GameEngine(20, 20)
        old_head = game.snake_body[0]
        game.change_direction(0, -1)
        game.update()
        new_head = game.snake_body[0]
        assert new_head == (old_head[0], old_head[1] - 1)

    def test_move_down(self):
        game = GameEngine(20, 20)
        old_head = game.snake_body[0]
        game.change_direction(0, 1)
        game.update()
        new_head = game.snake_body[0]
        assert new_head == (old_head[0], old_head[1] + 1)


class TestGameCollisions:
    """Тесты столкновений (старые — теперь это победа, а не смерть)"""

    def test_no_wall_death_on_empty_map(self):
        """На пустой карте стены не убивают, а телепортируют"""
        game = GameEngine(5, 5, map_type="empty")
        game._snake._body = [(4, 2)]
        game._snake._direction = (1, 0)
        game.update()
        assert game.status == GameStatus.PLAYING  # не умер, телепортировался

    def test_self_collision(self):
        game = GameEngine(10, 10)
        game._snake._body = [(5, 5), (4, 5), (3, 5), (2, 5)]
        game._snake._direction = (-1, 0)
        game._snake._next_direction = (-1, 0)
        game.update()
        game.update()
        game._snake._direction = (1, 0)
        game._snake._next_direction = (1, 0)
        game.update()
        assert game.status == GameStatus.GAME_OVER


class TestGameFood:
    """Тесты еды"""

    def test_eat_food_increases_score(self):
        game = GameEngine(10, 10)
        head_x, head_y = game.snake_body[0]
        game._food = (head_x + 1, head_y)
        old_score = game.score
        game.update()
        assert game.score == old_score + 1

    def test_eat_food_increases_snake_length(self):
        game = GameEngine(10, 10)
        head_x, head_y = game.snake_body[0]
        game._food = (head_x + 1, head_y)
        old_length = len(game.snake_body)
        game.update()
        assert len(game.snake_body) == old_length + 1

    def test_eat_food_generates_new_food(self):
        game = GameEngine(10, 10)
        head_x, head_y = game.snake_body[0]
        old_food = game.food_position
        game._food = (head_x + 1, head_y)
        game.update()
        assert game.food_position != old_food

    def test_new_food_not_on_snake(self):
        game = GameEngine(10, 10)
        head_x, head_y = game.snake_body[0]
        game._food = (head_x + 1, head_y)
        game.update()
        assert game.food_position not in game.snake_body

    def test_food_can_appear_on_edges(self):
        """На пустой карте еда может быть на краю"""
        game = GameEngine(10, 10, map_type="empty")
        # Заполняем всё поле, кроме клетки (0,0)
        all_cells = [(x, y) for x in range(10) for y in range(10)]
        game._snake._body = all_cells[1:]  # все кроме (0,0)
        game._generate_food()
        assert game.food_position == (0, 0)  # еда на краю


class TestGameWin:
    """Тесты победы"""

    def test_win_when_no_free_cells(self):
        game = GameEngine(3, 3)
        all_cells = [(x, y) for x in range(3) for y in range(3)]
        game._snake._body = all_cells
        game._generate_food()
        assert game.status == GameStatus.WIN
        assert game.food_position is None


class TestGameReset:
    """Тесты сброса игры"""

    def test_reset_resets_score(self):
        game = GameEngine(10, 10)
        game._score = 100
        game.reset()
        assert game.score == 0

    def test_reset_resets_snake_position(self):
        game = GameEngine(10, 10)
        game._snake._body = [(99, 99), (98, 99)]
        game.reset()
        center_x = 10 // 2
        center_y = 10 // 2
        assert game.snake_body[0] == (center_x, center_y)
        assert len(game.snake_body) == 1

    def test_reset_resets_status(self):
        game = GameEngine(10, 10)
        game._status = GameStatus.GAME_OVER
        game.reset()
        assert game.status == GameStatus.PLAYING

    def test_reset_generates_new_food(self):
        game = GameEngine(10, 10)
        game.reset()
        assert game.food_position is not None
        assert game.food_position not in game.snake_body

    def test_reset_changes_map_type(self):
        game = GameEngine(10, 10, map_type="empty")
        game.reset(map_type="obstacles")
        assert game.map_type == "obstacles"
        assert len(game.obstacles) > 0

    def test_reset_clears_obstacles_when_switching_to_empty(self):
        game = GameEngine(10, 10, map_type="obstacles")
        assert len(game.obstacles) > 0
        game.reset(map_type="empty")
        assert len(game.obstacles) == 0
        assert game.map_type == "empty"


class TestGameDirectionChanges:
    """Тесты смены направления в игре"""

    def test_change_direction_ignored_after_game_over(self):
        game = GameEngine(10, 10)
        game._status = GameStatus.GAME_OVER
        old_direction = game._snake.direction
        game.change_direction(1, 0)
        assert game._snake.direction == old_direction

    def test_change_direction_works_during_game(self):
        game = GameEngine(10, 10)
        game.change_direction(0, 1)
        game.update()
        assert game._snake.direction == (0, 1)


class TestGameBoundaries:
    """Тесты граничных условий"""

    def test_update_does_nothing_when_game_over(self):
        game = GameEngine(10, 10)
        game._status = GameStatus.GAME_OVER
        old_head = game.snake_body[0]
        game.update()
        assert game.snake_body[0] == old_head

    def test_update_does_nothing_when_win(self):
        game = GameEngine(10, 10)
        game._status = GameStatus.WIN
        old_head = game.snake_body[0]
        game.update()
        assert game.snake_body[0] == old_head
