import gym
import random
#from nbformat import current_nbformat
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =  20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)


    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()
        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning

        while (not done):
            # Epsilon greedy algorithm condition where
            # agent chooses random action
            if (random.uniform(0,1) < EPSILON):
                action = env.action_space.sample()
            # Epsilon greedy algorithm condition where
            # agent chooses optimal policy action
            else:
                # find the optimal action
                prediction = np.array(np.array([Q_table[(obs,i)] for i in range(env.action_space.n)]))
                action =  np.argmax(prediction)
            # get the rewards, state, terminal boolean, and info
            new_obs,reward,done,info = env.step(action)
            episode_reward += reward # update episode reward
            # update the Q_table with values of newly updated state   
            best_next_action = np.argmax([Q_table[(new_obs, i)] for i in range(env.action_space.n)])
            # td_target = reward + DISCOUNT_FACTOR * Q_table[(new_obs, best_next_action)]
            # td_delta = td_target - Q_table[(obs, action)]
            # Q_table[(obs, action)] += LEARNING_RATE * td_delta
            td = (1 - LEARNING_RATE) * Q_table[(obs, action)]
            if(done):
                Q_table[(obs, action)] = td + (LEARNING_RATE * reward)
            else:
                Q_table[(obs, action)] = td + (LEARNING_RATE * (reward + (DISCOUNT_FACTOR * Q_table[(new_obs, best_next_action)])))
            obs = new_obs
        EPSILON = EPSILON * EPSILON_DECAY

        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 

        
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    #### DO NOT MODIFY ######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################