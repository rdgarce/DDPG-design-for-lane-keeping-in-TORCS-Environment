class Actor:

  def __init__(self, state_space_dim = STATE_SPACE_DIM, 
                actions_actfunc_dict = ACTIONS_ACTFUNC_DICT, 
                alr = ALR, actor_1_dim = ACTOR_1_DIM, 
                actor_2_dim = ACTOR_2_DIM, name = 'Actor', 
                chkpt_dir = CHKPT_DIR):

    self.model_name = name
    self.checkpoint_dir = chkpt_dir
    self.alr = alr
    self.state_space_dim = state_space_dim
    self.actions_actfunc_dict = actions_actfunc_dict
    self.model = self.create_actor(actor_1_dim, actor_2_dim, alr)
    

  def __call__(self, state):
    return self.model.predict(state)

  def create_actor(self, actor_1_dim, actor_2_dim, alr):

    S = Input(shape=[self.state_space_dim])
    h0 = Dense(actor_1_dim, activation='relu')(S)
    h1 = Dense(actor_2_dim, activation='relu')(h0)

    lista = []
    for k,v in self.actions_actfunc_dict.items():
      lista.append(Dense(1,activation = v[0])(h1))

    V = Concatenate()(lista)

    model = Model(inputs = S, outputs = V)
    model.compile(optimizer = Adam(learning_rate = alr))

    return model

  def save_model(self, count):
    if not os.path.isdir(os.path.join(os.getcwd(), self.checkpoint_dir, str(count))):
      os.mkdir(os.path.join(os.getcwd(), self.checkpoint_dir, str(count)))
    self.model.save_weights(os.path.join(os.getcwd(), self.checkpoint_dir, 
                            str(count), self.model_name + '_ddpg.h5'))

  def load_model(self, count):
    self.model.load_weights(os.path.join(os.getcwd(), self.checkpoint_dir, 
                            str(count), self.model_name + '_ddpg.h5'))