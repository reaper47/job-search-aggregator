from enum import Enum


class Color(Enum):
    GREY = '#999'
    LIGHT_BLACK = '#2C3A47'
    ITEM_SELECTED = '#fed330'
    ITEM_NOT_SELECTED = '#333'
    TITLE = '#212121'
    LOCATION = '#00796B'
    COMPANY = '#455A64'


class Style(Enum):
    ONE_THIRD = (1/3)*100
    TWO_THIRDS = (2/3)*100
    HALF = (1/2)*100
    FONT_SIZE = 12
    QMAIN_WINDOW = """
        QMainWindow {
            background: #FFF;
        }
        QMainWindow::separator {
            border: none;
            height: 0;
            width: 0;
        }
    """
    QLIST_VIEW = """
        QListView {
            background: #EEE;
            border: none;
        }
        QScrollBar:vertical {
            background: #CAD3C8;
            border: none;
            margin: 20px 0px 20px 0px;
            width: 8px;
        }
        QScrollBar::handle:vertical {
            background: #2f3542;
        }
        QScrollBar::add-line:vertical {
            background: #2C3A47;
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: #2C3A47;
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
    """
    INFO_PANEL = """
        QTextEdit {
            border: none;
            background: #fff;
        }
        QLabel {
            padding-bottom:  25px;
        }
        QPushButton {
            padding:  12px;
        }
        QScrollBar:vertical {
            border: none;
            margin: 20px 0px 20px 0px;
            width: 9px;
        }
        QScrollBar::add-line:vertical {
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
    """
