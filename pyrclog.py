#!/usr/bin/pyhon
import socket
from datetime import datetime
import os
import sys
import time

#connection info
server = 'irchost'
port = 6667
channels = ['#test1', '#test2', '#test3']

#formatting stuff
now = datetime.now()
logbase = '/some/log/dir/for/base'

def filename():
    return str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.' + 'log'

def timeformat():
    return str(datetime.now().hour) + ':' + str(datetime.now().minute)

def startup(): #Checks to see if the dirs you're trying to log to are accessible, if not exit script
    try:
        for channel in channels:
            channel = channel.split('#')[1]
            os.listdir(logbase + channel)
    except OSError:
        return False
        sys.exit()
    return True
startup()

ircsoc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
ircsoc.connect(( server, port))
time.sleep(1)
ircsoc.send('NICK pyrclog\r\n' )
time.sleep(1)
ircsoc.send('USER pyrclog pyrclog pyrclog :Python IRClogger Maintained by Derek McKnight\r\n' )
time.sleep(1)


while startup():
    for channel in channels:
        ircsoc.send('JOIN %s\r\n' % channel)
    ircmsg = ircsoc.recv(2048)
    ircmsg=ircmsg.strip('\n\r')
    if ircmsg.find('PRIVMSG') != -1:
        nick=ircmsg.split('!')[0][1:]
        channel=ircmsg.split(' PRIVMSG' )[-1].split(' :')[0]
        new_channel=channel.split('#')[1]
        msg=ircmsg.split('PRIVMSG')[-1].split(' :')[1]
        with open(logbase + new_channel + '/' + filename() , 'a') as logfile:
            logfile.write('[%s]%s <%s>: %s\n' % (timeformat(),channel,nick,msg))
        #print '[%s]%s <%s>: %s' % (hrse,channel, nick, msg)



    if ircmsg.find( 'PING' ) != -1:
        ircsoc.send('PONG ' + ircmsg.split()[1] + '\r\n')
