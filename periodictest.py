from utils import *
import click
import threading
import speedtest
import os.path
from datetime import datetime


class SpeedTest:
    """
    Periodic Internet Speed test saved in Log File
    """
    pause = False

    def __init__(self, path, period):
        self.speed_test = speedtest.Speedtest()
        self.logger = create_rotating_log(os.path.join(path, "speedlog.txt"))
        self.__run_test__()     #Run test once
        threading.Timer(period * 60, self.__run_test__).start() #and keep repeating!

    def pause(self):
        """
        Pause executing periodic tests
        :return: None
        """
        pause = True

    def resume(self):
        """
        resume executing periodic tests
        :return: None
        """
        pause = False

    def __run_test__(self):
        """
        Save upload/download speed, ping and test server in log file
        :return: None
        """

        if SpeedTest.pause:
            return

        best_server = self.speed_test.get_best_server()

        self.logger.info("{!s}, {!s},{!s},{!s},{!s}".format(   datetime.now(),
                                                               convert_unit(self.speed_test.download(), SIZE_UNIT.MB),
                                                               convert_unit(self.speed_test.upload(), SIZE_UNIT.MB),
                                                               best_server['latency'],
                                                               best_server['url']))



@click.command()
@click.argument('period', type=int, default=30)
@click.argument('path', type=click.Path(exists=True))
def periodic_test_command(period, path):

    speed_test = SpeedTest(path, period)

if __name__ == '__main__':
    periodic_test_command()