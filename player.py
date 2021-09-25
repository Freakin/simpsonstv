import os
import sys
import random
import signal
from time import sleep
from omxplayer.player import OMXPlayer

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')

videos = []
bus = ["org.mpris.MediaPlayer2.omxplayer2", "org.mpris.MediaPlayer2.omxplayer3"]
plrs = [None, None]

def interrupt(signal, frame):
    print "Killing OMXPlayer..."
    for plr in plrs:
        if plr != None:
            plr.stop()
    sys.exit(0)


def getVideos():
    global videos
    videos = []
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
            videos.append(os.path.join(directory, file))

def playVideos():
    global videos
    global plrs
    if len(videos) == 0:
        getVideos()
        sleep(5)
        return
    random.shuffle(videos)
    for i, video in enumerate(videos):
        ix = i % 2
        plrs[ix] = OMXPlayer(video, args=['--layer', str((ix+1)%2)], dbus_name=bus[ix])
        print '{0} Duration: {1}'.format(video, plrs[ix].duration())
        sleep(plrs[ix].duration() - 3.50)

signal.signal(signal.SIGINT, interrupt)

while (True):
    playVideos()
