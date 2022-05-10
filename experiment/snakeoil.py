#!/usr/bin/python
# snakeoil.py
# Chris X Edwards <snakeoil@xed.ch>
# Snake Oil is a Python library for interfacing with a TORCS
# race car simulator which has been patched with the server
# extentions used in the Simulated Car Racing competitions.
# http://scr.geccocompetitions.com/
#
# To use it, you must import it and create a "drive()" function.
# This will take care of option handling and server connecting, etc.
# To see how to write your own client do something like this which is
# a complete working client:
# /-----------------------------------------------\
# |#!/usr/bin/python                              |
# |import snakeoil                                |
# |if __name__ == "__main__":                     |
# |    C= snakeoil.Client()                       |
# |    for step in xrange(C.maxSteps,0,-1):       |
# |        C.get_servers_input()                  |
# |        snakeoil.drive_example(C)              |
# |        C.respond_to_server()                  |
# |    C.shutdown()                               |
# \-----------------------------------------------/
# This should then be a full featured client. The next step is to
# replace 'snakeoil.drive_example()' with your own. There is a
# dictionary which holds various option values (see `default_options`
# variable for all the details) but you probably only need a few
# things from it. Mainly the `trackname` and `stage` are important
# when developing a strategic bot. 
#
# This dictionary also contains a ServerState object
# (key=S) and a DriverAction object (key=R for response). This allows
# you to get at all the information sent by the server and to easily
# formulate your reply. These objects contain a member dictionary "d"
# (for data dictionary) which contain key value pairs based on the
# server's syntax. Therefore, you can read the following:
#    angle, curLapTime, damage, distFromStart, distRaced, focus,
#    fuel, gear, lastLapTime, opponents, racePos, rpm,
#    speedX, speedY, speedZ, track, trackPos, wheelSpinVel, z
# The syntax specifically would be something like:
#    X= o[S.d['tracPos']]
# And you can set the following:
#    accel, brake, clutch, gear, steer, focus, meta 
# The syntax is:  
#     o[R.d['steer']]= X
# Note that it is 'steer' and not 'steering' as described in the manual!
# All values should be sensible for their type, including lists being lists.
# See the SCR manual or http://xed.ch/help/torcs.html for details.
#
# If you just run the snakeoil.py base library itself it will implement a
# serviceable client with a demonstration drive function that is
# sufficient for getting around most tracks.
# Try `snakeoil.py --help` to get started.
import os
import socket
import sys
import getopt
import pickle
PI= 3.14159265359

PORT = 3001
GLOBAL_PATH = os.getcwd()
MODELS_PATH = os.path.join( GLOBAL_PATH, 'models' )

# Initialize help messages
ophelp=  'Options:\n'
ophelp+= ' --host, -H <host>    TORCS server host. [localhost]\n'
ophelp+= ' --port, -p <port>    TORCS port. [3001]\n'
ophelp+= ' --id, -i <id>        ID for server. [SCR]\n'
ophelp+= ' --steps, -m <#>      Maximum simulation steps. 1 sec ~ 50 steps. [100000]\n'
ophelp+= ' --episodes, -e <#>   Maximum learning episodes. [1]\n'
ophelp+= ' --track, -t <track>  Your name for this track. Used for learning. [unknown]\n'
ophelp+= ' --stage, -s <#>      0=warm up, 1=qualifying, 2=race, 3=unknown. [3]\n'
ophelp+= ' --debug, -d          Output full telemetry.\n'
ophelp+= ' --help, -h           Show this help.\n'
ophelp+= ' --version, -v        Show current version.'
usage= 'Usage: {} [ophelp [optargs]] \n'.format(sys.argv[0])
usage= usage + ophelp
version= "20130505-2"

class Client():
    def __init__(self, Host = None, Port = None, Sid = None, Episodes = None, Steps = None, 
                                                Trackname = None, Stage = None, Debug = None):
        # If you don't like the option defaults,  change them here.
        self.host = 'localhost'
        self.port = 3001
        self.sid = 'SCR'
        self.maxEpisodes = 1
        self.trackname = 'unknown'
        self.stage = 3
        self.debug = False
        self.maxSteps = 100000  # 50steps/second
        if Host: self.host = Host
        if Port: self.port = Port
        if Sid: self.sid = Sid
        if Episodes: self.maxEpisodes = Episodes
        if Steps: self.maxSteps = Steps
        if Trackname: self.trackname = Trackname
        if Stage: self.stage = Stage
        if Debug: self.debug = Debug
        self.S= ServerState()
        self.R= DriverAction()
        self.setup_connection()

    def setup_connection(self):
        # == Set Up UDP Socket ==
        try:
            self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print('Error: Could not create socket...')
            sys.exit(-1)
        # == Initialize Connection To Server ==
        self.so.settimeout(1)
        while True:
            #vettore degli angoli dei 19 rangefinders come riportati nel paper"
            a= "-45 -19 -12 -7 -4 -2.5 -1.7 -1 -0.5 0 0.5 1 1.7 2.5 4 7 12 19 45"
            initmsg='{}(init {})'.format(self.sid, a)

            try:
                self.so.sendto(bytes(initmsg, "utf8"), (self.host, self.port))
            except socket.error:
                sys.exit(-1)
            sockdata = bytes(str(), "utf8")
            try:
                sockdata,addr= self.so.recvfrom(1024)
            except socket.error:
                print("Waiting for server............")
            if bytes('***identified***','utf8') in sockdata:
                print("Client connected..............")
                break

    def get_servers_input(self):
        '''Server's input is stored in a ServerState object'''
        if not self.so: return
        sockdata = bytes()
        while True:
            try:
                # Receive server data 
                sockdata,addr= self.so.recvfrom(1024)
            except socket.error:
                print("Waiting for data..............")
            if bytes('***identified***', 'utf8') in sockdata:
                print("Client connected..............")
                continue
            elif bytes('***shutdown***', 'utf8') in sockdata:
                print("Server has stopped the race. You were in {} place.".format(self.S.d['racePos'])) 
                self.shutdown()
                return
            elif bytes('***restart***', 'utf8') in sockdata:
                # What do I do here?
                print("Server has restarted the race.")
                # I haven't actually caught the server doing this.
                self.shutdown()
                return
            elif not sockdata: # Empty?
                continue       # Try again.
            else:
                self.S.parse_server_str(sockdata.decode("utf-8"))
                if self.debug: print(self.S)
                break # Can now return from this function.

    def respond_to_server(self):
        if not self.so: return
        if self.debug: print(self.R)
        try:
            self.so.sendto(bytes(repr(self.R), 'utf8'), (self.host, self.port))
        except socket.error as emsg:
            print("Error sending to server: {} Message {}%s".format(emsg[1], str(emsg[0])))
            sys.exit(-1)

    def shutdown(self):
        if not self.so: return
        print("Race terminated or {} steps elapsed. Shutting down.".format(self.maxSteps))
        self.so.close()
        self.so= None
        #sys.exit() # No need for this really.

