import time
import subprocess
import argparse
import logging
from daemon import runner

from mailing import send_email


class DaemonApp(object):
    """Daemon App."""

    def __init__(self, name=None, wait=60, attempts=4, interval=15,
                 log='/var/log/watchdog_daemon.log'):
        """Initialize Daemon."""
        self.stdin_path = log
        self.stdout_path = log
        self.stderr_path = log
        self.pidfile_path = '/tmp/daemon.pid'
        self.pidfile_timeout = 1
        self.name = name
        self.wait = int(wait)  # seconds
        self.attempts = attempts
        self.interval = interval  # seconds
        self.log = log

    def set_logger(self):
        logger = logging.getLogger('watchdog_logger')
        handler = logging.FileHandler(self.log)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger

    def resurrect_service(self, logger):
        attempt = 0
        while attempt <= self.attempts and self.is_inactive():
            attempt += 1
            logger.error('Service "%s" is down. Trying to start. '
                         'Attempt nr %s' % (self.name, str(attempt)))

            subprocess.Popen(["service", self.name, "start"],
                             stdout=subprocess.PIPE)

            time.sleep(self.interval)

        if self.is_inactive():
            logger.error('Failed to resurrect service "%s"' % self.name)
            send_email("Service '%s' failed to start after %s ." %
                       (self.name, str(attempt)))
        else:
            logger.info('Ressurection mission for service "%s" '
                        'was successfull after %s attempt(s).' %
                        (self.name, str(attempt)))
            send_email("Service '%s' successfuly started after %s "
                       "attempt(s)" % (self.name, str(attempt)))

    def is_inactive(self):
        output = subprocess.Popen(["service", self.name, "status"],
                                  stdout=subprocess.PIPE).communicate()[0]
        for line in output.split('\n'):
            if '(dead)' in line:
                return True

    def run(self):
        """Main Daemon Code."""
        logger = self.set_logger()

        while True:
            if self.is_inactive():
                send_email("Service '%s' is DOWN." % self.name)
                self.resurrect_service(logger)
            time.sleep(self.wait)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',
                        choices=('start', 'stop'))
    parser.add_argument("--name",
                        help="Process name", type=str)
    parser.add_argument("--wait",
                        help="Check every X seconds",
                        type=int, default=5)
    parser.add_argument("--attempts",
                        help="Number of attempts to start service",
                        type=int, default=4)
    parser.add_argument("--interval",
                        help="Time interval between tries to start service",
                        type=int, default=15)
    parser.add_argument("--log",
                        help="Log file path", type=str,
                        default='/var/log/watchdog_daemon.log')
    args = parser.parse_args()

    if args.action is 'start':
        if args.name is None:
            parser.error("Name of service is required")
        else:
            service_check = subprocess.Popen(
                ["service", args.name, "status"],
                stdout=subprocess.PIPE).communicate()[0]
            for line in service_check.split('\n'):
                if 'not-found' in line:
                    parser.error("There is no service with such name "
                                 "as '%s' loaded" % args.name)

    app = DaemonApp(name=args.name, wait=args.wait, attempts=args.attempts,
                    interval=args.interval, log=args.log)
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()
