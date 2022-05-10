'''
Checkpoint directory per il salvataggio dei modelli Actor e Critic
'''
import os
CHKPT_DIR = 'DDPG/models'
if not os.path.isdir(os.path.join(os.getcwd(), CHKPT_DIR)):
    os.mkdir(os.path.join(os.getcwd(), CHKPT_DIR))

'''
Dimensione del replayBuffer
'''
MEM_SIZE = 100000

'''
Dimensione del batch di prelievo dalla memoria e di aggiornamento network
'''
BATCH_SIZE = 64

'''
Numero di step prima dei quali l'agente non effettuerà training. 
Serve a riempire l'experience replay buffer di un numero sufficiente di transizioni prima di iniziare a prelevarle.
'''
DELAY_STEPS = 1024

'''
Numero di step che devono intercorrere tra ogni training dell'agente.
Qualsiasi sia il valore impostato si tenga a mente che il rapporto tra step dell'environment e aggiornamento delle reti rimane fisso ad 1
'''
UPDATE_EVERY = 64

'''
Il dizionario contentente le azioni desiderate e le rispettive funzioni di attivazione all'uscita dell'Actor network
e il (min,max) dell'azione.
Per modificare le azioni che si vuole includere nello schema di controllo agire solo su ACTIONS_ACTFUNC_DICT
'''
ACTIONS_ACTFUNC_DICT = {'accel': ['sigmoid',(0,1)], 'brake': ['sigmoid',(0,1)], 'steer': ['tanh',(-1,1)]}
ACTIONS_SPACE = [*ACTIONS_ACTFUNC_DICT.keys()]
ACTIONS_SPACE_DIM = len(ACTIONS_SPACE)
ACTIONS_MIN = [key_elem[1][1][0] for key_elem in ACTIONS_ACTFUNC_DICT.items()]
ACTIONS_MAX = [key_elem[1][1][1] for key_elem in ACTIONS_ACTFUNC_DICT.items()]

'''
Dizionario dei parametri di stato, la chiave indica il nome del parametro è una lista che contiene rispettivamente la dimensione
di quello stato e il valore rispetto al quale normalizzarlo prima di inserirlo nella rete neurale. 
Per aggiungere parametri allo spazio di stato basta aggiungere il loro identificativo, la dimensione e il valore con cui normalizzarli in questo dict
'''
PI= 3.14159265359
STATE_SPACE_DICT = {'angle': [1,PI], 'speedX': [1,300.],'speedY': [1,300.],'speedZ': [1,300.],'track': [19,200.],'trackPos': [1,1.]}
STATE_SPACE = [*STATE_SPACE_DICT.keys()]
STATE_SPACE_DIM = sum([elem[0] for elem in STATE_SPACE_DICT.values()])
STATE_SPACE_NORM = [v[1] for v in STATE_SPACE_DICT.values() for i in range(v[0])]

'''
Discount factor Q-Learning
'''
DC_FACT = 0.99

'''
Smooth factor per la soft copy tra modelli e modelli target
'''
SM_FACT = 0.001

'''
Learning rate del Critic Network e dell'Actor Network
'''
CLR = 0.001
ALR = 0.0001

'''
Numero di neuroni del primo e del secondo livello del Critic Network
'''
CRITIC_1_DIM = 300
CRITIC_2_DIM = 400

'''
Numero di neuroni del primo e del secondo livello dell'Actor Network
'''
ACTOR_1_DIM = 300
ACTOR_2_DIM = 400

'''
Funzione di noise da applicare all'actor per la exploration degli stati
'''
from DDPG.OU import *
NOISE = OU



'''-----------------------------------------------------------------------------------------------
Struttura completa dello stato

States = {
    'angle': 0.0, #Interesse
    'curLapTime': -0.962, 
    'damage': 0.0, 
    'distFromStart': 6201.46, 
    'distRaced': 0.0, 
    'fuel': 94.0, 
    'gear': 0.0, 
    'lastLapTime': 0.0, 
    'opponents': [200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0], 
    'racePos': 1.0, 
    'rpm': 1100.33, 
    'speedX': 0.0, #Interesse
    'speedY': 0.0, #Interesse
    'speedZ': -0.000605693, #Interesse
    'track': [4.00001, 4.14111, 4.61881, 5.65686, 8.00001, 11.6952, 15.4548, 23.0351, 45.8949, 200.0, 91.7896, 46.0701, 30.9096, 23.3904, 16.0, 11.3137, 9.2376, 8.2822, 7.99999], #Interesse
    'trackPos': 0.333332, #Interesse
    'wheelSpinVel': [0.0, 0.0, 0.0, 0.0], 
    'z': 0.345263, 
    'focus': [-1.0, -1.0, -1.0, -1.0, -1.0]
    }

Struttura completa delle azioni

Actions = {
    'accel': 1, #Interesse
    'brake': 0, #Interesse
    'clutch': 0, 
    'gear': 1, 
    'steer': -0.017622710219914715, #Interesse
    'focus': [-90, -45, 0, 45, 90], 
    'meta': 0
    }

'''