from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton,
    QComboBox, QDateEdit, QTimeEdit, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QDate, QTime

from logic.geo_lookup import load_city_data
from logic.astroniharEng import get_astro_data  
from logic.panchangWrapper import prepare_panchang_payload

import json

class StartForm(QWidget):
    def __init__(self, update_callback=None):
        super().__init__()
        self.setWindowTitle("RogaHora - User Form")
        self.city_data = load_city_data()
        self.update_callback = update_callback

        layout = QVBoxLayout()

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()

        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate.currentDate())

        self.time = QTimeEdit()
        self.time.setTime(QTime.currentTime())

        self.ampm = QComboBox()
        self.ampm.addItems(["AM", "PM"])

        self.state_dropdown = QComboBox()
        self.state_dropdown.addItems(sorted(self.city_data.keys()))
        self.state_dropdown.currentTextChanged.connect(self.update_cities)

        self.city_dropdown = QComboBox()

        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.first_name)

        layout.addWidget(QLabel("Surname:"))
        layout.addWidget(self.last_name)

        layout.addWidget(QLabel("Date of Birth:"))
        layout.addWidget(self.dob)

        layout.addWidget(QLabel("Time:"))
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time)
        time_layout.addWidget(self.ampm)
        layout.addLayout(time_layout)

        layout.addWidget(QLabel("State:"))
        layout.addWidget(self.state_dropdown)

        layout.addWidget(QLabel("City:"))
        layout.addWidget(self.city_dropdown)

        # Button Row
        btn_layout = QHBoxLayout()

        self.btn_generate = QPushButton("Generate Chart")
        self.btn_generate.clicked.connect(self.handle_generate_chart)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save_user_data)

        btn_layout.addWidget(self.btn_generate)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.update_cities(self.state_dropdown.currentText())

    def update_cities(self, state):
        self.city_dropdown.clear()
        self.city_dropdown.addItems(sorted(self.city_data[state].keys()))

    def handle_generate_chart(self):
        name = self.first_name.text()
        surname = self.last_name.text()
        date = self.dob.date().toString("dd-MM-yyyy")
        time = self.time.time().toString("hh:mm")
        ampm = self.ampm.currentText()
        state = self.state_dropdown.currentText()
        city = self.city_dropdown.currentText()
        lat, lon = self.city_data[state][city]
        full_time = f"{time} {ampm}"

        # Calculate data
        astro_data = get_astro_data(date, full_time, lat, lon)
        panchang_data = prepare_panchang_payload(date, time, ampm, lat, lon)

        if self.update_callback:
            # Called from inside main window (edit -> birthdata)
            self.update_callback(name, surname, date, full_time, lat, lon, astro_data, panchang_data)
            self.close()
        else:
            # Called from main.py, start main window
            from gui.main_window import MainWindow
            self.main_win = MainWindow(name, surname, date, full_time, lat, lon, astro_data, panchang_data)
            self.main_win.showMaximized()
            self.close()

    def save_user_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save User Data", "", "RogaHora Data (*.rhd)", options=options
        )

        if file_path:
            if not file_path.endswith(".rhd"):
                file_path += ".rhd"

            data = {
                "first_name": self.first_name.text(),
                "last_name": self.last_name.text(),
                "date": self.dob.date().toString("dd-MM-yyyy"),
                "time": self.time.time().toString("hh:mm"),
                "ampm": self.ampm.currentText(),
                "state": self.state_dropdown.currentText(),
                "city": self.city_dropdown.currentText()
            }

            try:
                with open(file_path, "w") as f:
                    json.dump(data, f)
                QMessageBox.information(self, "Saved", "User data saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {e}")
