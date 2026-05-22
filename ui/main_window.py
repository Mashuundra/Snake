"""
Главное окно приложения
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QGroupBox,
    QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import config as cfg
from ui.game_widget import GameWidget
from ui.start_dialog import StartDialog
from core.leaderboard import Leaderboard


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Змейка")
        self.setFixedSize(900, 700)

        self.leaderboard = Leaderboard()
        self.current_nickname = None
        self.current_map_type = cfg.MAP_EMPTY
        self.game_widget = None

        self.setup_ui()
        self.apply_styles()

        # Показываем диалог запуска при старте
        self.show_start_dialog()

    def setup_ui(self):
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Левая панель (игровое поле)
        self.game_container = QWidget()
        game_layout = QVBoxLayout(self.game_container)

        # Информационная панель
        info_panel = QWidget()
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(0, 0, 0, 10)

        self.nickname_label = QLabel("Игрок: ")
        self.nickname_label.setFont(QFont("Arial", 12))

        self.score_label = QLabel("Счёт: 0")
        self.score_label.setFont(QFont("Arial", 14, QFont.Bold))

        self.map_label = QLabel("Карта: Сквозная")
        self.map_label.setFont(QFont("Arial", 10))
        self.map_label.setStyleSheet("color: #aaa;")

        info_layout.addWidget(self.nickname_label)
        info_layout.addStretch()
        info_layout.addWidget(self.score_label)
        info_layout.addStretch()
        info_layout.addWidget(self.map_label)

        game_layout.addWidget(info_panel)

        # Создаём game_area с layout
        self.game_area = QWidget()
        game_area_layout = QVBoxLayout(self.game_area)
        game_area_layout.setContentsMargins(0, 0, 0, 0)
        game_layout.addWidget(self.game_area)

        main_layout.addWidget(self.game_container, stretch=2)

        # Правая панель (управление и рекорды)
        right_panel = QWidget()
        right_panel.setFixedWidth(250)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(15)

        # Блок управления
        control_group = QGroupBox("Управление")
        control_layout = QVBoxLayout(control_group)

        control_text = QLabel(
            "W / ↑ - вверх\n"
            "S / ↓ - вниз\n"
            "A / ← - влево\n"
            "D / → - вправо\n"
            "Пробел - пауза\n"
            "R - рестарт"
        )
        control_text.setWordWrap(True)
        control_layout.addWidget(control_text)

        right_layout.addWidget(control_group)

        # Кнопки управления
        self.new_game_btn = QPushButton("Новая игра")
        self.new_game_btn.clicked.connect(self.show_start_dialog)
        right_layout.addWidget(self.new_game_btn)

        # Таблица рекордов
        leaderboard_group = QGroupBox("🏆 Таблица рекордов")
        leaderboard_layout = QVBoxLayout(leaderboard_group)

        self.leaderboard_list = QLabel()
        self.leaderboard_list.setWordWrap(True)
        self.leaderboard_list.setFont(QFont("Courier", 10))
        self.leaderboard_list.setAlignment(Qt.AlignTop)
        leaderboard_layout.addWidget(self.leaderboard_list)

        right_layout.addWidget(leaderboard_group)
        right_layout.addStretch()

        main_layout.addWidget(right_panel)

    def apply_styles(self):
        """Применяет стили к виджетам"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ddd;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
            QLabel {
                color: #ddd;
            }
        """)

    def show_start_dialog(self):
        """Показывает диалог запуска новой игры"""
        dialog = StartDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            settings = dialog.get_settings()

            # Сохраняем настройки
            self.current_nickname = settings['nickname']
            self.current_map_type = settings['map_type']
            self.current_speed_level = settings['speed_level']  # Сохраняем скорость

            # Обновляем глобальные настройки
            cfg.DEFAULT_WIDTH = settings['width']
            cfg.DEFAULT_HEIGHT = settings['height']
            cfg.DEFAULT_SPEED_LEVEL = settings['speed_level']
            cfg.DEFAULT_SPEED = cfg.speed_level_to_delay(settings['speed_level'])

            # Обновляем отображение
            self.nickname_label.setText(f"Игрок: {self.current_nickname}")

            map_text = "Карта: С препятствиями" if self.current_map_type == cfg.MAP_OBSTACLES else "Карта: Сквозная"
            self.map_label.setText(map_text)

            # Создаём игру
            self.create_game_widget()

    def create_game_widget(self):
        """Создаёт виджет игры с текущими настройками"""
        # Очищаем старый виджет
        if self.game_area.layout():
            if self.game_widget:
                self.game_widget.stop_timer()

            while self.game_area.layout().count():
                widget = self.game_area.layout().takeAt(0).widget()
                if widget:
                    widget.deleteLater()

        # Создаём новый виджет
        self.game_widget = GameWidget(self)
        self.game_widget.set_game_settings(
            width=cfg.DEFAULT_WIDTH,
            height=cfg.DEFAULT_HEIGHT,
            map_type=self.current_map_type
        )

        self.game_widget.game_updated.connect(self.update_info_display)
        self.game_widget.game_ended.connect(self.on_game_ended)

        # Добавляем в game_area
        self.game_area.layout().addWidget(self.game_widget)

        self.game_widget.setFocus()
        self.update_info_display()
        self.update_leaderboard_display()

    def update_leaderboard_display(self):
        """Обновляет отображение таблицы рекордов"""
        records = self.leaderboard.get_top_scores(10)

        if not records:
            text = "   Пока нет рекордов\n   Сыграйте первую игру!"
        else:
            lines = []
            for i, record in enumerate(records, 1):
                nickname = record['nickname'][:12]
                score = record['score']
                map_type = "🔮" if record['map_type'] == cfg.MAP_EMPTY else "🧱"
                lines.append(f"{i:2}. {nickname:<12} {score:>4}  {map_type}")
            text = "\n".join(lines)

        self.leaderboard_list.setText(text)

    def update_info_display(self):
        """Обновляет отображение счёта"""
        if self.game_widget and self.game_widget.game:
            self.score_label.setText(f"Счёт: {self.game_widget.game.score}")

    def on_game_ended(self, score: int, map_type: str):
        """Обработка окончания игры"""
        if self.leaderboard.is_new_record(score):
            self.leaderboard.add_record(self.current_nickname, score, map_type)
            self.update_leaderboard_display()

    def keyPressEvent(self, event):
        """Передаём все нажатия клавиш игровому виджету"""
    # Сначала передаём игровому виджету
        if self.game_widget:
            self.game_widget.keyPressEvent(event)

        # Обрабатываем глобальную клавишу N (новая игра)
        if event.key() == Qt.Key_N:
            self.show_start_dialog()

        # Вызываем родительский метод
        super().keyPressEvent(event)
