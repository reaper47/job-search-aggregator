from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTextEdit


class JobInfoPanel(QTextEdit):

    def __init__(self):
        super().__init__()
        self.setViewportMargins(20, 20, 20, 20)
        self.setStyleSheet("""QTextEdit {
                                border: none;
                                border-bottom: 1px solid #eee;
                                background: #fff;
                                color: #333;
                            }""")
        font = QFont()
        font.setPixelSize(16)
        document = self.document()
        document.setDefaultFont(font)
