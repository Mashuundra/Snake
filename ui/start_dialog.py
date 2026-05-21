"""
Диалог запуска игры - ввод имени, выбор карты и скорости
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QGroupBox,
    QRadioButton, QSlider, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import config as cfg


class StartDialog(QDialog):
    """Диалог запуска игры с выбором карты и вводом имени"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🐍 Змейка - Новая игра")
        self.setModal(True)
        self.setFixedSize(500, 700)

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """Настройка интерфейса диалога"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # Заголовок
        title_label = QLabel("🐍 ЗМЕЙКА 🐍")
        title_label.setFont(QFont("Arial", 26, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Разделитель
        line = QWidget()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #4CAF50;")
        layout.addWidget(line)

        # Поле ввода имени
        name_group = QGroupBox("Ваше имя")
        name_layout = QVBoxLayout(name_group)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваш никнейм")
        self.name_input.setMaxLength(20)
        self.name_input.setFont(QFont("Arial", 12))
        self.name_input.setText("Игрок")
        name_layout.addWidget(self.name_input)

        layout.addWidget(name_group)

        # Выбор карты
        map_group = QGroupBox("Выберите карту")
        map_layout = QVBoxLayout(map_group)
        map_layout.setSpacing(10)

        # Карта 1: Сквозная
        self.map_empty_radio = QRadioButton("Сквозная карта")
        self.map_empty_radio.setChecked(True)
        self.map_empty_radio.setToolTip("Змейка телепортируется через края поля")
        map_layout.addWidget(self.map_empty_radio)

        # Описание сквозной карты
        desc1 = QLabel(
            "   • Змейка проходит сквозь края и появляется с другой стороны\n   • Нет стен и препятствий")
        desc1.setWordWrap(True)
        desc1.setStyleSheet("color: #aaaaaa; font-size: 10px; margin-left: 20px;")
        map_layout.addWidget(desc1)

        # Разделитель
        spacer = QWidget()
        spacer.setFixedHeight(8)
        map_layout.addWidget(spacer)

        # Карта 2: С препятствиями
        self.map_obstacles_radio = QRadioButton("Карта с препятствиями")
        self.map_obstacles_radio.setToolTip("На поле есть препятствия, которые нужно объезжать")
        map_layout.addWidget(self.map_obstacles_radio)

        # Описание карты с препятствиями
        desc2 = QLabel(
            "   • На поле есть серые блоки-препятствия\n   • Нужно объезжать препятствия")
        desc2.setWordWrap(True)
        desc2.setStyleSheet("color: #aaaaaa; font-size: 10px; margin-left: 20px;")
        map_layout.addWidget(desc2)

        layout.addWidget(map_group)

        # Размер поля
        size_group = QGroupBox("Размер поля")
        size_layout = QHBoxLayout(size_group)

        size_layout.addWidget(QLabel("Ширина:"))
        self.width_combo = QComboBox()
        for w in [15, 20, 25, 30, 35]:
            self.width_combo.addItem(str(w))
        self.width_combo.setCurrentText(str(cfg.DEFAULT_WIDTH))
        self.width_combo.setFixedWidth(60)
        size_layout.addWidget(self.width_combo)

        size_layout.addSpacing(20)

        size_layout.addWidget(QLabel("Высота:"))
        self.height_combo = QComboBox()
        for h in [15, 20, 25, 30, 35]:
            self.height_combo.addItem(str(h))
        self.height_combo.setCurrentText(str(cfg.DEFAULT_HEIGHT))
        self.height_combo.setFixedWidth(60)
        size_layout.addWidget(self.height_combo)

        size_layout.addStretch()

        layout.addWidget(size_group)

        # Настройки скорости
        speed_group = QGroupBox("Скорость игры")
        speed_layout = QVBoxLayout(speed_group)

        # Ползунок скорости
        speed_slider_layout = QHBoxLayout()
        speed_slider_layout.addWidget(QLabel("Медленно"))

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)  # Средняя скорость
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setFixedWidth(250)

        speed_slider_layout.addWidget(self.speed_slider)
        speed_slider_layout.addWidget(QLabel("Быстро"))

        speed_layout.addLayout(speed_slider_layout)

        # Отображение текущей скорости
        self.speed_value_label = QLabel("Скорость: 5/10 (средняя)")
        self.speed_value_label.setAlignment(Qt.AlignCenter)
        self.speed_value_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 12px;")
        speed_layout.addWidget(self.speed_value_label)

        # Информация о задержке
        self.speed_info_label = QLabel("Задержка: 300 мс между ходами")
        self.speed_info_label.setAlignment(Qt.AlignCenter)
        self.speed_info_label.setStyleSheet("color: #888888; font-size: 10px;")
        speed_layout.addWidget(self.speed_info_label)

        # Подключаем сигнал изменения скорости
        self.speed_slider.valueChanged.connect(self.update_speed_label)

        layout.addWidget(speed_group)

        layout.addStretch()

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.play_btn = QPushButton("НАЧАТЬ ИГРУ")
        self.play_btn.setFixedSize(200, 50)
        self.play_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.play_btn.clicked.connect(self.accept)

        btn_layout.addWidget(self.play_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # Инициализация отображения скорости
        self.update_speed_label(5)

    def update_speed_label(self, value):
        """Обновляет отображение скорости"""
        # Рассчитываем задержку
        delay = cfg.speed_level_to_delay(value)

        if value == 1:
            text = f"Скорость: {value}/10 (очень медленно)"
            info = f"⏱️ Задержка: {delay} мс (очень спокойная игра)"
        elif value == 2:
            text = f"Скорость: {value}/10 (медленно)"
            info = f"⏱️ Задержка: {delay} мс"
        elif value <= 4:
            text = f"Скорость: {value}/10 (ниже среднего)"
            info = f"⏱️ Задержка: {delay} мс"
        elif value == 5:
            text = f"Скорость: {value}/10 (⭐ средняя ⭐)"
            info = f"⏱️ Задержка: {delay} мс (рекомендуется для новичков)"
        elif value <= 7:
            text = f"Скорость: {value}/10 (выше среднего)"
            info = f"⏱️ Задержка: {delay} мс"
        elif value <= 9:
            text = f"Скорость: {value}/10 (быстро)"
            info = f"⏱️ Задержка: {delay} мс"
        else:
            text = f"Скорость: {value}/10 (очень быстро!)"
            info = f"⏱️ Задержка: {delay} мс (для опытных игроков)"

        self.speed_value_label.setText(text)
        self.speed_info_label.setText(info)

    def apply_styles(self):
        """Применяет стили"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                color: #ffffff;
                background-color: #252525;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #4CAF50;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #3a3a3a;
                border-radius: 6px;
                background-color: #2d2d2d;
                color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QRadioButton {
                color: #ffffff;
                spacing: 10px;
                font-size: 12px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #666;
                border-radius: 9px;
                background-color: #3a3a3a;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #4CAF50;
                border-radius: 9px;
                background-color: #4CAF50;
            }
            QComboBox {
                padding: 6px;
                border: 2px solid #3a3a3a;
                border-radius: 6px;
                background-color: #2d2d2d;
                color: white;
                font-size: 12px;
            }
            QComboBox:hover {
                border: 2px solid #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #4CAF50;
            }
            QSlider::groove:horizontal {
                border: 1px solid #3a3a3a;
                height: 6px;
                background: #3a3a3a;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                border: 1px solid #4CAF50;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #66bb6a;
            }
            QSlider::sub-page:horizontal {
                background: #4CAF50;
                border-radius: 3px;
            }
            QLabel {
                color: #cccccc;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

    def get_settings(self):
        """Возвращает настройки из диалога"""
        # Получаем имя
        nickname = self.name_input.text().strip()
        if not nickname:
            nickname = "Игрок"

        # Получаем тип карты
        if self.map_empty_radio.isChecked():
            map_type = cfg.MAP_EMPTY
        else:
            map_type = cfg.MAP_OBSTACLES

        # Получаем размеры
        width = int(self.width_combo.currentText())
        height = int(self.height_combo.currentText())

        # Получаем уровень скорости
        speed_level = self.speed_slider.value()

        return {
            'nickname': nickname[:20],
            'map_type': map_type,
            'width': width,
            'height': height,
            'speed_level': speed_level
        }