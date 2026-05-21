# core/__init__.py (обновлённый)
"""
core package - игровая логика змейки
"""

from core.snake import Snake
from core.game import GameEngine, GameStatus
from core.leaderboard import Leaderboard

__all__ = ['Snake', 'GameEngine', 'GameStatus', 'Leaderboard']