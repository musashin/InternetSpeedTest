import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import version
import periodictest
import click


class Worker(QtCore.QRunnable):
    """
    Work Thread
    """
    def __init__(self, speed_test):
        """
        Worker thread constructor
        :param speed_test: speed test object
        """
        super(Worker, self).__init__()
        self.speed_test = speed_test

    @QtCore.pyqtSlot()
    def run(self):
        """
        On thread run event, start the periodic speed test
        :return:
        """
        self.speed_test.start()


class AboutDialog(QtWidgets.QDialog):
    """
    About Dialog box
    """
    def __init__(self, period_in_min):
        """
        Constructor
        :param period_in_min: speed test period in minutes
        """
        super().__init__(parent=None)

        self.setWindowTitle("About Internet Speed Test")

        QBtn = QtWidgets.QDialogButtonBox.Ok

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.close)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Data collected every {!s} minutes by Internet Speed Test Version {!s}".
                                   format(period_in_min, version.__version__))
        self.layout.addWidget(message)
        message2 = QtWidgets.QLabel("AQUARUS RULES!!!!")
        self.layout.addWidget(message2)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    Qt System Tray Application
    """

    def __init__(self, icon, parent, speed_test):
        """
        Constructor
        :param icon: icon object
        :param parent: parent widget
        :param speed_test: speed test object
        """

        self.pause = False
        self.speed_test = speed_test

        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        aboutAction = menu.addAction("About")
        aboutAction.triggered.connect(self.about)
        aboutAction.setStatusTip("About")

        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        exitAction.setStatusTip("Exit Tool")

        self.pauseAction = menu.addAction("Pause")
        self.pauseAction.triggered.connect(self.pause_data_collection)
        self.pauseAction.setStatusTip("Pause/Resume Data Collection")

        # Pass the function to execute
        self.threadpool = QtCore.QThreadPool()
        worker = Worker(speed_test)
        self.threadpool.start(worker)

        self.setContextMenu(menu)


    def about(self):
        """
        Open the Abou tdialog box
        :return:
        """
        dlg = AboutDialog(self.speed_test.get_period_in_min())
        dlg.exec_()

    def exit(self):
        """
        Exit Handler for the Qt App
        :return:
        """
        QtCore.QCoreApplication.exit()

    def pause_data_collection(self):
        """
        Pause data collection on Call
        :return: None
        """
        self.pause = not self.pause

        self.pauseAction.setText("Resume" if self.pause else "Pause")

        if self.pause:
            self.speed_test.pause_collection()
        else:
            self.speed_test.resume_collection()


def start_tray_app(speed_test):
    """
    Use Qt to create a tray application
    :param speed_test: speed test object
    :return: None
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("Internet Speed Test")
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(r'icon.png'), w, speed_test)
    tray_icon.show()
    sys.exit(app.exec_())


@click.command()
@click.argument('period', type=int, default=30)
@click.argument('path', type=click.Path(exists=True))
def main(period_in_minutes, path):
    """
    Entry point of the application
    :param period_in_minutes: Period (in minutes) between speed measurements
    :param path: Fully qualified path (folder) for the log files
    :return: None
    """
    #Initiate the peridic test object
    speed_test = periodictest.SpeedTest(path, period_in_minutes)

    start_tray_app(speed_test)

if __name__ == '__main__':

    main()
