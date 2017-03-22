Watchdog Daemon
====

Daemon to watch out for service. If service is down, daemon attempts to start service 
and sends notifications about service status.

Instruction:
---
```
Create virtualenv and activate (Python2.7)
pip install -r requirements.txt
```
Help:
```
python watchdog.py -h for help

Mandatory argument:
  --name NAME          Process name

Optional arguments: 
  --wait WAIT          Check every X seconds
  --attempts ATTEMPTS  Number of attempts to start service
  --interval INTERVAL  Time interval between tries to start service
  --log LOG            Log file path
```
Run example:

```
python watchdog.py start --name=httpd --wait=60 --attempts=4 --interval==15 --log=/var/log/watchdog_daemon.log
```
Stop:
```
python watchdog.py stop
```

Requirements
-----

To run it may be required to make proper chown on /tmp/daemon.pid.
 
Depending on setup it may be required to append to called commands 'sudo', make user sudoer or w/e.

To send emails, configured SMTP server (e.g. Postfix) is required. OS environmental variables 
"MAIL_SENDER" and "MAIL_RECEIVER" are used.