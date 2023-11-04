from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QSize

class MainButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QtCore.QVariantAnimation(
            startValue=QtGui.QColor("#1F8EFA"),
            endValue=QtGui.QColor("#333A51"),
            valueChanged=self._on_value_changed,
            duration=200,
        )
        self._update_stylesheet(QtGui.QColor("#333A51"))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def _on_value_changed(self, color):
        self._update_stylesheet(color)

    def _update_stylesheet(self, background):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            color: white;
            border-radius: 30px;
            padding: 16px 32px;
            text-align: center;
            text-decoration: none;
            font-size: 20px;
            margin: 4px 2px;
            border: 2px solid #1F8EFA;
            font-weight: bold;
        }
        """
            % (background.name())
        )

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)

class MainButton1(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QtCore.QVariantAnimation(
            startValue=QtGui.QColor("#1F8EFA"),
            endValue=QtGui.QColor("#333A51"),
            valueChanged=self._on_value_changed,
            duration=200,
        )
        self._update_stylesheet(QtGui.QColor("#333A51"))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def _on_value_changed(self, color):
        self._update_stylesheet(color)

    def _update_stylesheet(self, background):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            color: white;
            border-radius: 20px;
            padding: 5px 20px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
            border: 2px solid #1F8EFA;
        }
        """
            % (background.name())
        )

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)

class SquareButton(QtWidgets.QPushButton):
    def __init__(self, parent, path=None, path_hover=None):
        super().__init__(parent)
        if path:
            self.path = path
            self.path_hover = path_hover
            self.icon = QtGui.QIcon(path)
            self.setIcon(self.icon)
            self.setIconSize(QSize(25, 25))
        self._animation = QtCore.QVariantAnimation(
            startValue=QtGui.QColor("#364059"),
            endValue=QtGui.QColor("#2C3751"),
            valueChanged=self._on_value_changed,
            duration=200,
        )
        self._update_stylesheet(QtGui.QColor("#2C3751"))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def _on_value_changed(self, color):
        self._update_stylesheet(color)

    def _update_stylesheet(self, background):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            color: white;
            text-align: left;
            text-decoration: none;
            font-size: 16px;
            padding: 0px 15px;
            border: none;
            letter-spacing: .05em;
        }
        """
            % (background.name())
        )

    def enterEvent(self, event):
        self.icon = QtGui.QIcon(self.path_hover)
        self.setIcon(self.icon)
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.icon = QtGui.QIcon(self.path)
        self.setIcon(self.icon)
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)


class ImageButton(QtWidgets.QPushButton):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.icon = QtGui.QIcon(path)
        self.setIcon(self.icon)
        self.setIconSize(QSize(150, 130))

        self.setStyleSheet(
            """
        QPushButton{
            background-color: #2C3751;
            text-align: center;
            text-decoration: none;
            font-size: 20px;
            margin: 4px 2px;
            border: none;
        }
        """
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.animation = QtCore.QPropertyAnimation(self, b"iconSize")
        self.animation.setDuration(300)  # Animation duration in milliseconds
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)

    def enterEvent(self, event):
        self.animation.setEndValue(QtCore.QSize(165, 140))
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setEndValue(QtCore.QSize(150, 130))
        self.animation.start()

class ImageButton1(QtWidgets.QPushButton):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.icon = QtGui.QIcon(path)
        self.setIcon(self.icon)
        self.setIconSize(QSize(30, 30))

        self.setStyleSheet(
            """
        QPushButton{
            font-size: 20px;
            margin: 4px 2px;
            border: none;
        }
        """
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def enterEvent(self, event):
        self.setIconSize(QSize(35, 35))

    def leaveEvent(self, event):
        self.setIconSize(QSize(30, 30))

class ImageButton2(QtWidgets.QPushButton):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.icon = QtGui.QIcon(path)
        self.setIcon(self.icon)
        self.setIconSize(QSize(137, 210))

        self.setStyleSheet(
            """
        QPushButton{
            background-color: rgba(0,0,0,0);
            text-align: center;
            text-decoration: none;
            font-size: 20px;
            margin: 4px 2px;
            border: none;
        }
        """
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.animation = QtCore.QPropertyAnimation(self, b"iconSize")
        self.animation.setDuration(300)  # Animation duration in milliseconds
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)

    def enterEvent(self, event):
        self.animation.setEndValue(QtCore.QSize(150, 230))
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setEndValue(QtCore.QSize(137, 210))
        self.animation.start()

class ExtraButton(QtWidgets.QPushButton):
    def __init__(self, parent, path, path_hover):
        super().__init__(parent)
        self.path = path
        self.path_hover = path_hover
        self.icon = QtGui.QIcon(path)
        self.setIcon(self.icon)
        self.setIconSize(QSize(30, 30))

        self.setStyleSheet(
        """
            QPushButton{
                background-color: #2C3751;
                text-align: center;
                text-decoration: none;
                font-size: 20px;
                margin: 4px 2px;
                border: none;
                font-weight: bold;
                color: #ACACBF;
            }
            QPushButton:hover {
                color: #FFFFFF;
            }
        """
        )

        self.setCursor(Qt.PointingHandCursor);

    def enterEvent(self, event):
        self.icon = QtGui.QIcon(self.path_hover)
        self.setIcon(self.icon)
    
    def leaveEvent(self, event):
        self.icon = QtGui.QIcon(self.path)
        self.setIcon(self.icon)

class TextButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QPushButton{
                background-color: #2C3751;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                border: none;
                font-weight: bold;
                color: #ACACBF;
            }
            
            QPushButton:hover{
                text-decoration: underline;
            }
            """
        )
        
        self.setCursor(Qt.DragLinkCursor);

class ExitButton(QtWidgets.QPushButton):
    def __init__(self, parent, path=None, path_hover=None):
        super().__init__(parent)
        self.path = path
        self.path_hover = path_hover
        self.icon = QtGui.QIcon(path)
        self.setIcon(self.icon)
        self.setIconSize(QSize(30, 30))

        self.setStyleSheet(
            """
            QPushButton{
                background-color: #2C3751;
                text-align: center;
                text-decoration: none;
                font-size: 20px;
                margin: 4px 2px;
                border: none;
                font-weight: bold;
                color: #ACACBF;
            }

            QPushButton:hover {
                color: #FF0000;
            }
        """
        )
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def enterEvent(self, event):
        self.icon = QtGui.QIcon(self.path_hover)
        self.setIcon(self.icon)

    def leaveEvent(self, event):
        self.icon = QtGui.QIcon(self.path)
        self.setIcon(self.icon)

class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Dialog"))

        # self.pushButton = SquareButton()
        self.pushButton = ImageButton(self, "./Images/logo03.png")
        # self.pushButton.setText(self.tr("Click Here"))
        self.pushButton.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.pushButton)

        self.resize(400, 300)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())