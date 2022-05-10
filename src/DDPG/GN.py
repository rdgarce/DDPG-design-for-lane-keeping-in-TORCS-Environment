from numpy.random import normal, random
from numpy import zeros, array

#media e std del rumore gaussiano aggiunto nel 90% dei casi
MU_1 = array([[0.60 , -0.10 , 0.0]], dtype='float32')
STD_1 = array([[0.10 , 0.05 , 0.0]], dtype='float32')

#media e std del rumore gaussiano aggiunto nel 10% dei casi
#valori necessari nel caso dello stochastic brake
#https://yanpanlau.github.io/2016/10/11/Torcs-Keras.html
MU_2 = array([[0.60 , 0.20 , 0.0]], dtype='float32')
STD_2 = array([[0.10 , 0.10 , 0.0]], dtype='float32')

class GN:

    def __init__(self, mu = [MU_1,MU_2], std = [STD_1,STD_2], decay_time = 300000):
        
        self.mu = mu
        self.std = std
        self.decay_time = decay_time
        self.epsilon = 1.0

    def __call__(self):
        
        if self.decay_time > 0:
            self.epsilon -= 1/self.decay_time
        
        if random() > self.epsilon:
            return zeros(self.mu[0].shape)
        
        if random() <= 0.1:
            return self.mu[1] + self.std[1] * normal(size = self.mu[1].shape)
        else:
           return self.mu[0] + self.std[0] * normal(size = self.mu[0].shape)