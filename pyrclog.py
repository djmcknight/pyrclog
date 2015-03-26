#!/usr/bin/python
import socket
from datetime import datetime
import os
import sys
import time

#pid file info
pid = str(os.getpid())
pidfile = '/tmp/pyrclog.pid'
if os.path.isfile(pidfile):
    print '%s already exsists, exiting' % pidfile
    sys.exit()
else:
    with open(pidfile,'w') as pid_file:
        pid_file.write(pid)

#connection info
server = 'irchost'
port = 6667
channels = ['#test1', '#test2', '#test3']
nick = 'pyrclogger'


#formatting stuff
now = datetime.now()
logbase = '/elsnfs/irclogs/'

#Function for returning datetime month-day-year.log for the filename of the logfile - this creates the Logrotation becuase
#when it's a new day - it will automatially write to this new file.
def filename():
#    return str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.' + 'txt'
    dtn  = datetime.now()
    nfn = dtn.strftime('%Y-%m-%d.txt')
    return nfn
#Time format for when we receive an alert in [hour:minute] format
def timeformat():
    tf = datetime.now()
    toutput = tf.strftime('%H:%M')
    return toutput
    #return str(datetime.now().hour) + ':' + str(datetime.now().minute)

#You need to have the logbase + dir of the channel you're going to be watching for. So - if you need to add a new
#channel to watching in 'channels' - you need to mkdir new channel in the logbase dir.
def startup():
    try:
        for channel in channels:
            channel = channel.split('#')[1]
            os.listdir(logbase + channel) #Tries to list dir
    except OSError: #If it can't use the OSError it rasies
        return False #and return false
        sys.exit() #then exit
    return True #IF it works - return true.
startup() #calls Startup to check the channels log dir

#opens the socket
ircsoc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#connnects to irc server asiged to 'server', and 'port'
ircsoc.connect(( server, port))
#sleep for one second
time.sleep(1)
ircsoc.send('NICK %s\r\n' % nick )
time.sleep(1) #More Sleep
ircsoc.send('USER DerekM DerekM DerekM :Python IRClogger\r\n' )
time.sleep(1) #bot is sleepy

def main():
    chan_num = 0
    while startup():
        ircmsg = ircsoc.recv(8192)
        ircmsg=ircmsg.strip('\r\n')
        #responsed to the IRC Serv PING messages.
        if ircmsg.find( 'PING' ) != -1:
            ircsoc.send('PONG ' + ircmsg.split()[1] + '\r\n')
        #joins the channels, but only once. This is a test to see if try and stop the excess flood
        #messages durkin was seeing on his bot
        while chan_num != len(channels):
            for channel in channels:
                ircsoc.send('JOIN %s\r\n' % channel) #Joins the channles in 'channels'
                chan_num += 1
                time.sleep(30)
        if ircmsg.find('PRIVMSG') != -1: #If Statement to look for messages from users in IRC channels
            nick=ircmsg.split('!')[0][1:]                         #Message formatting
            channel=ircmsg.split(' PRIVMSG' )[-1].split(' :')[0]  #More message formatting
            if channel.startswith(' #'): #Makes it so people how private message the bot don't crash it.
                new_channel=channel.split('#')[1]                 #Even more message formatting
                msg=ircmsg.split('PRIVMSG')[-1].split(' :')[1]    #Lots mor message formatting
                #The 'with open' opens the new file with the current date, as seen in the filename function - this creates the
                #log rotation ability because this will only write to files of the current date - when it becomes a new day
                #you get a new file. This also makes sure that you don't have to explicitly close the file after each call.
                with open(logbase + new_channel + '/' + filename() , 'a') as logfile:
                    logfile.write('%s[%s] <%s>: %s\n' % (channel,timeformat(),nick,msg))

#The "Python Boilerplate - this calls the main() function above ONLY if you're executing the script, not importing it into another python script
if __name__ == '__main__':
    main()
