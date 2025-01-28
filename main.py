import sys
import os
from colorama import init
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir

from gui import HarmonyGeneratorGUI

init() 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    translations_dir = QDir.currentPath() + "/i18n"
    if not QDir(translations_dir).exists():
        os.makedirs("i18n", exist_ok=True)

    gui = HarmonyGeneratorGUI()
    gui.show()

    sys.exit(app.exec())