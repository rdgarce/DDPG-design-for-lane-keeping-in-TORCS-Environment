class Critic

  def __init__(self, state_space_dim = STATE_SPACE_DIM, 
                actions_space_dim = ACTIONS_SPACE_DIM, 
                clr = CLR, critic_1_dim = CRITIC_1_DIM, 
                critic_2_dim = CRITIC_2_DIM, name = 'Critic', 
                chkpt_dir = CHKPT_DIR):

    self.model_name = name
    self.checkpoint_dir = chkpt_dir
    self.clr = clr
    self.state_space_dim = state_space_dim
    self.actions_space_dim = actions_space_dim
    self.model = self.create_critic(critic_1_dim, critic_2_dim, clr)

  def __call__(self, state, action):
    return self.model.predict([state,action])

  def create_critic(self, critic_1_dim, critic_2_dim, clr):
    
    S = Input(shape = [self.state_space_dim])
    w1 = Dense(critic_1_dim, activation = 'relu')(S)
    h1 = Dense(critic_2_dim, activation = 'linear')(w1)
    
    A = Input(shape = [self.actions_space_dim], name = 'action2')
    a1 = Dense(critic_2_dim, activation ='linear')(A)
    
    h2 = Add()([h1,a1])
    h3 = Dense(critic_2_dim, activation = 'relu')(h2)
    V = Dense(1, activation = 'linear')(h3)
    
    model = Model(inputs = [S,A], outputs = V)
    model.compile(optimizer = Adam(learning_rate = clr))
    return model

  def save_model(self, count):
    if not os.path.isdir(os.path.join(os.getcwd(), self.checkpoint_dir, str(count))):
      os.mkdir(os.path.join(os.getcwd(), self.checkpoint_dir, str(count)))
    self.model.save_weights(os.path.join(os.getcwd(), self.checkpoint_dir, 
                            str(count), self.model_name + '_ddpg.h5'))

  def load_model(self, count):
    self.model.load_weights(os.path.join(os.getcwd(), self.checkpoint_dir, 
                            str(count), self.model_name + '_ddpg.h5'))