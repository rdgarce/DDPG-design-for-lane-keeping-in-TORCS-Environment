# π DDPG design for lane keeping in TORCS Environment
My absolutely first repository on github!

This repository contains my bachelor's degree thesis project: Designing a DDPG algorithm for approaching the lane keeping problem in the autonomous ground vehicle driving.

## Pre-requisites
- Python 3 with Keras and Tensorflow
- TORCS game with SCR patch

## Structure
The work is structured as follows.
```
βββ src                         #The main folder of all the code
β   βββ DDPG                    #Folder containing all the classes and functions for implementing the algo.
β   |   βββ noise               #Foler containing the noise classes used fro the DDPG
|   |   |   βββ OU.py           #Implementation of the OrnsteinβUhlenbeck noise with the stochastic brake mod
|   |   |   βββ GN.py           #Implementation of the Gaussian Noise
|   |   |   βββ TVNoise.py      #Implementation of the Time Variant Noise
β   β   βββ conditioning.py     #Implementation of a utility function for interacting with TORCS env.
β   β   βββ networks.py         #Implementation of Actor and Critic networks
β   β   βββ replayBuffer.py     #Implementation of the experience replay required by DDPG
β   β   βββ reward.py           #Implementation of the three env. reward functions
β   β   βββ config.py           #Config file you need to look before running any experiment with DDPG
β   β   βββ agent.py            #Implementation of the agent class and all of its functions
β   βββ launch.py               #Main python script to launch the experiment
β   βββ snakeoil.py             #Implementation of the client interface for the interaction with TORCS game
βββ experiment                  #A copy of the src folder but with the final driver model in it for testing purpose
β   βββ DDPG                    #Folder containing all the classes and functions for implementing the algo.
β   |   βββ noise               #Foler containing the noise classes used fro the DDPG
|   |   |   βββ OU.py           #Implementation of the OrnsteinβUhlenbeck noise with the stochastic brake mod
|   |   |   βββ GN.py           #Implementation of the Gaussian Noise
|   |   |   βββ TVNoise.py      #Implementation of the Time Variant Noise
|   βββ models                  #Folder containing different version of the driver. 
β   β   βββ conditioning.py     #Implementation of a utility function for interacting with TORCS env.
β   β   βββ networks.py         #Implementation of Actor and Critic networks
β   β   βββ replayBuffer.py     #Implementation of the experience replay required by DDPG
β   β   βββ reward.py           #Implementation of the three env. reward functions
β   β   βββ config.py           #Config file you need to look before running any experiment with DDPG
β   β   βββ agent.py            #Implementation of the agent class and all of its functions
β   βββ launch.py               #Main python script to launch the experiment
β   βββ snakeoil.py             #Implementation of the client interface for the interaction with TORCS game
βββ docs                        #Folder containing documents
    βββ Tesi.pdf                #Thesis on DDPG design for lane keeping in TORCS Environment. Italian language
    βββ latex_template          #Latex template folder of my thesis project
    
```
