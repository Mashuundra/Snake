"""
main.py
Точка входа в игру "Змейка" (текстовая версия)
"""

import sys
import argparse

import config as cfg


def parse_arguments():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(description='Змейка - классическая игра в терминале')
    parser.add_argument(
        '--width', '-w',
        type=int,
        default=cfg.DEFAULT_WIDTH,
        help=f'Ширина поля в клетках (от {cfg.MIN_WIDTH} до {cfg.MAX_WIDTH})'
    )
    parser.add_argument(
        '--height', '-H',  # Изменено с -h на -H (заглавная H)
        type=int,
        default=cfg.DEFAULT_HEIGHT,
        help=f'Высота поля в клетках (от {cfg.MIN_HEIGHT} до {cfg.MAX_HEIGHT})'
    )
    parser.add_argument(
        '--speed', '-s',
        type=int,
        default=cfg.DEFAULT_SPEED,
        help=f'Скорость игры (от {cfg.MIN_SPEED} до {cfg.MAX_SPEED})'
    )
    return parser.parse_args()


def validate_and_apply_args(args):
    """Валидирует аргументы и обновляет конфиг"""
    if not (cfg.MIN_WIDTH <= args.width <= cfg.MAX_WIDTH):
        print(f"Ошибка: ширина должна быть от {cfg.MIN_WIDTH} до {cfg.MAX_WIDTH}. "
              f"Использую значение по умолчанию ({cfg.DEFAULT_WIDTH})")
        args.width = cfg.DEFAULT_WIDTH

    if not (cfg.MIN_HEIGHT <= args.height <= cfg.MAX_HEIGHT):
        print(f"Ошибка: высота должна быть от {cfg.MIN_HEIGHT} до {cfg.MAX_HEIGHT}. "
              f"Использую значение по умолчанию ({cfg.DEFAULT_HEIGHT})")
        args.height = cfg.DEFAULT_HEIGHT

    if not (cfg.MIN_SPEED <= args.speed <= cfg.MAX_SPEED):
        print(f"Ошибка: скорость должна быть от {cfg.MIN_SPEED} до {cfg.MAX_SPEED}. "
              f"Использую значение по умолчанию ({cfg.DEFAULT_SPEED})")
        args.speed = cfg.DEFAULT_SPEED

    cfg.DEFAULT_WIDTH = args.width
    cfg.DEFAULT_HEIGHT = args.height
    cfg.DEFAULT_SPEED = args.speed


def main():
    """Главная функция"""
    print(" Добро пожаловать в игру «Змейка»! ")
    print()
    print("Управление:")
    print("  • W/A/S/D - движение змейки")
    print("  • R - начать заново")
    print("  • Q - выход из игры")
    print()
    print("Цель: съесть как можно больше еды, не врезавшись в стены или себя")
    print()
    print("Игра запускается через 2 секунды...")
    print("(Убедитесь, что окно терминала достаточно большое)")

    import time
    time.sleep(2)

    args = parse_arguments()
    validate_and_apply_args(args)

    print(f"\nЗапуск игры с параметрами:")
    print(f"  • Размер поля: {args.width} x {args.height}")
    print(f"  • Скорость: {args.speed}")
    print()

    from ui.renderer import run_game
    run_game(args.width, args.height)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Игра прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n Произошла ошибка: {e}")
        sys.exit(1)