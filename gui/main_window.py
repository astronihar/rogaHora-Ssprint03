from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTabWidget, QToolBar, QAction, QMainWindow
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

from gui.chakras.vargasTabWidget import VargasTabWidget
from gui.basic import BasicsTab
from gui.start_form import StartForm


class MainWindow(QMainWindow):
    def __init__(self, name, surname, date, time, lat, lon, astro_data, panchang_data):
        super().__init__()
        self.setWindowTitle(f"RogaHora - Chart Viewer for {name} {surname}")
        self.setGeometry(100, 100, 1400, 900)

        # 🧠 Store Data
        self.name = name
        self.surname = surname
        self.date = date
        self.time = time
        self.lat = lat
        self.lon = lon
        self.astro_data = astro_data
        self.panchang_data = panchang_data
        self.birth_form = None

        # 🌟 Central Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 🛠 Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.toolbar.addAction(QAction(QIcon(), "New", self))
        self.toolbar.addAction(QAction(QIcon(), "Open", self))
        self.toolbar.addAction(QAction(QIcon(), "Save", self))

        edit_action = QAction(QIcon(), "Edit", self)
        self.toolbar.addAction(edit_action)
        from gui.toolmenus.edit_toolbar_menu import attach_dropdown_to_edit_action
        attach_dropdown_to_edit_action(self, self.toolbar, edit_action)

        self.toolbar.addAction(QAction(QIcon(), "Help", self))
        self.toolbar.addSeparator()

        # 🎯 Icon Bar
        self.iconbar = QToolBar("Icon Navigation Bar")
        self.iconbar.setIconSize(QSize(28, 28))
        self.iconbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.layout.addWidget(self.iconbar)

        self.iconbar.addAction(QAction(QIcon("icons/newicon.png"), "D1 Chart", self))
        self.iconbar.addAction(QAction(QIcon("icons/saveicon.png"), "D9 Navamsa", self))
        self.iconbar.addAction(QAction(QIcon("icons/d30.png"), "D30 Trimsamsa", self))
        self.iconbar.addAction(QAction(QIcon("icons/transit.png"), "Transits", self))
        self.iconbar.addAction(QAction(QIcon("icons/strength.png"), "Strengths", self))
        self.iconbar.addAction(QAction(QIcon("icons/remedy.png"), "Remedies", self))
        self.iconbar.addSeparator()
        self.iconbar.addAction(QAction(QIcon("icons/settings.png"), "Settings", self))

        # 📑 Tabs
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        self.load_tabs()

        self.setStyleSheet("""
            QTabBar::tab {
                font-size: 13px;
                padding: 8px 15px;
                margin-right: 3px;
            }
            QTabBar::tab:selected {
                font-weight: bold;
                background-color: #f0f0f0;
                font-size: 11px;
            }
            QToolBar {
                font-size: 10px;
                spacing: 10px;
            }
            QToolButton {
                font-size: 15px;
                padding: 6px;
            }
        """)

    def load_tabs(self):
        self.tabs.clear()
        self.tabs.addTab(self.create_chakras_tab(self.astro_data), "Chakras")
        self.tabs.addTab(BasicsTab(self.astro_data, self.panchang_data), "Basics")
        self.tabs.addTab(self.create_panchang_tab(self.panchang_data), "Panchang")
        self.tabs.addTab(QLabel("Strength data..."), "Strengths")
        self.tabs.addTab(QLabel("Vimshottari Dasha..."), "Dasas")
        self.tabs.addTab(QLabel("Transits..."), "Transits")
        self.tabs.addTab(QLabel("Tajaka charts..."), "Tajaka")
        self.tabs.addTab(QLabel("Tithi Pravesha..."), "Tithi Pravesha")
        self.tabs.addTab(QLabel("Mundane info..."), "Mundane")
        self.tabs.addTab(QLabel("Remedies..."), "Remedies")
        self.tabs.addTab(QLabel("Research..."), "Research")
        self.tabs.addTab(QLabel("Learn Medical Astrology..."), "Learn Medical Astrology")

        # 🔁 Show "Basics" tab first
        self.tabs.setCurrentIndex(1)

    def create_chakras_tab(self, astro_data):
        container = QWidget()
        layout = QVBoxLayout()
        sub_tabs = QTabWidget()
        sub_tabs.addTab(VargasTabWidget(astro_data), "Many Vargas")
        sub_tabs.addTab(QLabel("Mixed 2-Vargas coming soon..."), "Mixed 2-Vargas")
        sub_tabs.addTab(QLabel("Kalachakra data..."), "Kalachakra")
        sub_tabs.addTab(QLabel("Sarvatobhadra..."), "Sarvatobhadra")
        sub_tabs.addTab(QLabel("Kota Chakra..."), "Kota Chakra")
        layout.addWidget(sub_tabs)
        container.setLayout(layout)
        return container

    def create_panchang_tab(self, panchang_data):
        container = QWidget()
        layout = QVBoxLayout()
        for key, value in panchang_data.items():
            layout.addWidget(QLabel(f"<b>{key.capitalize()}:</b> {value}"))
        layout.addStretch()
        container.setLayout(layout)
        return container

    def open_birthdata_editor(self):
        try:
            if self.birth_form and self.birth_form.isVisible():
                self.birth_form.raise_()
                self.birth_form.activateWindow()
                return
        except AttributeError:
            pass

        self.birth_form = StartForm(update_callback=self.update_chart_data)
        self.birth_form.setAttribute(Qt.WA_DeleteOnClose, False)
        self.birth_form.show()

    def update_chart_data(self, name, surname, date, time, lat, lon, astro_data, panchang_data):
        self.name = name
        self.surname = surname
        self.date = date
        self.time = time
        self.lat = lat
        self.lon = lon
        self.astro_data = astro_data
        self.panchang_data = panchang_data
        self.setWindowTitle(f"RogaHora - Chart Viewer for {name} {surname}")
        self.load_tabs()
