# Parking System Application

## Overview
This project is a PyQt5-based desktop application for managing a parking system. It provides user authentication (login, registration, password reset) via Firebase and allows users to enter vehicle and driver information, as well as book parking slots.

## Features
- **User Authentication**: Register, login, and reset password functionality using Firebase Authentication.
- **Vehicle and Driver Information**: Form for entering vehicle details and selecting date and time for parking.
- **Slot Booking**: Book available parking slots based on the entered details.

## Installation
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/parking-system.git
    cd parking-system
    ```

2. **Install Dependencies**:
    ```sh
    pip install pyqt5 pyrebase4
    ```

3. **Firebase Configuration**:
    Ensure your Firebase project is set up and replace the Firebase configuration in the code with your own Firebase project's credentials.

## Usage
1. **Run the Application**:
    ```sh
    python main.py
    ```
    This will open the login window of the application.

2. **Login/Register**:
    - Enter your email and password to login.
    - If you do not have an account, use the register button to create one.

3. **Forgot Password**:
    - Enter your email and click "Forgot Password?" to receive a password reset email.

4. **Enter Vehicle and Driver Information**:
    - After logging in, enter your vehicle number, model, select batch, date, and time, and then submit.

5. **Book Parking Slot**:
    - After submitting the vehicle information, proceed to the slot booking window to select and book a parking slot.

## Code Structure
- **main.py**: Contains the main application code with PyQt5 window classes and Firebase interaction.

## Firebase Configuration
Replace the `config` dictionary in the code with your Firebase project's configuration details:
```python
config = {
    "apiKey": "your_api_key",
    "authDomain": "your_project_id.firebaseapp.com",
    "databaseURL": "https://your_project_id.firebaseio.com",
    "projectId": "your_project_id",
    "storageBucket": "your_project_id.appspot.com",
    "messagingSenderId": "your_messaging_sender_id",
    "appId": "your_app_id",
    "measurementId": "your_measurement_id"
}
```
## Dependencies

- `PyQt5`
- `pyrebase4`

## Contributing

Contributions are welcome! Please create a pull request or submit an issue to discuss your ideas or report bugs.

## License

This project is licensed under the MIT License.
