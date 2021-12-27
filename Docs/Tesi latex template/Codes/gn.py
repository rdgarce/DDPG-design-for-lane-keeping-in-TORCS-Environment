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