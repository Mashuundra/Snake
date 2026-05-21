# main.py
import os
import sys

# путь к плагинам PyQt5
try:
    import PyQt5

    pyqt_path = os.path.dirname(PyQt5.__file__)

    possible_plugins = [
        os.path.join(pyqt_path, 'Qt5', 'plugins'),
        os.path.join(pyqt_path, 'plugins'),
        os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
    ]

    for plugins_path in possible_plugins:
        if os.path.exists(plugins_path):
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugins_path
            print(f"Найдены плагины: {plugins_path}")
            break
except:
    pass

os.environ['QT_QPA_PLATFORM'] = 'windows'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt

        app = QApplication(sys.argv)

        app.setStyle('Fusion')

        from ui.main_window import MainWindow
        window = MainWindow()
        window.show()

        print("Игра запущена")
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main()