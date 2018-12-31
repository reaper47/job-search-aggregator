from PySide2.QtWidgets import QWidget, QGridLayout
from job_search.interface.gui.widgets.jobs_list import JobsListWidget


class Orchestrator(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        grid = QGridLayout()
        grid.setSpacing(10)

        jobs_list1 = JobsListWidget()
        jobs_list2 = JobsListWidget()

        grid.addWidget(jobs_list1, 0, 2, 1, 1)
        grid.addWidget(jobs_list2, 0, 0, 1, 2)

        self.setLayout(grid)
