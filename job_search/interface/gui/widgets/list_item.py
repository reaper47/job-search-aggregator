import copy
from PySide2.QtCore import QModelIndex, QAbstractListModel, Qt, QSize
from PySide2.QtGui import QColor, QImage, QBrush
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle
from job_search.interface.assets.assets_mapper import AssetsMapper
from job_search.interface.gui.styles.styles import Style, Color


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

    def addItem(self, item: Item):
        nrows = self.rowCount()
        self.beginInsertRows(QModelIndex(), nrows, nrows)
        self.items.append(item)
        self.endInsertRows()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        del self.items[:]
        self.endRemoveRows()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        item = self.getItem(index)
        if item is not None:
            if role == Qt.SizeHintRole:
                return QSize(100, 80)
            elif role == ItemModel.TitleRole:
                return item.title
            elif role == ItemModel.CompanyRole:
                return item.company
            elif role == ItemModel.LocationRole:
                return item.location
            elif role == ItemModel.PinRole:
                return item.pinned

    def getItem(self, index: QModelIndex):
        row = index.row()
        if self.__is_index_valid(index):
            return self.items[row]

    def __is_index_valid(self, index: QModelIndex) -> bool:
        return index.isValid() and 0 <= index.row() < self.rowCount()

    def rowCount(self, index=QModelIndex()):
        return len(self.items)

    def insertItem(self, item: Item, index: QModelIndex):
        self.beginInsertRows(QModelIndex(), index, index)
        self.items.insert(index, item)
        self.endInsertRows()

    def removeItem(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.items[row]
        self.endRemoveRows()

    def updateItem(self, index: QModelIndex, item: Item):
        self.setData(index, item)

    def setData(self, index: QModelIndex, item: Item, role=Qt.EditRole):
        self.items[index.row()] = item
        self.dataChanged.emit(index, index, [ItemModel.TitleRole, ItemModel.CompanyRole,
                                             ItemModel.LocationRole, ItemModel.PinRole])


class ItemDelegate(QStyledItemDelegate):

    def __init__(self):
        super().__init__()

    def paint(self, painter, option, index):
        options = QStyleOptionViewItem(option)
        style = options.widget.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)
        painter.save()
        rectangle = option.rect

        if option.state & QStyle.State_Selected:
            pin = QImage(AssetsMapper.PINNED_SELECTED.value)
            painter.fillRect(rectangle, QBrush(QColor(Color.ITEM_SELECTED.value)))
        else:
            pin = QImage(AssetsMapper.PINNED.value)

        rectangle.setX(10)
        pin.setDevicePixelRatio(2.0)
        font = painter.font()
        font.setPixelSize(Style.FONT_SIZE.value)
        painter.setFont(font)
        pin_rect = copy.copy(rectangle)
        pin_rect.setHeight(32)
        pin_rect.setWidth(32)
        yoffset = 42

        # Draw title
        title = index.data(ItemModel.TitleRole)
        pinned = index.data(ItemModel.PinRole)

        pin_point = rectangle.topLeft()
        pin_point.setY(pin_point.y() + 32)
        pin_rect.setTopLeft(pin_point)
        point = option.rect.topLeft()
        point.setY(point.y() - 40)
        rectangle.setTopLeft(point)
        pin_point.setY(pin_point.y() - 20)
        pin_rect.setTopLeft(pin_point)
        pin_rect.setHeight(16)
        pin_rect.setWidth(16)

        if pinned:
            painter.drawImage(pin_rect, pin)
            title = f'      {title}'

        painter.setPen(QColor(Color.TITLE.value))
        painter.drawText(rectangle, Qt.AlignVCenter, title)

        # Draw company
        company = index.data(ItemModel.CompanyRole)

        point = option.rect.topLeft()
        point.setY(point.y() + yoffset)
        rectangle.setTopLeft(point)
        font.setPixelSize(Style.FONT_SIZE.value)
        painter.setFont(font)
        painter.setPen(QColor(Color.COMPANY.value))
        painter.drawText(rectangle, Qt.AlignVCenter, company)

        # Draw location
        location = index.data(ItemModel.LocationRole)

        point = option.rect.topLeft()
        point.setY(point.y() + yoffset)
        rectangle.setTopLeft(point)
        font.setPixelSize(Style.FONT_SIZE.value - 2)
        painter.setFont(font)
        painter.setPen(QColor(Color.LOCATION.value))
        painter.drawText(rectangle, Qt.AlignVCenter, location)

        painter.restore()
