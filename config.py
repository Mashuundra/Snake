# config.py
"""
config.py
Конфигурационные параметры игры "Змейка"
"""

# РАЗМЕРЫ ИГРОВОГО ПОЛЯ (в клетках)
DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 20
MIN_WIDTH = 10
MAX_WIDTH = 40
MIN_HEIGHT = 10
MAX_HEIGHT = 40

# ВИЗУАЛЬНЫЕ ПАРАМЕТРЫ
DEFAULT_CELL_SIZE = 30
MIN_CELL_SIZE = 20
MAX_CELL_SIZE = 50

# СКОРОСТЬ ИГРЫ
# Значения от 1 до 10, где:
# 1 - очень медленно, 10 - очень быстро
DEFAULT_SPEED_LEVEL = 5  # средняя скорость по умолчанию

# Минимальный и максимальный уровень скорости
MIN_SPEED_LEVEL = 1
MAX_SPEED_LEVEL = 10


# Соответствие уровня скорости задержке в мс
# Чем выше уровень, тем меньше задержка (быстрее игра)
def speed_level_to_delay(level: int) -> int:
    """Преобразует уровень скорости (1-10) в задержку в миллисекундах"""
    # Уровень 1: 500 мс (очень медленно)
    # Уровень 5: 300 мс (средне)
    # Уровень 10: 50 мс (очень быстро)

    # Ограничиваем уровень
    level = max(MIN_SPEED_LEVEL, min(MAX_SPEED_LEVEL, level))

    # Расчёт задержки: от 500 до 50 мс
    # При level=1 -> 500, при level=10 -> 50
    delay = 500 - (level - 1) * 50
    return delay


# Для обратной совместимости со старым кодом
DEFAULT_SPEED = speed_level_to_delay(DEFAULT_SPEED_LEVEL)
MIN_SPEED = speed_level_to_delay(MIN_SPEED_LEVEL)
MAX_SPEED = speed_level_to_delay(MAX_SPEED_LEVEL)

# ЦВЕТА (RGB формата)
COLOR_BACKGROUND = (30, 30, 35)
COLOR_SNAKE_HEAD = (0, 200, 0)
COLOR_SNAKE_BODY = (0, 150, 0)
COLOR_FOOD = (255, 50, 50)
COLOR_OBSTACLE = (100, 100, 100)
COLOR_GRID = (50, 50, 55)
COLOR_TEXT = (255, 255, 255)

# НАСТРОЙКИ ОТРИСОВКИ
DRAW_GRID = True

# Типы карт
MAP_EMPTY = "empty"        # Сквозная карта (телепортация)
MAP_OBSTACLES = "obstacles" # Карта с препятствиями

# Начальное направление (вправо)
INITIAL_DIRECTION = (1, 0)