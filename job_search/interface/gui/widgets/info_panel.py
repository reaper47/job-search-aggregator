import webbrowser
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QWidget, QPushButton, QFormLayout, QGroupBox,
                               QTextEdit, QVBoxLayout, QHBoxLayout, QLabel)
from PySide2.QtWebEngineWidgets import QWebEngineView
from job_search.interface.gui.styles.styles import Style


class JobInfoPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(Style.INFO_PANEL.value)

        self.__create_title()
        self.__create_description_groupbox()
        self.__create_res_req_groupbox()
        self.__create_contact_groupbox()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.horizontal_groupbox)
        main_layout.addLayout(self.restrictions_layout)
        main_layout.addLayout(self.contact_layout)

        self.setLayout(main_layout)

    def __create_title(self):
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPixelSize(17)
        self.title.setFont(font)
        self.title.setStyleSheet('padding: 12px; border: 1px solid #212121; border-radius: 10px;')

    def __create_description_groupbox(self):
        self.horizontal_groupbox = QGroupBox('Description:')

        self.description = QTextEdit()
        self.description.setReadOnly(True)

        layout = QHBoxLayout()
        layout.addWidget(self.description, Style.TWO_THIRDS.value)

        window = QWidget()
        window.setMinimumSize(320, 625)
        self.web = QWebEngineView(window)
        self.web.setHtml(self.generate_html_map(0, 0))
        self.webpage = self.web.page()
        layout.addWidget(self.web, Style.ONE_THIRD.value)

        self.horizontal_groupbox.setLayout(layout)

    def generate_html_map(self, lat, lng):
        initialize = ("var earth; var marker; var zoomLevel = 3.5;"
                      "function initialize() {"
                      "  var options={zoom: zoomLevel, position: [" + str(lat) + "," + str(lng) + "]};"
                      "  earth = new WE.map('earth_div', options);"
                      "  WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(earth);"
                      f" add_marker({lat}, {lng})"
                      "}"
                      "function rm_marker() {marker.removeFrom(earth)}"
                      "function add_marker(lat,lng) {"
                      "  try {rm_marker()} catch(e) {}"
                      "  marker = WE.marker([lat,lng]).addTo(earth);"
                      "  earth.setView([lat,lng], zoomLevel);}")

        style = ("html, body{padding: 0; margin: 0;}"
                 "#earth_div{top: 0; right: 0; bottom: 0; left: 0; position: absolute !important;}")

        return f'''
            <!DOCTYPE HTML>
            <html>
              <head>
                <script src="http://www.webglearth.com/v2/api.js"></script>
                <script>{initialize}</script>
              <style>{style}</style>
              </head>
              <body onload="initialize()">
                <div id="earth_div"></div>
              </body>
            </html>
        '''

    def __create_res_req_groupbox(self):
        hbox = QHBoxLayout()
        restrictions_group = QGroupBox('Restrictions:')
        self.restrictions = QTextEdit()
        self.restrictions.setReadOnly(True)
        hbox.addWidget(self.restrictions)
        restrictions_group.setLayout(hbox)

        hbox = QHBoxLayout()
        requirements_group = QGroupBox('Requirements:')
        self.requirements = QTextEdit()
        self.requirements.setReadOnly(True)
        hbox.addWidget(self.requirements)
        requirements_group.setLayout(hbox)

        self.restrictions_layout = QHBoxLayout()
        self.restrictions_layout.addWidget(requirements_group, Style.TWO_THIRDS.value)
        self.restrictions_layout.addWidget(restrictions_group, Style.ONE_THIRD.value)

    def __create_contact_groupbox(self):
        hbox = QHBoxLayout()
        about_group = QGroupBox('About:')
        self.about = QTextEdit()
        self.about.setReadOnly(True)
        hbox.addWidget(self.about)
        about_group.setLayout(hbox)

        layout = QFormLayout()
        contact_group = QGroupBox('Contact Info')
        self.contact_name = QLabel()
        self.contact_email = QLabel()
        self.contact_website = QPushButton('Apply')
        self.contact_website.clicked.connect(lambda: webbrowser.open(self.apply_website))
        layout.addRow(QLabel('Contact:'), self.contact_name)
        layout.addRow(QLabel('Email:'), self.contact_email)
        layout.addRow(QLabel('Website:'), self.contact_website)
        contact_group.setLayout(layout)

        self.contact_layout = QHBoxLayout()
        self.contact_layout.addWidget(about_group, Style.TWO_THIRDS.value)
        self.contact_layout.addWidget(contact_group, Style.ONE_THIRD.value)

    def set_contact_info(self, contact: str, email: str, website: str, company: str):
        self.contact_name.setText(contact)
        self.contact_email.setText(email)

        self.apply_website = website
        if self.apply_website is None:
            self.apply_website = f'https://duckduckgo.com/?q={company}&t=ffab&ia=web'
