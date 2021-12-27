# DDPG design for lane keeping in TORCS Environment
My absolutely first repository on github!

## Structure
The work is structured as follows.
```
├── Code #The main folder of all the code of the experiment
    ├── DDPG #Folder containing all the classes and functions for implementing the algo
        ├── OU.py #Implementation of the Ornstein–Uhlenbeck noise with the stochastic brake mod
        ├── GN.py #Implementation of the Gaussian Noise
        ├── TVNoise.py #Implementation of the Time Variant Noise
        ├── conditioning.py #Implementation of a utility function for interacting with TORCS env
        ├── networks.py #Implementation of Actor and Critic networks
        ├── replayBuffer.py #Implementation of the experience replay required by DDPG
        ├── reward.py #Implementation of the env. reward function
        
```
