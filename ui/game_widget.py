"""
Виджет для отрисовки игры на PyQt5
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont

import config as cfg
from core.game import GameEngine, GameStatus


class GameWidget(QWidget):
    """Виджет для отображения и управления игрой"""

    game_updated = pyqtSignal()
    game_ended = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(400, 400)

        self.game = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_step)
        self.is_paused = False

    def set_game_settings(self, width, height, map_type):
        """Устанавливает настройки игры и перезапускает её"""
        print(f"Создание игры: {width}x{height}, карта: {map_type}")

        # Останавливаем таймер
        self.timer.stop()

        # Создаём новый игровой движок
        self.game = GameEngine(width, height, map_type)

        # Получаем задержку из уровня скорости
        speed_delay = cfg.speed_level_to_delay(cfg.DEFAULT_SPEED_LEVEL)
        self.timer.setInterval(speed_delay)

        # Сбрасываем флаги
        self.is_paused = False

        # Запускаем таймер
        self.timer.start()

        # Обновляем отображение
        self.update()
        self.game_updated.emit()

    def set_speed(self, speed_level):
        """Изменяет скорость игры во время игры"""
        speed_delay = cfg.speed_level_to_delay(speed_level)
        self.timer.setInterval(speed_delay)

    def start_timer(self):
        """Запускает таймер игры"""
        if not self.timer.isActive() and self.game:
            self.timer.start(cfg.DEFAULT_SPEED)
        self.is_paused = False

    def stop_timer(self):
        """Останавливает таймер"""
        self.timer.stop()

    def game_step(self):
        """Один шаг игры"""
        if self.is_paused or self.game is None:
            return

        if self.game.status == GameStatus.PLAYING:
            self.game.update()
            self.game_updated.emit()
            self.update()

            if self.game.status != GameStatus.PLAYING:
                self.stop_timer()
                self.game_ended.emit(self.game.score, self.game.map_type)

    def reset_game(self):
        """Сбрасывает игру с текущим типом карты"""
        if self.game is None:
            return

        current_map_type = self.game.map_type
        current_width = self.game.width
        current_height = self.game.height

        # Полностью пересоздаём игру
        self.game = GameEngine(current_width, current_height, current_map_type)
        self.is_paused = False

        # Обновляем скорость
        speed_delay = cfg.speed_level_to_delay(cfg.DEFAULT_SPEED_LEVEL)
        self.timer.setInterval(speed_delay)

        self.start_timer()
        self.update()
        self.game_updated.emit()

    def toggle_pause(self):
        """Пауза/продолжение"""
        if self.game and self.game.status == GameStatus.PLAYING:
            self.is_paused = not self.is_paused
            self.update()

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if self.game is None:
            return

        key = event.key()

        # Управление направлением (только если игра активна)
        if self.game.status == GameStatus.PLAYING and not self.is_paused:
            if key == Qt.Key_W or key == Qt.Key_Up:
                self.game.change_direction(0, -1)
            elif key == Qt.Key_S or key == Qt.Key_Down:
                self.game.change_direction(0, 1)
            elif key == Qt.Key_A or key == Qt.Key_Left:
                self.game.change_direction(-1, 0)
            elif key == Qt.Key_D or key == Qt.Key_Right:
                self.game.change_direction(1, 0)

        # Глобальные команды
        if key == Qt.Key_Space:
            self.toggle_pause()
        elif key == Qt.Key_R:
            self.reset_game()

        self.update()

    def paintEvent(self, event):
        """Отрисовка игры"""
        if not self.game:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)

        # Расчёт размера клетки
        cell_size = min(
            self.width() // self.game.width,
            self.height() // self.game.height
        )
        cell_size = max(15, cell_size)

        offset_x = (self.width() - cell_size * self.game.width) // 2
        offset_y = (self.height() - cell_size * self.game.height) // 2

        # Заливка фона
        painter.fillRect(0, 0, self.width(), self.height(), QColor(*cfg.COLOR_BACKGROUND))

        # Отрисовка сетки
        if cfg.DRAW_GRID:
            painter.setPen(QPen(QColor(*cfg.COLOR_GRID), 1))
            for x in range(self.game.width + 1):
                painter.drawLine(
                    offset_x + x * cell_size, offset_y,
                    offset_x + x * cell_size, offset_y + self.game.height * cell_size
                )
            for y in range(self.game.height + 1):
                painter.drawLine(
                    offset_x, offset_y + y * cell_size,
                              offset_x + self.game.width * cell_size, offset_y + y * cell_size
                )

        # Отрисовка препятствий
        for x, y in self.game.obstacles:
            rect = QRectF(
                offset_x + x * cell_size,
                offset_y + y * cell_size,
                cell_size - 1, cell_size - 1
            )
            painter.fillRect(rect, QColor(*cfg.COLOR_OBSTACLE))

        # Отрисовка еды
        if self.game.food_position:
            fx, fy = self.game.food_position
            rect = QRectF(
                offset_x + fx * cell_size,
                offset_y + fy * cell_size,
                cell_size - 1, cell_size - 1
            )
            painter.fillRect(rect, QColor(*cfg.COLOR_FOOD))

        # Отрисовка змейки
        for i, (x, y) in enumerate(self.game.snake_body):
            rect = QRectF(
                offset_x + x * cell_size,
                offset_y + y * cell_size,
                cell_size - 1, cell_size - 1
            )
            if i == 0:
                painter.fillRect(rect, QColor(*cfg.COLOR_SNAKE_HEAD))
            else:
                painter.fillRect(rect, QColor(*cfg.COLOR_SNAKE_BODY))

        # Отрисовка паузы
        if self.is_paused and self.game.status == GameStatus.PLAYING:
            painter.setPen(QPen(QColor(*cfg.COLOR_TEXT), 2))
            painter.setFont(QFont("Arial", 20, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "ПАУЗА")

        # Отрисовка сообщения о конце игры
        if self.game.status == GameStatus.GAME_OVER:
            painter.setPen(QPen(QColor(255, 100, 100), 2))
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(
                self.rect(), Qt.AlignCenter,
                f"GAME OVER\nСчёт: {self.game.score}\nНажмите R для новой игры"
            )
        elif self.game.status == GameStatus.WIN:
            painter.setPen(QPen(QColor(100, 255, 100), 2))
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(
                self.rect(), Qt.AlignCenter,
                f"ПОБЕДА!\nСчёт: {self.game.score}\nНажмите R для новой игры"
            )