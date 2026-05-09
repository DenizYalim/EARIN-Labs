# https://gymnasium.farama.org/environments/classic_control/mountain_car/
# The goal is to reach the flag placed on top of the right hill as quickly as possible, as such the agent is penalised with a reward of -1 for each timestep.
# ACTION SPACE: 0: Accelerate to the left  1: Don’t accelerate  2: Accelerate to the right
# STATE SPACE: SPEED : POSITION
# terminated: position >= 0.5 # reached a hill
# truncated: hit 200 step limit
# alpha: learning rate gamma: caring about future rewards


import gymnasium as gym
import numpy as np

env = gym.make("MountainCar-v0")

num_bins = np.array([20, 20])
state_low = env.observation_space.low
state_high = env.observation_space.high
num_actions = env.action_space.n

q_table = np.zeros((*num_bins, num_actions))

alpha = 0.1
gamma = 0.99


def discretize_state(state):  #
    ratios = (state - state_low) / (state_high - state_low)
    ratios = np.clip(ratios, 0, 1)
    bins = (ratios * (num_bins - 1)).astype(int)
    return tuple(bins)


def update_q_table(discrete_state, action, reward, next_discrete_state):
    old_value = q_table[discrete_state][action]
    next_max = np.max(q_table[next_discrete_state])
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    q_table[discrete_state][action] = new_value


state, info = env.reset()
discrete_state = discretize_state(state)

total_reward = 0
steps = 0

terminated = False
truncated = False

time_stamp = 0


while not terminated and not truncated:  # one episode
    time_stamp += 1

    action = env.action_space.sample()

    next_state, reward, terminated, truncated, info = env.step(action)
    next_discrete_state = discretize_state(next_state)

    update_q_table(discrete_state, action, reward, next_discrete_state)

    total_reward += reward
    steps += 1

    if time_stamp % 10 == 0:
        print(f"Time stamp: {time_stamp}")
        print("state:", np.round(state, 4))
        print("discrete_state:", discrete_state)
        print("action:", action)
        print("next_state:", np.round(next_state, 4))
        print("next_discrete_state:", next_discrete_state)
        print("reward:", reward)
        print("q-values:", np.round(q_table[discrete_state], 4), "\n")

    state = next_state
    discrete_state = next_discrete_state

print("total_reward:", total_reward)
print("steps:", steps)
print("terminated:", terminated)
print("truncated:", truncated)

np.save("q_table.npy", q_table)  # SAVE Q-TABLE TO FILE

env.close()
