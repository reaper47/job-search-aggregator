import sys
from PySide2.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QDockWidget, QWidget, QAction
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QKeySequence
from job_search.interface.assets.assets_mapper import AssetsMapper
from job_search.interface.gui.styles.styles import Styles
from job_search.interface.gui.widgets.info_panel import JobInfoPanel
from job_search.interface.gui.widgets.jobs_list import ListView
from job_search.application.services.jobs.job_service import JobService
from job_search.application.services.jobs.job_factory import JobFactory
from job_search.repository.jobs.sqlite_job_repository import SQLiteJobRepository


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(Styles.QMAIN_WINDOW.value)
        self.setWindowTitle('Job Search Aggregator')
        self.setWindowIcon(QIcon(AssetsMapper.APP_ICON.value))

        self.resize(1024, 768)
        self.__center()
        self.__add_close_action()

    def __center(self):
        geometry = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())

    def __add_close_action(self):
        self.action_exit = QAction(('E&xit'), self)
        self.action_exit.setShortcuts([QKeySequence('Ctrl+W'), QKeySequence('Ctrl+Q')])
        self.addAction(self.action_exit)
        self.action_exit.triggered.connect(self.close)


class JobSearchAggregator:

    def __init__(self, job_service):
        self.app = QApplication(sys.argv)
        self.job_service = job_service

        self.list_view = ListView()
        self.info_panel = JobInfoPanel()

        self.dock = QDockWidget()
        self.dock.setWidget(self.list_view)
        self.dock.setFeatures(self.dock.NoDockWidgetFeatures)
        self.dock.setTitleBarWidget(QWidget())

        self.main_window = MainWindow()
        self.main_window.setCentralWidget(self.info_panel)
        self.main_window.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.list_view.selectionModel().currentChanged.connect(self.list_item_selected)

    def run(self):
        self.__populate_item_model()
        self.list_view.select(0)

        self.main_window.show()
        sys.exit(self.app.exec_())

    def __populate_item_model(self):
        jobs = self.job_service.gather_all_jobs()
        self.uids = [job.uid for job in jobs]
        [self.list_view.append(job) for job in jobs]

    def list_item_selected(self, index):
        job_id = self.uids[index.row()]
        job = self.job_service.consult_job(job_id)
        print(job)


if __name__ == '__main__':
    service = JobService(JobFactory(), SQLiteJobRepository())
    app = JobSearchAggregator(service)
    app.run()
