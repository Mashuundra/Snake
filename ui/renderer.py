"""
ui/renderer.py
Максимально простая пошаговая версия (нажимайте Enter после каждой команды)
"""

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as cfg
from core.game import GameEngine, GameStatus


class GameRenderer:
    def __init__(self, game: GameEngine):
        self._game = game

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _render(self):
        # Создаём поле
        field = [[cfg.SYMBOL_EMPTY for _ in range(self._game.width)]
                 for _ in range(self._game.height)]

        # Рисуем стены
        if cfg.DRAW_WALLS:
            for x in range(self._game.width):
                field[0][x] = cfg.SYMBOL_WALL
                field[self._game.height - 1][x] = cfg.SYMBOL_WALL
            for y in range(self._game.height):
                field[y][0] = cfg.SYMBOL_WALL
                field[y][self._game.width - 1] = cfg.SYMBOL_WALL

        # Рисуем еду
        if self._game.food_position:
            fx, fy = self._game.food_position
            field[fy][fx] = cfg.SYMBOL_FOOD

        # Рисуем змейку
        for i, (x, y) in enumerate(self._game.snake_body):
            if i == 0:
                field[y][x] = cfg.SYMBOL_SNAKE_HEAD
            else:
                field[y][x] = cfg.SYMBOL_SNAKE_BODY

        # Выводим поле
        print("┌" + "─" * self._game.width + "┐")
        for row in field:
            print("│" + "".join(row) + "│")
        print("└" + "─" * self._game.width + "┘")

    def run(self):
        controls = {
            'w': (0, -1), 'ц': (0, -1),  # Вверх
            's': (0, 1),  'ы': (0, 1),   # Вниз
            'a': (-1, 0), 'ф': (-1, 0),  # Влево
            'd': (1, 0),  'в': (1, 0)    # Вправо
        }

        while True:
            self._clear_screen()
            self._render()

            print(f"\nСчёт: {self._game.score} | Длина: {len(self._game.snake_body)}")

            if self._game.status != GameStatus.PLAYING:
                if self._game.status == GameStatus.GAME_OVER:
                    print("\n GAME OVER! ")
                else:
                    print("\n ПОБЕДА! ")
                print(f"Финальный счёт: {self._game.score}")
                print("\nНажмите R для рестарта, Q для выхода")

                cmd = input("> ").lower()
                if cmd == 'r':
                    self._game.reset()
                    continue
                elif cmd == 'q':
                    break
                continue

            print("\nВаш ход (w/a/s/d для движения, q - выход):")
            move = input("> ").lower()

            if move == 'q':
                break
            elif move in controls:
                self._game.change_direction(*controls[move])
                self._game.update()
            else:
                print("Неверная команда! Используйте W/A/S/D")
                time.sleep(1)


def run_game(width=cfg.DEFAULT_WIDTH, height=cfg.DEFAULT_HEIGHT):
    width = max(cfg.MIN_WIDTH, min(cfg.MAX_WIDTH, width))
    height = max(cfg.MIN_HEIGHT, min(cfg.MAX_HEIGHT, height))

    game = GameEngine(width, height)
    renderer = GameRenderer(game)
    renderer.run()