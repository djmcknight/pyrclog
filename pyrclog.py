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

#Function for returning datetime month-day-year.log for the filename of the logfile - this creates the Logrotation becuase
#when it's a new day - it will automatially write to this new file.
def filename():
    return str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.' + 'log'

#Time format for when we receive an alert in [hour:minute] format
def timeformat():
    return str(datetime.now().hour) + ':' + str(datetime.now().minute)

#You need to have the logbase + dir of the channel you're going to be watching for. So - if you need to add a new 
#channel to watching in 'channels' - you need to mkdir new channel in the logbase dir.
def startup(): 
    try:
        for channel in channels:
            channel = channel.split('#')[1]
            os.listdir(logbase + channel)
    except OSError:
        return False
        sys.exit()
    return True
startup() #calls Startup to check the channels log dir

#opens the socket
ircsoc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#connnects to irc server asiged to 'server', and 'port'
ircsoc.connect(( server, port))
#sleep for one second
time.sleep(1)
ircsoc.send('NICK pyrclog\r\n' )
time.sleep(1)
ircsoc.send('USER pyrclog pyrclog pyrclog :Python IRClogger Maintained by Derek McKnight\r\n' )
time.sleep(1)

#Chceks to see if startup function is true. This is an infinite loop
while startup():
    for channel in channels:
        ircsoc.send('JOIN %s\r\n' % channel) #Joins the channels
    ircmsg = ircsoc.recv(2048)
    ircmsg=ircmsg.strip('\n\r')
    if ircmsg.find('PRIVMSG') != -1: #If Statement to look for messages from users in IRC channels
        nick=ircmsg.split('!')[0][1:]                        #Message formatting
        channel=ircmsg.split(' PRIVMSG' )[-1].split(' :')[0] #More message formatting
        new_channel=channel.split('#')[1]                    #Even more message formatting
        msg=ircmsg.split('PRIVMSG')[-1].split(' :')[1]       #Lots mor message formatting
        #The 'with open' opens the new file with the current date, as seen in the filename function - this creates the
        #log rotation ability because this will only write to files of the current date - when it becomes a new day
        #you get a new file. This also makes sure that you don't have to explicitly close the file after each call.
        with open(logbase + new_channel + '/' + filename() , 'a') as logfile:
            logfile.write('[%s]%s <%s>: %s\n' % (timeformat(),channel,nick,msg))
    #Responds to the IRC PING responses. If you don't aswer the PING with PONG and the numeral in the PING request
    #you will eventually be timed out of the server
    if ircmsg.find( 'PING' ) != -1:
        ircsoc.send('PONG ' + ircmsg.split()[1] + '\r\n')
