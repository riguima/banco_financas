from PySide6 import QtWidgets
import sys

from login import Login


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = Login()
    widget.show()
    sys.exit(app.exec())
