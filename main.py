from PyQt5.QtWidgets import QApplication
import sys
import json
from gui.start_form import StartForm
from gui.main_window import MainWindow
from logic.geo_lookup import load_city_data
from logic.astroniharEng import get_astro_data
from logic.panchangWrapper import prepare_panchang_payload

app = QApplication(sys.argv)

if len(sys.argv) > 1 and sys.argv[1].endswith(".rhd"):
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            user_data = json.load(f)

        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        date = user_data["date"]
        time = user_data["time"]
        ampm = user_data["ampm"]
        full_time = f"{time} {ampm}"
        state = user_data["state"]
        city = user_data["city"]

        city_data = load_city_data()
        lat, lon = city_data[state][city]

        # 🔍 Get Astro and Panchang data
        astro_data = get_astro_data(date, full_time, lat, lon)
        panchang_data = prepare_panchang_payload(date, time, ampm, lat, lon)

        window = MainWindow(first_name, last_name, date, full_time, lat, lon, astro_data, panchang_data)
        window.showMaximized()

    except Exception as e:
        print(f"[ERROR] Failed to load .rhd file: {e}")
        window = StartForm()
        window.show()
else:
    window = StartForm()
    window.show()

sys.exit(app.exec_())
