from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QListView
from job_search.interface.gui.widgets.list_item import ItemModel, ItemDelegate, Item
from job_search.interface.gui.styles.styles import Style, Color
from job_search.domain.jobs.value_objects.job_type import JobInfo


class ListView(QListView):

    def __init__(self):
        super().__init__()
        self.selected = 0
        self.setStyleSheet(Style.QLIST_VIEW.value)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setAlternatingRowColors(True)

        color = QColor(Color.GREY.value)
        palette = QPalette()
        palette.setColor(QPalette.Highlight, color)
        self.setPalette(palette)

        self.model = ItemModel(0, 1, self)
        self.setModel(self.model)
        self.setItemDelegate(ItemDelegate())
        self.model.rowsAboutToBeRemoved.connect(self.__items_deleted)

    def __items_deleted(self):
        self.setCurrentIndex(self.model.index(self.selected))

    def append(self, job: JobInfo):
        item = self.__build_item(job)
        self.model.addItem(item)

    def insert(self, job: JobInfo, row: int):
        self.selected = row
        item = self.__build_item(job)
        self.model.insertItem(item, row)
        self.setCurrentIndex(self.model.index(row))

    def update(self, job: JobInfo):
        item = self.__build_item(job)
        self.model.updateItem(self.currentIndex(), item)

    def __build_item(self, job: JobInfo) -> Item:
        nchars = 30 if job.pinned else 35
        title = self.__cap(job.title, nchars)
        company = self.__cap(job.company, 35)
        location = self.__cap(str(job.location), 42)

        return Item(title=title,
                    company=company,
                    location=location,
                    pinned=job.pinned)

    def __cap(self, text: str, nchars: int) -> str:
        return text if len(text) <= nchars else text[:nchars] + '…'

    def clear(self):
        self.model.clear()

    def select(self, row: int):
        if 0 <= row < self.model.rowCount():
            self.setCurrentIndex(self.model.index(row))
            self.selected = row

    def remove(self, row: int):
        self.model.removeItem(row)
        count = self.model.rowCount()
        self.selected = row if row < count else row - 1
        self.setCurrentIndex(self.model.index(self.selected))
