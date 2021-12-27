def _update_target(self, sm_fact = None):

    if sm_fact is None:
        sm_fact = self.sm_fact

    target_critic_weights = self.target_critic.model.weights
    new_target_critic_weights = []

    for i, elem in enumerate(self.critic.model.weights):
        new_target_critic_weights.append( sm_fact * elem + (1 - sm_fact) * 
                                        target_critic_weights[i] )

    self.target_critic.model.set_weights(new_target_critic_weights)


    target_actor_weights = self.target_actor.model.weights
    new_actor_critic_weights = []

    for i, elem in enumerate(self.actor.model.weights):
        new_actor_critic_weights.append( sm_fact * elem + (1 - sm_fact) * 
                                        target_actor_weights[i] )

    self.target_actor.model.set_weights(new_actor_critic_weights)