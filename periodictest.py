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
        """
        Constructor
        :param path: fully qualified path to log files
        :param period: period of text in
        """
        self.speed_test = speedtest.Speedtest()
        self.logger = create_rotating_log(os.path.join(path, "speedlog.txt"))
        self.period = period

    def start(self):
        """
        Periodically call the run test method
        :return:
        """

        ticker = threading.Event()
        while not ticker.wait(self.period * 60):
            self.run_test()

    def get_period_in_min(self):
        """
        Accessor for test period
        :return: test period in minutes
        """
        return self.period

    def pause_collection(self):
        """
        Pause executing periodic tests
        :return: None
        """
        SpeedTest.pause = True

    def resume_collection(self):
        """
        resume executing periodic tests
        :return: None
        """
        SpeedTest.pause = False

    def run_test(self):
        """
        Save upload/download speed, ping and test server in log file
        :return: None
        """

        if SpeedTest.pause:
            return

        print("-- Start Test --")
        best_server = self.speed_test.get_best_server()

        self.logger.info("{!s}, {!s},{!s},{!s},{!s}".format(   datetime.now(),
                                                               convert_unit(self.speed_test.download(), SIZE_UNIT.MB),
                                                               convert_unit(self.speed_test.upload(), SIZE_UNIT.MB),
                                                               best_server['latency'],
                                                               best_server['url']))
        print("-- Stop Test --")

@click.command()
@click.argument('period', type=int, default=30)
@click.argument('path', type=click.Path(exists=True))
def periodic_test_command(period, path):

    speed_test = SpeedTest(path, period)
    speed_test.start()


if __name__ == '__main__':
    periodic_test_command()