class ServerState():
    'What the server is reporting right now.'
    def __init__(self):
        self.servstr= str()
        self.d= dict()

    def parse_server_str(self, server_string):
        'parse the server string'
        self.servstr= server_string.strip()[:-1]
        sslisted = self.servstr.strip().lstrip('(').rstrip(')').split(')(')
        for i in sslisted:
            w= i.split(' ')
            self.d[w[0]]= destringify(w[1:])

    def __repr__(self):
        out= str()
        for k in sorted(self.d):
            strout= str(self.d[k])
            if type(self.d[k]) is list:
                strlist= [str(i) for i in self.d[k]]
                strout= ', '.join(strlist)
            out+= "{}: {}\n".format(k, strout)
        return out

class DriverAction():
    '''What the driver is intending to do (i.e. send to the server).
    Composes something like this for the server:
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus 0)(meta 0) or
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus -90 -45 0 45 90)(meta 0)'''
    def __init__(self):
       self.actionstr= str()
       # "d" is for data dictionary.
       self.d= { 'accel':0.2,
                   'brake':0,
                  'clutch':0,
                    'gear':1,
                   'steer':0,
                   'focus':[-90,-45,0,45,90],
                    'meta':0 
                    }

    def __repr__(self):
        out= str()
        for k in self.d:
            out+= '('+k+' '
            v= self.d[k]
            if not type(v) == list:
                out+= '{:.3f}'.format(v)
            else:
                out+= ' '.join([str(x) for x in v])
            out+= ')'
        return out
        return out+'\n'

# == Misc Utility Functions
def destringify(s):
    '''makes a string into a value or a list of strings into a list of
    values (if possible)'''
    if not s: return s
    if type(s) is str:
        try:
            return float(s)
        except ValueError:
            print("Could not find a value in {}".format(s))
            return s
    elif type(s) is list:
        if len(s) < 2:
            return destringify(s[0])
        else:
            return [destringify(i) for i in s]

def clip(v,lo,hi):
    if v<lo: return lo
    elif v>hi: return hi
    else: return v

def drive_example(c):
    '''This is only an example. It will get around the track but the
    correct thing to do is write your own `drive()` function.'''
    S= c.S.d
    R= c.R.d  # As python passes values by reference, modifications in R affect Client.R.
    target_speed=100

    # Damage Control
    target_speed-= S['damage'] * .05
    if target_speed < 25: target_speed= 25

    # Steer To Corner
    R['steer']= S['angle']*10 / PI
    # Steer To Center
    R['steer']-= S['trackPos']*.10
    R['steer']= clip(R['steer'],-1,1)

    # Throttle Control
    if S['speedX'] < target_speed - (R['steer']*50):
        R['accel']+= .01
    else:
        R['accel']-= .01
    if S['speedX']<10:
       R['accel']+= 1/(S['speedX']+.1)

    # Traction Control System
    if ((S['wheelSpinVel'][2]+S['wheelSpinVel'][3]) -
       (S['wheelSpinVel'][0]+S['wheelSpinVel'][1]) > 5):
       R['accel']-= .2
    R['accel']= clip(R['accel'],0,1)

    # Automatic Transmission
    R['gear']=1
    if S['speedX']>50:
        R['gear']=2
    if S['speedX']>80:
        R['gear']=3
    if S['speedX']>110:
        R['gear']=4
    if S['speedX']>140:
        R['gear']=5
    if S['speedX']>170:
        R['gear']=6
        
    return

# ================ MAIN ================
if __name__ == "__main__":
    
    
    file = open(os.path.join(MODELS_PATH,"saved_actions.pkl"), "rb")
    actions = pickle.load(file)
    file.close()
    C = Client(Host='localhost', Port=PORT)

    for elem in actions:
        C.get_servers_input()
        
        
        C.R.d['accel'] = elem[0][0]
        C.R.d['brake'] = elem[0][1]
        C.R.d['steer'] = elem[0][2]
    
    # Trasmissione Automatica
        C.R.d['gear']=1
        if C.S.d['speedX']>50:
            C.R.d['gear']=2
        if C.S.d['speedX']>80:
            C.R.d['gear']=3
        if C.S.d['speedX']>110:
            C.R.d['gear']=4
        if C.S.d['speedX']>140:
            C.R.d['gear']=5
        if C.S.d['speedX']>170:
            C.R.d['gear']=6

        C.respond_to_server()
    C.shutdown()
