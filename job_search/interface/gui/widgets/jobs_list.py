from PySide2.QtWidgets import (QLabel, QWidget, QGridLayout, QMainWindow,
                               QHBoxLayout, QListWidget, QListWidgetItem)


class QJobListItemWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = QLabel()
        self.company = QLabel()
        self.location = QLabel()

        vlayout = QGridLayout()
        vlayout.addWidget(self.title, 0, 0, 1, 2)
        vlayout.addWidget(self.company, 1, 0, 1, 2)
        vlayout.addWidget(self.location, 0, 1, 1, 1, 2)
        vlayout.setSpacing(20)

        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.allQHBoxLayout.addLayout(vlayout, 0)
        self.setLayout(self.allQHBoxLayout)

        self.title.setStyleSheet('color: rgb(0, 0, 255); float:right;')
        self.location.setStyleSheet('color: rgb(255, 0, 0);')

    def set_title(self, text):
        self.title.setText(text)

    def set_location(self, text):
        self.location.setText(text)

    def set_company(self, imagePath):
        self.company.setText(imagePath)


class JobsListWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QListView with QItemDelegate")
        self.setStyleSheet("""QMainWindow {
                                background: #fff;
                              }
                              QMainWindow::separator {
                                height: 0;
                                border: none;
                                width: 0;
                              }""")
        self.setUnifiedTitleAndToolBarOnMac(True)

        self.job_list = QListWidget(self)

        items = [
            (
                'Python Backend\nDeveloper',
                'Biarri\n',
                'Brisbane, Queensland, Australia'
            ),
            (
                'Web Developer\n(Django/ Python)',
                'Newcastle\nUniversity',
                'Newcastle-upon-Tyne,\nTyne and Wear,\nUnited Kingdom'
            ),
            (
                'Senior Infrastructure\nDeveloper (Python)',
                'Bromium',
                'Cambridge, Cambridgeshire,\nUnited Kingdom'
            )
        ]*10

        self.job_list.selectionModel().currentChanged.connect(self.on_row_changed)

        for index, name, icon in items:
            job_item = QJobListItemWidget()
            job_item.set_title(index)
            job_item.set_location(name)
            job_item.set_company(icon)

            list_item_widget = QListWidgetItem(self.job_list)
            list_item_widget.setSizeHint(job_item.sizeHint())
            self.job_list.addItem(list_item_widget)
            self.job_list.setItemWidget(list_item_widget, job_item)

        self.setCentralWidget(self.job_list)

    def on_row_changed(self, current, previous):
        print(current)
