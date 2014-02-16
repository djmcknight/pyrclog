#!/usr/bin/python
import os, commands, string, subprocess, sys, smtplib



SERVER = 'localhost'
FROM = 'you@example.com'
TO = ['recepiant@example.com']
SUBJECT = 'The IRC logger is not running'
TEXT = '''The IRC LOGGER is no longer running'''


message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ",".join(TO), SUBJECT, TEXT)
server = smtplib.SMTP(SERVER)



tmpfile = '/tmp/pyrclog.pid'
if os.path.isfile(tmpfile):
    pidfile = open(tmpfile, 'rw')
    pid = pidfile.readlines()
    pidfile.close()


output = commands.getoutput("ps -ef | grep -v grep | grep " + pid[0])

proginfo = string.split(output)

if len(proginfo) > 0:
    if proginfo[8] == 'pyrclog.py':
        sys.exit()
else:
    server.sendmail(FROM, TO, message)
    server.quit()
    sys.exit()
