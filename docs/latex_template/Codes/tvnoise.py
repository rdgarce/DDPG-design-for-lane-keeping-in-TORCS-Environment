class TVNoise:

    def __init__(self, mu = [MU_1,MU_2,MU_3], std = [STD_1,STD_2,STD_3]):
        
        self.mu = mu
        self.std = std
        self.time_step1 = 50000
        self.time_step2 = 150000
        self.time_step3 = 300000
        self.countr = -1

    def __call__(self):

        self.countr += 1

        if self.countr < self.time_step1:
            return self.mu[0] + self.std[0] * normal(size = self.mu[0].shape)
        
        elif self.countr >= self.time_step1 and self.countr < self.time_step2:
            
            mu = (self.mu[0] - self.mu[1])/(self.time_step1 - self.time_step2) 
                    * self.countr + (self.time_step1*self.mu[1] - self.time_step2
                    * self.mu[0])/(self.time_step1 - self.time_step2)
            std = (self.std[0] - self.std[1])/(self.time_step1 - self.time_step2) 
                    * self.countr + (self.time_step1*self.std[1] - self.time_step2
                    * self.std[0])/(self.time_step1 - self.time_step2)
            
            return mu + std * normal(size = mu.shape)
        
        elif self.countr >= self.time_step2 and self.countr < self.time_step3:
            
            mu = (self.mu[1] - self.mu[2])/(self.time_step2 - self.time_step3) 
                    * self.countr + (self.time_step2*self.mu[2] - self.time_step3
                    * self.mu[1])/(self.time_step2 - self.time_step3)
            std = (self.std[1] - self.std[2])/(self.time_step2 - self.time_step3) 
                    * self.countr + (self.time_step2*self.std[2] - self.time_step3
                    * self.std[1])/(self.time_step2 - self.time_step3)
            
            return mu + std * normal(size = mu.shape)
        
        else:
           return zeros_like(self.mu[0])