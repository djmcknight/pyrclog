#!/usr/bin/python
import socket
from datetime import datetime
import os
import sys
import time

#Creates the .pid file on the server. If the file exists already - exit the script.
pid = str(os.getpid())
pidfile = '/tmp/pyrclog.pid'
if os.path.isfile(pidfile):
    print '%s already exsists, exiting' % pidfile
    sys.exit()
else: #writing to pid to the file called "pyrclog.pid"
    with open(pidfile,'w') as pid_file:
        pid_file.write(pid)

#connects to your server
server = 'irchost'
port = 6667
channels = ['#test1', '#test2', '#test3'] #list of channels
nick = 'pyrclog' #The 'nickname' on the IRC server (what everyone sees you as



#This is the logbase. This is needed for writing the logs to the files.
logbase = '/home/pyrclog/logs/'

#This creates the file name - and creates the native log rotation. Since it's going to call this every time it tries to write
#When it becomes a new day - it creates a new file (move on this below)
def filename():
    return str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.' + 'txt'

#time formating for when the script writes inside the log file.
def timeformat():
    tf = datetime.now()
    toutput = tf.strftime('%H:%M')
    return toutput
    

#This startup function tries to list the director logbase(as seen above) + channel. So if /home/pyrclog/logs/test1 is not
#a valid directory - the script will exit.
def startup():
    try:
        for channel in channels:
            channel = channel.split('#')[1]
            os.listdir(logbase + channel) 
    except OSError: #excepting the OSError for invalid dir
        return False 
        sys.exit() #exit the script
    return True #Return true if the logbase + channel is a valid directory
startup() 

#Setting up the socet.
ircsoc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#connecting to the socket
ircsoc.connect(( server, port))

time.sleep(1) #sleep 1 second
ircsoc.send('NICK %s\r\n' % nick )
time.sleep(1) #sleep 1 second
ircsoc.send('USER pyrclog pyrclog pyrclog :Python IRClogger Maintained by Derek McKnight\r\n' )
time.sleep(1) #sleep 1 second.

#The "main" loop. This is called if the python script ran - not imported.
def main():
    chan_num = 0
    while startup(): #Checks to see if startup(): is true. This creates an infinite loop.
        ircmsg = ircsoc.recv(8192) #Recieve datat from socket
        ircmsg=ircmsg.strip('\r\n')
        #Below looks for the first inital PING message from the irc server. you HAVE to answer this first before
        #the irc server will accept any commands from you.
        if ircmsg.find( 'PING' ) != -1: 
            ircsoc.send('PONG ' + ircmsg.split()[1] + '\r\n')
        #Joins the channels one at a time
        while chan_num != len(channels):
            for channel in channels:
                ircsoc.send('JOIN %s\r\n' % channel) 
                chan_num += 1
        # Looks for messages in the data you recieved from  the sockets that are from other people.
        if ircmsg.find('PRIVMSG') != -1: 
            nick=ircmsg.split('!')[0][1:]                         
            channel=ircmsg.split(' PRIVMSG' )[-1].split(' :')[0]  
            if channel.startswith(' #'): #This is so if someone PM's the bot - it doesn't crash it.
                new_channel=channel.split('#')[1] #message formatting.            
                msg=ircmsg.split('PRIVMSG')[-1].split(' :')[1]    
                # The with open(file) is so you don't have to specifically close the file every time you write - becuase
                # "with open" does this after it's dones writing to the file.
                with open(logbase + new_channel + '/' + filename() , 'a') as logfile:
                    logfile.write('[%s]%s <%s>: %s\n' % (timeformat(),channel,nick,msg))
                    #The above only writes to a file that's today's take - for example 8-1-2014.txt - So when it's a new day
                    #you get a new file - automatic log rotation.

#The 'python boiler plate'. Makes it so that the main() function only gets called when you run the script from CLI
#and not if the file is impoorted into another python script.
if __name__ == '__main__':
    main()

