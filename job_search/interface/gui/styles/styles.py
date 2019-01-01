from enum import Enum


class Color(Enum):
    GREY = '#999'
    LIGHT_BLACK = '#2C3A47'


class Styles(Enum):
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
