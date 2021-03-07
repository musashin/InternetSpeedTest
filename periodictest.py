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
        self.period = period

    def start(self):
        #TODO
        #threading.Timer(self.period * 2, self.run_test).start() #and keep repeating!
        ticker = threading.Event()
        while not ticker.wait(self.period * 60):
            self.run_test()

    def get_period_in_min(self):
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

        print("Starting Test")

        best_server = self.speed_test.get_best_server()

        self.logger.info("{!s}, {!s},{!s},{!s},{!s}".format(   datetime.now(),
                                                               convert_unit(self.speed_test.download(), SIZE_UNIT.MB),
                                                               convert_unit(self.speed_test.upload(), SIZE_UNIT.MB),
                                                               best_server['latency'],
                                                               best_server['url']))

        print("Completing Test")


@click.command()
@click.argument('period', type=int, default=30)
@click.argument('path', type=click.Path(exists=True))
def periodic_test_command(period, path):

    speed_test = SpeedTest(path, period)
    speed_test.start()


if __name__ == '__main__':
    periodic_test_command()