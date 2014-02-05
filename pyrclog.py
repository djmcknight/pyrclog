#!/usr/bin/pyhon
import socket
from datetime import datetime
 
server = 'hubbard.freenode.net'
port = 6665 #default
channels = ['#pybot', '#pybot1', '#pybot3'] #channels you want to join (Please Change)
botnick = 'pyrclog' #nickname for bot
now = datetime.now()
hrse = str(now.hour) + ':' + str(now.second)

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
        print '[%s]%s <%s>: %s' % (hrse,channel, nick, msg)
    if ircmsg.find( 'PING' ) != -1:
        ircsoc.send('PONG' + ircmsg.split() [1] + '\r\n')
