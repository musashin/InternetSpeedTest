import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import version
import periodictest
import click


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, period_in_min):
        super().__init__(parent=None)

        self.setWindowTitle("About Internet Speed Test")

        QBtn = QtWidgets.QDialogButtonBox.Ok

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.close)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Data collected every {!s} minutes by Internet Speed Test Version {!s}".
                                   format(period_in_min,version.__version__))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent, speed_test):

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

        self.setContextMenu(menu)

    def about(self):
        dlg = AboutDialog(self.speed_test.get_period_in_min())
        dlg.exec_()

    def exit(self):
        QtCore.QCoreApplication.exit()

    def pause_data_collection(self):
        self.pause = not self.pause
        self.pauseAction.setText("Resume" if self.pause else "Pause")

        if self.pause:
            self.speed_test.pause()
        else:
            self.speed_test.resume()


@click.command()
@click.argument('period', type=int, default=30)
@click.argument('path', type=click.Path(exists=True))
def main(period, path):

    speed_test = periodictest.SpeedTest(path, period)

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(r'icon.png'), w, speed_test)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
