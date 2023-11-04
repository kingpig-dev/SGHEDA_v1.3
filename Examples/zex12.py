from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

if __name__ == "__main__":
    app = QApplication([])

    # Create a main window
    window = QMainWindow()
    window.resize(800, 600)

    # Create a web view widget
    web_view = QWebEngineView(window)
    window.setCentralWidget(web_view)

    # Load and display the HTML table
    html_content = """
    <html>
    <body>
    <table border="1">
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
            <th>Column 3</th>
        </tr>
        <tr>
            <td>Value 1</td>
            <td>Value 2</td>
            <td>Value 3</td>
        </tr>
        <tr>
            <td>Value 4</td>
            <td>Value 5</td>
            <td>Value 6</td>
        </tr>
    </table>
    </body>
    </html>
    """

    web_view.setHtml(html_content, QUrl("http://localhost"))

    # Show the window
    window.show()

    # Start the application event loop
    app.exec_()