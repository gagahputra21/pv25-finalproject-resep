import sys
from PyQt5.QtWidgets import QApplication

from gui import ResepApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ResepApp()
    ex.show()
    sys.exit(app.exec_())