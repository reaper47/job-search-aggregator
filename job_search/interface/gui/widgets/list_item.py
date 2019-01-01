import copy
from PySide2.QtCore import QModelIndex, QAbstractListModel, Qt, QSize
from PySide2.QtGui import QColor, QImage
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle
from job_search.interface.assets.assets_mapper import AssetsMapper


class Item:
    __slots__ = ('title', 'company', 'location', 'pinned')

    def __init__(self, title: str, company: str, location: str, pinned: bool):
        self.title = title
        self.company = company
        self.location = location
        self.pinned = pinned


class ItemModel(QAbstractListModel):
    TitleRole, CompanyRole, LocationRole, PinRole = range(Qt.UserRole, Qt.UserRole + 4)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.items = []

    def addItem(self, item):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(item)
        self.endInsertRows()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self.items = []
        self.endRemoveRows()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if 0 <= index.row() < self.rowCount():
            item = self.items[index.row()]

            if role == Qt.SizeHintRole:
                return QSize(100, 80)
            elif role == ItemModel.TitleRole:
                return item.title
            elif role == ItemModel.CompanyRole:
                if item.company:
                    return item.company
                return None
            elif role == ItemModel.LocationRole:
                print(item.location)
            elif role == ItemModel.PinRole:
                return item.pinned

    def getItem(self, index):
        row = index.row()
        if index.isValid() and 0 <= row < self.rowCount():
            return self.items[row]

    def insertItem(self, item, index):
        self.beginInsertRows(QModelIndex(), index, index)
        self.items.insert(index, item)
        self.endInsertRows()

    def removeItem(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.items[row]
        self.endRemoveRows()

    def rowCount(self, index=QModelIndex()):
        return len(self.items)

    def setData(self, index, item, role=Qt.EditRole):
        self.items[index.row()] = item
        self.dataChanged.emit(index, index, [ItemModel.TitleRole,
                              ItemModel.CompanyRole, ItemModel.PinRole])

    def updateItem(self, index, item):
        self.setData(index, item)


class ItemDelegate(QStyledItemDelegate):

    def __init__(self):
        super().__init__()

    def paint(self, painter, option, index):
        options = QStyleOptionViewItem(option)
        style = options.widget.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)
        painter.save()

        color = QColor()
        if option.state & QStyle.State_Selected:
            color.setNamedColor("#FFF")
            painter.setPen(color)
            pin = QImage(AssetsMapper.PINNED_SELECTED.value)
        else:
            color.setNamedColor("#333")
            painter.setPen(color)
            pin = QImage(AssetsMapper.PINNED.value)

        pin.setDevicePixelRatio(2.0)
        title = index.data(ItemModel.TitleRole)
        company = index.data(ItemModel.CompanyRole)
        pinned = index.data(ItemModel.PinRole)
        font = painter.font()
        font.setPixelSize(16)
        painter.setFont(font)
        rectangle = option.rect
        rectangle.setX(10)
        pin_rect = copy.copy(rectangle)
        pin_rect.setHeight(32)
        pin_rect.setWidth(32)

        if title:
            pin_point = rectangle.topLeft()
            pin_point.setY(pin_point.y() + 32)
            pin_rect.setTopLeft(pin_point)

            if company:
                point = option.rect.topLeft()
                point.setY(point.y() - 20)
                rectangle.setTopLeft(point)
                pin_point.setY(pin_point.y() - 10)
                pin_rect.setTopLeft(pin_point)

            pin_rect.setHeight(16)
            pin_rect.setWidth(16)

            if pinned:
                painter.drawImage(pin_rect, pin)
                title = f'     {title}'
            painter.drawText(rectangle, Qt.AlignVCenter, title)

        if company:
            point = option.rect.topLeft()
            point.setY(point.y() + 40)
            rectangle.setTopLeft(point)
            font.setPixelSize(12)
            painter.setFont(font)
            painter.drawText(rectangle, Qt.AlignVCenter, company)

        painter.restore()
