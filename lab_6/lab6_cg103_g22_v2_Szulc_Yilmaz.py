# https://gymnasium.farama.org/environments/classic_control/mountain_car/
# The goal is to reach the flag placed on top of the right hill as quickly as possible, as such the agent is penalised with a reward of -1 for each timestep.
# ACTION SPACE: 0: Accelerate to the left  1: Don’t accelerate  2: Accelerate to the right
# STATE SPACE: SPEED : POSITION
# terminated: position >= 0.5 # reached a hill
# truncated: hit 200 step limit
# alpha: learning rate gamma: caring about future rewardsfrom utility import Timer
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from utility import Timer

env = gym.make("MountainCar-v0")

num_bins = np.array([20, 20])
state_low = env.observation_space.low
state_high = env.observation_space.high
num_actions = env.action_space.n


### PARAMETERS
use_alpha_decay = True
alpha_start = 0.1
alpha = alpha_start
alpha_decay = 0.99995
alpha_min = 0.001

gamma = 0.95

epsilon = 1.0
epsilon_decay = 0.9995
epsilon_min = 0.01

episodes = 40000


naming_convention = (
    f"_alpha{alpha_start}"
    f"_useAlphaDecay{use_alpha_decay}"
    f"_alphaDecay{alpha_decay}"
    f"_alphaMin{alpha_min}"
    f"_gamma{gamma}"
    f"_epsilon{epsilon}"
    f"_decay{epsilon_decay}"
    f"_episodes{episodes}"
)

q_table_filename = f"q_table{naming_convention}.npy"

try:
    q_table = np.load(q_table_filename)
    print("Q-table loaded from file.")
except FileNotFoundError:
    q_table = np.zeros((*num_bins, num_actions))


rewards_per_episode = []
steps_per_episode = []
successes_per_episode = []
alphas_per_episode = []


def discretize_state(state):
    ratios = (state - state_low) / (state_high - state_low)
    ratios = np.clip(ratios, 0, 1)
    bins = (ratios * (num_bins - 1)).astype(int)
    return tuple(bins)


def choose_action(discrete_state):
    if np.random.random() < epsilon:
        return env.action_space.sample()
    return np.argmax(q_table[discrete_state])


def update_q_table(discrete_state, action, reward, next_discrete_state, terminated):
    old_value = q_table[discrete_state][action]

    if terminated:
        target = reward
    else:
        next_max = np.max(q_table[next_discrete_state])
        target = reward + gamma * next_max

    new_value = old_value + alpha * (target - old_value)
    q_table[discrete_state][action] = new_value


def moving_average(values, window_size):
    return np.convolve(values, np.ones(window_size) / window_size, mode="valid")


max_reward = -float("inf")  # interchangable with min_step_count

if __name__ == "__main__":
    timer = Timer("MountainCar Q-Learning")
    timer()

    for episode in range(episodes):
        state, info = env.reset()
        discrete_state = discretize_state(state)

        total_reward = 0
        steps = 0

        terminated = False
        truncated = False

        while not terminated and not truncated:
            action = choose_action(discrete_state)

            next_state, reward, terminated, truncated, info = env.step(action)
            next_discrete_state = discretize_state(next_state)

            update_q_table(discrete_state, action, reward, next_discrete_state, terminated)

            total_reward += reward
            steps += 1

            state = next_state
            discrete_state = next_discrete_state

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        if use_alpha_decay:
            alpha = max(alpha_min, alpha * alpha_decay)

        if total_reward > max_reward:
            max_reward = total_reward
            print(f"New max reward: {max_reward} at episode {episode}")

        rewards_per_episode.append(total_reward)
        steps_per_episode.append(steps)
        successes_per_episode.append(1 if terminated else 0)
        alphas_per_episode.append(alpha)

        if episode % 3000 == 0:
            print("episode:", episode, "total_reward:", total_reward, "steps:", steps, "epsilon:", round(epsilon, 4), "alpha:", round(alpha, 4))

    np.save(q_table_filename, q_table)

    timer()  # stop timer and print elapsed time

    window_size = 100

    plt.plot(moving_average(rewards_per_episode, window_size))
    plt.xlabel("Episode")
    plt.ylabel("Average reward")
    plt.title("MountainCar Q-Learning Training Progress")
    plt.savefig(f"training_rewards{naming_convention}.png")
    plt.show()

    plt.plot(moving_average(successes_per_episode, window_size))
    plt.xlabel("Episode")
    plt.ylabel("Success rate")
    plt.title("MountainCar Training Success Rate")
    plt.savefig(f"success_rate{naming_convention}.png")
    plt.show()

    plt.plot(alphas_per_episode)
    plt.xlabel("Episode")
    plt.ylabel("Alpha")
    plt.title("Learning Rate Decay" if use_alpha_decay else "Learning Rate")
    plt.savefig(f"alpha_decay{naming_convention}.png")
    plt.show()

    env.close()

    print(f"lowest time: {max_reward}")
