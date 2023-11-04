import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTextEdit, QScrollArea


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tab Widget with Scrollbar")
        self.setGeometry(100, 100, 400, 300)

        # Create the QTabWidget
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # Create the first tab
        tab1 = QWidget()

        # Create the contents of the tab (a QTextEdit in this example)
        text_edit = QTextEdit()
        text_edit.setPlainText("This is a lot of content...\n" * 50)

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the widget to resize
        scroll_area.setWidget(text_edit)

        # # Create the layout for the tab
        # tab_layout = QVBoxLayout()
        # tab_layout.addWidget(scroll_area)

        # Set the layout for the tab
        # tab1.setLayout(tab_layout)

        # Add the tab to the tab widget
        tab_widget.addTab(scroll_area, "Tab 1")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())