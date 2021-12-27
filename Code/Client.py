from DDPG.agent import *
from snakeoil import *
import pickle
import shutil

PORT = 3001
training_mode = True
load_model = True

save_actions = False
saved_actions = list()

Steps = 6000
Episodes = 1000

training_data = {
    "episode_count" : -1, 
    "episodic_reward_list": list(), 
    "avg_reward_list": list()
    }

agent = Agent(training=training_mode)

if load_model:
    load_status = agent.load_agent()
    
    if load_status == 0:
        try:
            file = open(os.path.join(os.getcwd(),CHKPT_DIR,"training_data.pkl"), "rb")
            training_data = pickle.load(file)
            file.close()
            training_data["episodic_reward_list"]
            training_data["avg_reward_list"]
        except:
            print("File training_data.pkl non trovato o corrotto -> Il modello è stato caricato \
                    ma le statistiche sono azzerate ")
            
            training_data = {
                "episode_count" : -1, 
                "episodic_reward_list": list(), 
                "avg_reward_list": list()
                }
    elif load_status == -1:
        print("Nessun modello trovato: Si parte da zero!")
    else:
        print("Il modello scelto è corrotto e non può essere caricato: Si parte da zero!")
else:
    shutil.rmtree(os.path.join(os.getcwd(), CHKPT_DIR), ignore_errors= True)
    os.mkdir(os.path.join(os.getcwd(), CHKPT_DIR))


input(f"Si parte dall'episodio {training_data['episode_count']+1}: Clicca un tasto per partire")
C = Client(Host = 'localhost', Steps = Steps, Port = PORT)

C.get_servers_input()

for episode in range(training_data['episode_count']+1, Episodes+training_data['episode_count']+1):
    
    
    done = False
    step = 0
    episodic_reward = 0
    low_velocity_count = 0

    while not done and step < Steps:
        current_state = conditionDict(C.S.d, STATE_SPACE, STATE_SPACE_NORM)
        #print(current_state)
        action = agent.act(current_state)
        #print("Azione dell'agent: ", action[0][0], action[0][1], action[0][2])
        
        
        C.R.d['accel'] = action[0][0]
        C.R.d['brake'] = action[0][1]
        C.R.d['steer'] = action[0][2]

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

        if save_actions:
            saved_actions.append(action)
        
        C.respond_to_server()
        C.get_servers_input()
        new_state = conditionDict(C.S.d, STATE_SPACE, STATE_SPACE_NORM)
        #print(C.S.d['trackPos'])
        reward_t = reward(C.S.d['speedX'],C.S.d['angle'],C.S.d['trackPos'])
        episodic_reward += reward_t
        #print("Reward: ",str(reward_t),'\n')

        
        if C.S.d['speedX'] < 5:
            low_velocity_count += 1
        else:
            low_velocity_count = 0

        #controllo sull'uscita fuori pista, sull'angolo di direzione dell'auto e sulla velocità < 5km/h per 3 secondi di fila
        if reward_t == -200 or cos(C.S.d['angle']) < 0 or low_velocity_count >= 150:
            done = True
            
        agent.store_transition(current_state,action,new_state,reward_t,done)
        
        agent.train()
        
        step += 1
    
    C.R.d['meta'] = True
    C.respond_to_server()
    C.shutdown()
    
    training_data["episodic_reward_list"].append(episodic_reward)
    avg_reward = np.mean(training_data["episodic_reward_list"])
    training_data["episode_count"] = episode
    training_data["avg_reward_list"].append(avg_reward)

    if training_mode:
        agent.save_agent(episode)
    
        file = open(os.path.join(os.getcwd(),CHKPT_DIR,"training_data.pkl"), "wb")
        pickle.dump(training_data, file)
        file.close()

    if save_actions:
        file = open(os.path.join(os.getcwd(),CHKPT_DIR,"saved_actions.pkl"), "wb")
        pickle.dump(saved_actions, file)
        file.close()

    print("Episodio {}: Ricompensa: {}, Media ricompense: {}".format(episode, episodic_reward, avg_reward))

    C = Client(Host = 'localhost', Steps = Steps, Port = PORT)
    C.get_servers_input()
    
C.shutdown()   
print("Tutti gli episodi sono terminati: termino esecuzione")