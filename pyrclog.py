 1 #!/usr/bin/pyhon
  2 import socket
  3 from datetime import datetime
  4 import os
  5 import sys
  6 import time
  7
  8 #connection info
  9 server = 'irchost'
 10 port = 6667
 11 channels = ['#test1', '#test2', '#test3']
 12 
 13 #formatting stuff
 14 now = datetime.now()
 15 logbase = '/some/random/dir/youwant/as/logbase'
 16
 17 def filename():
 18     return str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.' + 'log'
 19
 20 def timeformat():
 21     return str(datetime.now().hour) + ':' + str(datetime.now().minute)
 22
 23 def startup(): #Checks to see if the dirs you're trying to log to are accessible, if not exit script
 24     try:
 25         for channel in channels:
 26             channel = channel.split('#')[1]
 27             os.listdir(logbase + channel)
 28     except OSError:
 29         return False
 30         sys.exit()
 31     return True
 32 startup()
 33
 34 ircsoc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
 35 ircsoc.connect(( server, port))
 36 time.sleep(1)
 37 ircsoc.send('NICK pyrclogbot\r\n' )
 38 time.sleep(1)
 39 ircsoc.send('USER pyrclog pyrclog pyrclog :Python IRClogger Maintained by Derek McKnight\r\n' )
 40 time.sleep(1)
 41
 42
 43 while startup():
 44     for channel in channels:
 45         ircsoc.send('JOIN %s\r\n' % channel)
 46     ircmsg = ircsoc.recv(2048)
 47     ircmsg=ircmsg.strip('\n\r')
 48     if ircmsg.find('PRIVMSG') != -1:
 49         nick=ircmsg.split('!')[0][1:]
 50         channel=ircmsg.split(' PRIVMSG' )[-1].split(' :')[0]
 51         new_channel=channel.split('#')[1]
 52         msg=ircmsg.split('PRIVMSG')[-1].split(' :')[1]
 53         with open(logbase + new_channel + '/' + filename() , 'a') as logfile:
 54             logfile.write('[%s]%s <%s>: %s\n' % (timeformat(),channel,nick,msg))
 55         #print '[%s]%s <%s>: %s' % (hrse,channel, nick, msg)
 56
 57
 58
 59     if ircmsg.find( 'PING' ) != -1:
 60         ircsoc.send('PONG ' + ircmsg.split()[1] + '\r\n')
