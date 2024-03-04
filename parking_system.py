import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit, QTimeEdit, QHBoxLayout, QFrame, QGridLayout, QDialog, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QFont
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize

import datetime
import pyrebase

# Firebase configuration
config = {
    "apiKey": " AIzaSyAOs9HR3UY9GcECAXwNubcH0DFDRkUq1L8 ",
    "authDomain": "parking-system-a1329.firebaseapp.com",
    "databaseURL": "https://parking-system-a1329-default-rtdb.firebaseio.com/",
    "projectId": "parking-system-a1329",
    "storageBucket": "parking-system-a1329.appspot.com",
    "messagingSenderId": "602309979248",
    "appId": "1:602309979248:web:4197f619b7a6c665e158b5",
    "measurementId": "G-74CK80T7RM"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def encode_email(email):
    return email.replace('.', ',')

def decode_email(encoded_email):
    return encoded_email.replace(',', '.')

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login to the Parking System")
        self.setGeometry(100, 100, 960, 540)  # Use a fixed size for demo purposes

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                font-size: 20px;
                color: white;
            }
            QLineEdit {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QPushButton {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """)

        self.overlayImage = QLabel(self)
        pixmapOverlay = QPixmap('images/background.png').scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Resize image to 400x300, maintaining aspect ratio
        self.overlayImage.setPixmap(pixmapOverlay)
        self.overlayImage.resize(pixmapOverlay.size())  # Resize QLabel to fit the scaled pixmap

        # Position the overlay image
        # Example: Center the image in the window
        self.overlayImage.move(80,150)

        # Main layout is horizontal: image | login form
        mainLayout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        # Adjust the layout with a spacer on the left (if necessary)
        leftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        mainLayout.addItem(leftSpacer)

        # Right side - Login form in a QVBoxLayout
        formLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)

        # Logo at the top
        logo = QLabel(self)
        pixmap = QPixmap('images/logo.png').scaled(150, 150, Qt.KeepAspectRatio)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(logo)

        # Adjust spacing and alignment
        formLayout.setAlignment(Qt.AlignCenter)
        formLayout.setSpacing(10)

        # Widgets
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("Login")
        self.registerButton = QPushButton("Register")
        self.forgotPasswordButton = QPushButton("Forgot Password?")

        # Styling Widgets
        self.loginButton.setStyleSheet("QPushButton { margin: 5px; padding: 10px; font-size: 16px; }")
        self.registerButton.setStyleSheet("QPushButton { margin: 5px; padding: 10px; font-size: 16px; }")
        self.forgotPasswordButton.setStyleSheet("QPushButton { margin: 5px; padding: 10px; font-size: 16px; }")
        self.email.setFont(QFont("Arial", 10))
        self.password.setFont(QFont("Arial", 10))

        # Add widgets to the form layout
        formLayout.addWidget(self.email)
        formLayout.addWidget(self.password)
        formLayout.addWidget(self.loginButton)
        formLayout.addWidget(self.registerButton)
        formLayout.addWidget(self.forgotPasswordButton)

        # Connect buttons
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)
        self.forgotPasswordButton.clicked.connect(self.forgotPassword)

    def login(self):
        email = self.email.text()
        password = self.password.text()
        try:
            auth.sign_in_with_email_and_password(email, password)
            self.main = MainWindow()
            self.main.show()
            self.close()
        except Exception as e:
            error_message = str(e)
            QMessageBox.warning(self, "Login failed", "Failed to login: " + error_message)

    def register(self):
        email = self.email.text()
        password = self.password.text()
        try:
            auth.create_user_with_email_and_password(email, password)
            QMessageBox.information(self, "Registration successful", "You can now login with your credentials")
        except Exception as e:
            error_message = e.args[1]  # Get detailed error message
            QMessageBox.warning(self, "Registration failed", error_message)

    def forgotPassword(self):
        email = self.email.text()
        if email:
            try:
                auth.send_password_reset_email(email)
                QMessageBox.information(self, "Password Reset", "A password reset link has been sent to your email.")
            except Exception as e:
                QMessageBox.warning(self, "Reset Failed", "Failed to send password reset email.")
        else:
            QMessageBox.warning(self, "Input Required", "Please enter your email address.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Vehicle and Driver Information")
        self.setGeometry(100, 100, 960, 540)  # Use a fixed size for demo purposes

        # Apply stylesheet for consistent look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                font-size: 20px;
                color: white;
            }
            QLineEdit {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QPushButton {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
            QDateEdit, QTimeEdit, QComboBox {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout(centralWidget)
        centralWidget.setLayout(mainLayout)

        # Centering content within the layout
        mainLayout.setAlignment(Qt.AlignCenter)

        # Spacing between widgets
        mainLayout.setSpacing(10)

        # Add your widgets here
        self.infoLabel = QLabel("Enter Vehicle and Driver Information:")
        self.infoLabel.setAlignment(Qt.AlignCenter)

        self.vehicleNumber = QLineEdit()
        self.vehicleNumber.setPlaceholderText("Vehicle Number")

        self.vehicleModel = QLineEdit()
        self.vehicleModel.setPlaceholderText("Vehicle Model")

        self.batchSelect = QComboBox()
        self.batchSelect.addItems(["Morning", "Afternoon", "Evening"])

        self.dateSelect = QDateEdit()
        self.dateSelect.setCalendarPopup(True)
        self.dateSelect.setDate(QDate.currentDate())

        self.timeSelect = QTimeEdit()
        self.timeSelect.setTime(QTime.currentTime())

        self.submitButton = QPushButton("Submit")

        # Adding widgets to the main layout
        mainLayout.addWidget(self.infoLabel)
        mainLayout.addWidget(self.vehicleNumber)
        mainLayout.addWidget(self.vehicleModel)
        mainLayout.addWidget(self.batchSelect)
        mainLayout.addWidget(self.dateSelect)
        mainLayout.addWidget(self.timeSelect)
        mainLayout.addWidget(self.submitButton)

        # Connect the submit button to its function
        self.submitButton.clicked.connect(self.submitInformation)

    def submitInformation(self):
        vehicle_number = self.vehicleNumber.text()
        vehicle_model = self.vehicleModel.text()
        batch = self.batchSelect.currentText()
        date = self.dateSelect.date().toString("yyyy-MM-dd")
        time = self.timeSelect.time().toString()

        # Here you would add the logic to store the information in Firebase
        print(f"Vehicle Number: {vehicle_number}, Model: {vehicle_model}, Batch: {batch}, Date: {date}, Time: {time}")
        # Assuming you have a method to store this information in Firebase
        self.storeInformation(vehicle_number, vehicle_model, batch, date, time)
        self.openSlotBooking()

    def storeInformation(self, vehicle_number, vehicle_model, batch, date, time):
        user_id = auth.current_user['localId']
        new_entry = {
            "vehicle_number": vehicle_number,
            "vehicle_model": vehicle_model,
            "batch": batch,
            "date": date,
            "time": time
        }
        db.child("users").child(user_id).child("vehicle_info").push(new_entry)
        QMessageBox.information(self, "Success", "Information submitted successfully.")
        
    def openSlotBooking(self):
        self.slotBookingWindow = SlotBookingWindow(db)
        self.slotBookingWindow.show()
        
# Assuming db is your Pyrebase database instance from the main application
class SlotBookingWindow(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Book Parking Slot")
        self.setGeometry(100, 100, 960, 540)
        self.db=db
        self.initUI()
        
        self.setStyleSheet("""
            QDialog{
                background-color: #2c3e50;
            }
            QLabel {
                font-size: 20px;
                color: white;
            }
            QLineEdit {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QPushButton {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
            QDateEdit, QTimeEdit, QComboBox {
                font-size: 18px;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)

    def initUI(self):
        gridLayout = QGridLayout()

        self.dateSelect = QDateEdit()
        self.dateSelect.setCalendarPopup(True)
        self.dateSelect.setDate(QDate.currentDate())

        self.timeSelect = QTimeEdit()
        self.timeSelect.setTime(QTime.currentTime())

        self.slotSelect = QComboBox()
        # Assuming slots are predefined, populate this dynamically based on your Firestore data in a real app
        self.slotSelect.addItems(["Slot 1", "Slot 2", "Slot 3"])

        self.checkAvailabilityButton = QPushButton("Check Availability")
        self.checkAvailabilityButton.clicked.connect(self.checkAvailability)

        self.bookSlotButton = QPushButton("Book Slot")
        self.bookSlotButton.clicked.connect(self.bookSlot)

        gridLayout.addWidget(QLabel("Date:"), 0, 0)
        gridLayout.addWidget(self.dateSelect, 0, 1)
        gridLayout.addWidget(QLabel("Time:"), 1, 0)
        gridLayout.addWidget(self.timeSelect, 1, 1)
        gridLayout.addWidget(QLabel("Slot:"), 2, 0)
        gridLayout.addWidget(self.slotSelect, 2, 1)
        gridLayout.addWidget(self.checkAvailabilityButton, 3, 0)
        gridLayout.addWidget(self.bookSlotButton, 3, 1)

        self.setLayout(gridLayout)

    def checkAvailability(self):
        # Example: Check slot availability (this function should query Firestore to check for existing bookings)
        print("Checking slot availability...")

    def bookSlot(self):
        # Adjusted for Pyrebase
        date = self.dateSelect.date().toString("yyyy-MM-dd")
        time = self.timeSelect.time().toString("HH:mm")
        slot = self.slotSelect.currentText()
        booking = {"date": date, "time": time, "slot": slot}
        self.db.child('bookings').push(booking)
        QMessageBox.information(self, "Success", "Slot booked successfully.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
