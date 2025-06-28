from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from logic.chakras import vargas

class VargasTabWidget(QWidget):
    def __init__(self, astro_data):
        super().__init__()
        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        html = self.generate_html(astro_data)
        self.browser.setHtml(html)
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def generate_html(self, astro_data):
        asc_deg = astro_data["ascendant"]["degree"]
        planets_raw = {k: v["degree"] for k, v in astro_data["planets"].items()}

        charts = {
           "D1": vargas.get_d1_chart(astro_data),
           "D3": vargas.get_d3_chart(planets_raw, asc_deg),
           "D6": vargas.get_d6_chart(planets_raw, asc_deg),
           "D9": vargas.get_d9_chart(planets_raw, asc_deg),
           "D30": vargas.get_d30_chart(planets_raw, asc_deg),
           "D60": vargas.get_d60_chart(planets_raw, asc_deg),
        }

        def chart_to_svg(chart):
            svg = '<svg viewBox="-120 -120 240 240" width="450" height="450">'
            svg += """
            <rect x="-100" y="-100" width="200" height="200" fill="white" stroke="black"/>
            <line x1="-100" y1="-100" x2="100" y2="100" stroke="black"/>
            <line x1="100" y1="-100" x2="-100" y2="100" stroke="black"/>
            <line x1="0" y1="-100" x2="100" y2="0" stroke="black"/>
            <line x1="100" y1="0" x2="0" y2="100" stroke="black"/>
            <line x1="0" y1="100" x2="-100" y2="0" stroke="black"/>
            <line x1="-100" y1="0" x2="0" y2="-100" stroke="black"/>
            """

            positions = {
                1:  (0, 55), 2: (-50, 80), 3: (-80, 50), 4: (-60, 0),
                5: (-80, -45), 6: (-50, -85), 7: (0, -40), 8: (60, -80),
                9: (90, -50), 10: (40, 0), 11: (80, 50), 12: (55, 80)
            }

            for house in range(1, 13):
                x, y = positions[house]
                y = -y
                planets = chart[house]['planets']
                zodiac = chart[house]['zodiac']
                for i, p in enumerate(planets):
                    svg += f'<text x="{x}" y="{y + i*9 - 6}" font-size="8" fill="darkred" text-anchor="middle">{p}</text>'
                svg += f'<text x="{x}" y="{y + len(planets)*9 + 4}" font-size="7" fill="black" text-anchor="middle">{zodiac}</text>'
            svg += '</svg>'
            return svg

        html = """
        <html><head><style>
        body { font-family: Arial; background-color: #f4f4f4; }
        .charts { display: flex; flex-wrap: wrap; gap: 10px; padding: 10px; }
        .chart { background: white; border: 1px solid #ccc; width: 450px; padding: 5px; }
        .chart h4 { margin: 0; background: #eee; padding: 4px; font-size: 14px; text-align: center; }
        </style></head><body><div class="charts">
        """
        for key, chart in charts.items():
            html += f'<div class="chart"><h4>{key} Chart</h4>{chart_to_svg(chart)}</div>'
        html += '</div></body></html>'
        return html


# ✅ REUSABLE FUNCTION for other tabs like Basics
def create_chart_group_box(astro_data):
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWidgets import QVBoxLayout

    html = VargasTabWidget(astro_data).generate_html(astro_data)
    box = QGroupBox("Divisional Charts")
    layout = QVBoxLayout()
    view = QWebEngineView()
    view.setHtml(html)
    layout.addWidget(view)
    box.setLayout(layout)
    return box
