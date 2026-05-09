# https://gymnasium.farama.org/environments/classic_control/mountain_car/
# The goal is to reach the flag placed on top of the right hill as quickly as possible, as such the agent is penalised with a reward of -1 for each timestep.
# ACTION SPACE: 0: Accelerate to the left  1: Don’t accelerate  2: Accelerate to the right
# STATE SPACE: SPEED : POSITION
import gymnasium as gym
import numpy as np

env = gym.make("MountainCar-v0")

num_bins = np.array([20, 20])
num_actions = env.action_space.n

q_table = np.zeros((*num_bins, num_actions))


state, info = env.reset()

# main
if __name__ == "__main__":
    for time_stamp in range(10000):
        action = 2

        next_state, reward, terminated, truncated, info = env.step(action)

        if time_stamp % 100 == 0:
            print(f"Time stamp: {time_stamp}")
            print("state:", state)
            print("action:", action)
            print("next_state:", next_state)
            print("reward:", reward)
            print("q-values:", q_table[discrete_state], "\n")

        state = next_state

        if terminated or truncated:
            state, info = env.reset()

    env.close()
