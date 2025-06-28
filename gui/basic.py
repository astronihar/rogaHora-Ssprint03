from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QScrollArea, QSizePolicy, QHeaderView, QLabel
)
from PyQt5.QtCore import Qt
from gui.chakras.vargasTabWidget import create_chart_group_box
from logic.karakas import assign_karakas  # ✅ Import here


class BasicsTab(QWidget):
    def __init__(self, astro_data, panchang_data):
        super().__init__()

        # ✅ Assign karakas before rendering
        if "planets" in astro_data:
            astro_data["planets"], astro_data["karakas"] = assign_karakas(astro_data["planets"])

        layout = QHBoxLayout()

        # 🌗 Left Panel
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        planet_table = self.create_planet_table(astro_data)
        planet_scroll = QScrollArea()
        planet_scroll.setWidgetResizable(True)
        planet_scroll.setWidget(planet_table)
        planet_scroll.setMinimumHeight(280)

        panchang_display = self.create_panchang_display(panchang_data)
        panchang_scroll = QScrollArea()
        panchang_scroll.setWidgetResizable(True)
        panchang_scroll.setWidget(panchang_display)
        panchang_scroll.setMinimumHeight(220)
        panchang_scroll.setFrameShape(0)
        panchang_scroll.setStyleSheet("QScrollArea { border: none; }")

        left_layout.addWidget(planet_scroll)
        left_layout.addWidget(panchang_scroll)
        layout.addWidget(left_container, 3)

        # 🗺️ Right Panel
        chart_box = create_chart_group_box(astro_data)
        chart_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(chart_box, 5)

        self.setLayout(layout)

    def create_planet_table(self, astro_data):
        planets = astro_data.get("planets", {})
        asc = astro_data.get("ascendant", {})

        headers = ["#", "Planet", "Deg°", "Sign", "Nakshatra", "Pada"]
        row_count = len(planets) + 1

        table = QTableWidget(row_count, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.setShowGrid(True)

        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                font-size: 15px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                font-weight: bold;
                font-size: 15px;
                padding: 6px;
            }
        """)

        # Ascendant row
        table.setItem(0, 0, QTableWidgetItem("0"))
        table.setItem(0, 1, QTableWidgetItem("Asc"))
        table.setItem(0, 2, QTableWidgetItem(str(round(asc.get("degree", 0), 5))))
        table.setItem(0, 3, QTableWidgetItem(asc.get("zodiac", "")))
        table.setItem(0, 4, QTableWidgetItem(asc.get("nakshatra", "")))
        table.setItem(0, 5, QTableWidgetItem(str(asc.get("pada", ""))))

        # Planet rows
        for i, (planet, data) in enumerate(planets.items(), start=1):
            karaka = data.get("karaka", "")
            display_name = f"{planet} ({karaka})" if karaka else planet

            table.setItem(i, 0, QTableWidgetItem(str(i)))
            table.setItem(i, 1, QTableWidgetItem(display_name))
            table.setItem(i, 2, QTableWidgetItem(str(round(data["degree"], 5))))
            table.setItem(i, 3, QTableWidgetItem(data["zodiac"]))
            table.setItem(i, 4, QTableWidgetItem(data["nakshatra"]))
            table.setItem(i, 5, QTableWidgetItem(str(data["pada"])))

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        table.setMinimumWidth(700)

        return table

    def create_panchang_display(self, panchang_data):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        if panchang_data:
            for key, value in panchang_data.items():
                key_str = f"{key.replace('_', ' ').title():<16} :"
                label = QLabel(f"{key_str}  {value}")
                label.setStyleSheet("font-size: 15px; padding: 4px;")
                layout.addWidget(label)
        else:
            layout.addWidget(QLabel("Panchang data not available."))

        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        container.adjustSize()
        return container
