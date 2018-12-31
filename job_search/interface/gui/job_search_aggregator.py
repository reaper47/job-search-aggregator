import sys
from PySide2.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PySide2.QtGui import QIcon
from job_search.interface.gui.orchestrator import Orchestrator
from job_search.interface.assets.assets_mapper import AssetsMapper


class JobSearchAggregator(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Job Search Aggregator')
        self.resize(1024, 768)
        self.__center()

        self.orchestrator = Orchestrator(self)
        self.setCentralWidget(self.orchestrator)

    def __center(self):
        geometry = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = JobSearchAggregator()
    window.setWindowIcon(QIcon(AssetsMapper.APP_ICON.value))
    window.show()

    sys.exit(app.exec_())
