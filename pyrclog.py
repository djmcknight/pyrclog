#!/usr/bin/python
import socket
from datetime import datetime
import os
import sys
import time


pid = str(os.getpid())
pidfile = '/tmp/pyrclog.pid'
if os.path.isfile(pidfile):
    print '%s already exsists, exiting' % pidfile
    sys.exit()
else:
    with open(pidfile,'w') as pid_file:
        pid_file.write(pid)


server = 'irchost'
port = 6667
channels = ['#test1', '#test2', '#test3']
nick = 'pyrclog'




logbase = '/home/pyrclog/logs/'


def filename():
    return str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.' + 'txt'


def timeformat():
    tf = datetime.now()
    toutput = tf.strftime('%H:%M')
    return toutput
    


def startup():
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
ircsoc.send('NICK %s\r\n' % nick )
time.sleep(1) 
ircsoc.send('USER pyrclog pyrclog pyrclog :Python IRClogger Maintained by Derek McKnight\r\n' )
time.sleep(1) 

chan_num = 0
main():
    while startup():
        ircmsg = ircsoc.recv(8192)
        ircmsg=ircmsg.strip('\r\n')
   
        if ircmsg.find( 'PING' ) != -1:
            ircsoc.send('PONG ' + ircmsg.split()[1] + '\r\n')

        while chan_num != len(channels):
            for channel in channels:
                ircsoc.send('JOIN %s\r\n' % channel) 
                chan_num += 1
        if ircmsg.find('PRIVMSG') != -1: 
            nick=ircmsg.split('!')[0][1:]                         
            channel=ircmsg.split(' PRIVMSG' )[-1].split(' :')[0]  
            if channel.startswith(' #'): 
                new_channel=channel.split('#')[1]                 
                msg=ircmsg.split('PRIVMSG')[-1].split(' :')[1]    
            
                with open(logbase + new_channel + '/' + filename() , 'a') as logfile:
                    logfile.write('[%s]%s <%s>: %s\n' % (timeformat(),channel,nick,msg))

if __name__ == '__main__':
    main()
