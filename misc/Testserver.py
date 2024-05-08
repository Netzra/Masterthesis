from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
import slab
import os

#Todo
# 1. centrilize
# 2. update with unreal info
ip = "127.0.0.1"
serverPort = 10004
unrealclientPort = 8001
pyBinSimClientPortds = 10000
pyBinSimClientPortlate = 10003
# print(os.getcwd())
conditions = [entry for entry in os.listdir("signals") if ".wav" in entry]
global artificialdistance
artificialdistance = 1.0

#update with unreal information
x = -700.0
unrealAdress = "/ctrlUnreal/sourcePosition"
value = [0, 200.0, x, 120.0, 0.0, 0.0, -90.0]

global trialsequence
trialsequence = slab.Trialsequence(conditions)

dispatcher = Dispatcher()
# global unrealClient
# Unrealclient = SimpleUDPClient(ip, UnrealclientPort)
global Clientdirect
Clientdirect = SimpleUDPClient(ip, pyBinSimClientPortds)
global Clientlate
Clientlate = SimpleUDPClient(ip, pyBinSimClientPortlate)

def saving_perceived(address = str, *args):
    global artificialdistance
    if address.__contains__("input"):
        if args[0] == 1:
            artificialdistance += 1
            Clientlate.send_message("/pyBinSim_late_Filter", [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, artificialdistance, 0.0, 0.0, 0.0, 0.0, 0.0])
        elif args[0] == 2:
            artificialdistance -= 1
            Clientlate.send_message("/pyBinSim_late_Filter", [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, artificialdistance, 0.0, 0.0, 0.0, 0.0, 0.0])
    # if trialsequence.this_n < trialsequence.n_trials - 1:
        # print(trialsequence.__next__())
    # else:
    #     # unrealClient.send_message(unrealAdress, value)
    #     print("finished")
def reroute_information(*args):
    temp = args[1:]
    Clientdirect.send_message("/pyBinSim_ds_Filter", temp)
    pass

dispatcher.map("/saving/*", saving_perceived)
dispatcher.map("/reroute/*", reroute_information)
server = ThreadingOSCUDPServer((ip, serverPort), dispatcher)
server.serve_forever()  # Blocks forever
