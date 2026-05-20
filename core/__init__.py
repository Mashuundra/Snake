"""
core package - игровая логика змейки

Содержит:
- Snake: класс змейки
- GameEngine: основной игровой движок
- GameStatus: состояния игры
"""

from core.snake import Snake
from core.game import GameEngine, GameStatus

__all__ = ['Snake', 'GameEngine', 'GameStatus']
