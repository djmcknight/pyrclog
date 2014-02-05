#!/usr/bin/pyhon
import socket
from datetime import datetime
import os
import sys
 
server = 'hubbard.freenode.net'
port = 6665 
channels = ['#pybot', '#pybot1', '#pybot3'] 
botnick = 'pyrclog' 
now = datetime.now()
hrse = str(now.hour) + ':' + str(now.second)
file_name = str(now.month) + "-" + str(now.day) + '-' + str(now.year) + '.' + 'log'
logbase = '/home/Derek/Projects/pyrclog/logs/'

def startup():
    for channel in channels:
        channel = channel.split('#')[1]
    if os.path.isdir(logbase + channel):
        continue
    else:
        sys.exit('Please create a valid directory for the channel you are trying to join')

ircsoc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
ircsoc.connect(( server, port))
ircsoc.send('NICK pyrclog\r\n' )
ircsoc.send('USER pyrclog pyrclog pyrclog :Python IRClogger\r\n' )
for channel in channels:
    ircsoc.send('JOIN %s\r\n' % channel)


while True:
    ircmsg = ircsoc.recv(2048)
    ircmsg=ircmsg.strip('\n\r')
    if ircmsg.find('PRIVMSG') != -1: 
        nick=ircmsg.split('!')[0][1:]
        channel=ircmsg.split(' PRIVMSG' )[-1].split(' :')[0]
        msg=ircmsg.split('PRIVMSG')[-1].split(' :')[1]
        with open(logcation, 'a') as logfile:
            logfile.write('[%s]%s <%s>: %s\n' % (hrse,channel,nick,msg))
        #print '[%s]%s <%s>: %s' % (hrse,channel, nick, msg)
    if ircmsg.find( 'PING' ) != -1:
        ircsoc.send('PONG' + ircmsg.split() [1] + '\r\n')
