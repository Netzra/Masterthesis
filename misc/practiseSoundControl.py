#____________________________________________________________________
# UNTESTED
#____________________________________________________________________

#imports
import time
from os import listdir, getcwd
from pythonosc import udp_client
from random import randint

# TODO centrilize
# hardcoded variables
practise = True
client = udp_client.SimpleUDPClient("127.0.0.1", 10003)
soundfileList = []
unplayed = [int(x) for x in range(soundfileList.__len__())]

# TODO
#  1. generalize, possible function
#  2. make it more elegant
# saving all .wav entries of signals into a list
for entry in listdir("signals"):
    if ".wav" in entry:
        soundfileList.append(entry)

# TODO make it more elegant
# change the played soundfile every 60 seconds
while(practise):
    time.sleep(60)
    if unplayed.__len__() == 0:
        unplayed = [int(x) for x in range(soundfileList.__len__())]
    else:
        temp = unplayed[randint(0, unplayed.__len__())]
        client.send_message("/pyBinSimFile", "signals/"+soundfileList[temp])
        unplayed.pop(temp)

# DEBUG
# print(getcwd())
# print(listdir())
# print([type(x) for x in soundfileList])

