import sys
import platform
import hashlib
import uuid
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox


class LicenseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("License Window")
        self.setGeometry(100, 100, 400, 200)

        # Create labels
        label_machine_number = QLabel("Machine Number:", self)
        label_machine_number.setGeometry(20, 20, 120, 20)

        # Create line edit for machine number
        self.line_machine_number = QLineEdit(self)
        self.line_machine_number.setGeometry(150, 20, 200, 20)
        self.line_machine_number.setReadOnly(True)

        # Create labels
        label_serial_number = QLabel("Serial Number:", self)
        label_serial_number.setGeometry(20, 60, 120, 20)

        # Create line edit for serial number
        self.line_serial_number = QLineEdit(self)
        self.line_serial_number.setGeometry(150, 60, 200, 20)

        # Create button for validating the serial number
        self.button_validate = QPushButton("Validate", self)
        self.button_validate.setGeometry(150, 100, 100, 30)
        self.button_validate.clicked.connect(self.validate_license)

        # Get machine number
        machine_number = self.get_machine_number()
        self.line_machine_number.setText(machine_number)

    def get_machine_number1(self):
        # Use the platform module to retrieve the machine number
        node = platform.node()
        machine_number = str(hash(node))  # Convert the machine number to a string
        return machine_number

    def get_machine_number(self):
        # Get operating system version
        mac_address = uuid.getnode()

        # Get program version
        program_version = "1.0"  # Replace with your actual program version

        # Combine OS version and program version
        combined_str = f"{mac_address}-{program_version}"

        # Generate a hash of the combined string
        hash_value = hashlib.md5(combined_str.encode()).hexdigest()
        machine_number = hash_value[:16]
        return machine_number

    def validate_license(self):
        # Get the entered serial number
        entered_serial_number = self.line_serial_number.text()

        # Implement your license validation logic here
        # You can compare the entered serial number with a valid serial number

        # For example, let's assume the valid serial number is "123456"
        valid_serial_number = "123456"

        if entered_serial_number == valid_serial_number:
            QMessageBox.information(self, "License Validation", "License is valid!")
        else:
            QMessageBox.warning(self, "License Validation", "Invalid license!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LicenseWindow()
    window.show()
    sys.exit(app.exec_())

#     self.is_dragging = False
    #     self.offset = QPoint()
    #
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.is_dragging = True
    #         self.offset = event.pos()
    #
    # def mouseMoveEvent(self, event):
    #     if self.is_dragging:
    #         self.move(event.globalPos() - self.offset)
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.is_dragging = False
    # -----------------
    # ticker button