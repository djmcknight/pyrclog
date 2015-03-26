#!/usr/bin/python

import os
import time
from datetime import datetime
import tarfile

def timeformat():
    tf = datetime.now()
    toutput = tf.strftime('%Y-%m-%d')
    return toutput

#walk the directory specific, making 3 lists. root, dir, and rfiles.
for root, dirs, rfiles in os.walk('/home/pyrclog/logs/'):
    #iterate over each dir in the list.
    for dir in dirs:
        #take all the files from the dir, and put them in the list
        dirList = os.listdir(root + '/' + dir)
        #open the tarfile object
        tar = tarfile.open(root + '/' + dir + '/' + dir + '.' + timeformat() + '.tar.gz', "w:gz")
        #loop over the list of files in the dir
        for logfiles in dirList:
            #make sure i'm ONLY looking at log files, so anything that doesn't end in .txt get ignored.
            if logfiles.endswith('.txt'):
                #comparing the epoch time from right now, and then divide by 86400 to get the number of days. Minus that by the modify time
                #of the file and you get the number of days since it's been modified. If that is > than 30 - it is slected to be added to the tar.
                #I then remove the file from the Dir
                if (int(time.time() / 86400) - int(os.stat(root + '/' + dir + '/' + logfiles).st_mtime / 86400)) > 30:
                    tar.add(root + '/' + dir + '/' + logfiles)
                    os.remove(root + '/' + dir + '/' + logfiles)
                #if the file is less than 30days old - pass the "continue" to move onto the next item in list.
                elif (int(time.time() / 86400) - int(os.stat(root + '/' + dir + '/' + logfiles).st_mtime / 86400)) <  30:
                    continue
                #since this is python 2.6.6, and the tarfile module doesn't work with the "with tarfile.open" i have to call the close after i'm done.
                else:
                    tar.close()
