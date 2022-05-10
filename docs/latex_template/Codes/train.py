def train(self):

    if self.replayBuffer.mem_cntr < self.batch_size:
        return
    states, actions, new_states, rewards, dones = self.replayBuffer.sample_buffer(
                                                                self.batch_size)
    rewards = rewards.reshape(-1,1)
    dones = dones.reshape(-1,1)

    states = tf.convert_to_tensor(states, dtype=tf.float32)
    actions = tf.convert_to_tensor(actions, dtype=tf.float32)
    new_states = tf.convert_to_tensor(new_states, dtype=tf.float32)
    rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)


    with tf.GradientTape() as tape:
        target_actions = self.target_actor.model(new_states, training = True)
        new_critic_value = self.target_critic.model([new_states, target_actions], 
                                                    training = True)
        critic_value = self.critic.model([states, actions], training = True)

        target = rewards + self.dc_fact * new_critic_value * (1-dones)
        critic_loss = tf.keras.losses.MSE(target, critic_value)

        critic_network_gradient = tape.gradient(critic_loss, 
                                            self.critic.model.trainable_variables)
        self.critic.model.optimizer.apply_gradients(zip(critic_network_gradient, 
                                            self.critic.model.trainable_variables))

    with tf.GradientTape() as tape:
        new_policy_actions = self.actor.model(states, training = True)
        critic_value = -self.critic.model([states, new_policy_actions], 
                                            training = True)
        actor_loss = tf.math.reduce_mean(critic_value)

        actor_network_gradient = tape.gradient(actor_loss, 
                                            self.actor.model.trainable_variables)
        self.actor.model.optimizer.apply_gradients(zip(actor_network_gradient, 
                                            self.actor.model.trainable_variables))

        self._update_target() #Soft copy dei networks