import gymnasium as gym
import numpy as np

Q_TABLE_FILES = [
    "standard_Values.npy",
    "smaller_alpha_no_decay.npy",
    "slower_epsilon_decay.npy",
    "lower_gamma.npy",
    "alpha_decay_on.npy",
]

TEST_EPISODES = 10000
SEED = 42


def ai_bot(velocity, position):
    if velocity < 0:
        return 0
    elif velocity > 0:
        return 2
    else:
        if position < -0.5:
            return 2
        else:
            return 0


def discretize_state(state, state_low, state_high, num_bins):
    ratios = (state - state_low) / (state_high - state_low)
    ratios = np.clip(ratios, 0, 1)
    bins = (ratios * (num_bins - 1)).astype(int)
    return tuple(bins)


def test_q_table(q_table_file):
    env = gym.make("MountainCar-v0")

    q_table = np.load(q_table_file)

    num_bins = np.array(q_table.shape[:2])
    state_low = env.observation_space.low
    state_high = env.observation_space.high

    rewards = []
    steps_list = []
    successes = []

    for episode in range(TEST_EPISODES):
        state, info = env.reset(seed=SEED + episode)
        discrete_state = discretize_state(state, state_low, state_high, num_bins)

        total_reward = 0
        steps = 0

        terminated = False
        truncated = False

        while not terminated and not truncated:
            action = int(np.argmax(q_table[discrete_state]))

            next_state, reward, terminated, truncated, info = env.step(action)
            next_discrete_state = discretize_state(next_state, state_low, state_high, num_bins)

            total_reward += reward
            steps += 1

            state = next_state
            discrete_state = next_discrete_state

        rewards.append(total_reward)
        steps_list.append(steps)
        successes.append(1 if terminated else 0)

    env.close()

    return {
        "name": q_table_file,
        "average_reward": round(np.mean(rewards), 2),
        "average_steps": round(np.mean(steps_list), 2),
        "best_reward": np.max(rewards),
        "worst_reward": np.min(rewards),
        "success_rate": round(np.mean(successes), 4),
    }


def test_ai_bot():
    env = gym.make("MountainCar-v0")

    rewards = []
    steps_list = []
    successes = []

    for episode in range(TEST_EPISODES):
        state, info = env.reset(seed=SEED + episode)

        total_reward = 0
        steps = 0

        terminated = False
        truncated = False

        while not terminated and not truncated:
            position = state[0]
            velocity = state[1]

            action = ai_bot(velocity, position)

            next_state, reward, terminated, truncated, info = env.step(action)

            total_reward += reward
            steps += 1

            state = next_state

        rewards.append(total_reward)
        steps_list.append(steps)
        successes.append(1 if terminated else 0)

    env.close()

    return {
        "name": "manual_ai_bot",
        "average_reward": round(np.mean(rewards), 2),
        "average_steps": round(np.mean(steps_list), 2),
        "best_reward": np.max(rewards),
        "worst_reward": np.min(rewards),
        "success_rate": round(np.mean(successes), 4),
    }


results = []

for q_table_file in Q_TABLE_FILES:
    result = test_q_table(q_table_file)
    results.append(result)

    print("Agent:", result["name"])
    print("Test episodes:", TEST_EPISODES)
    print("Average reward:", result["average_reward"])
    print("Average steps/time:", result["average_steps"])
    print("Best reward:", result["best_reward"])
    print("Worst reward:", result["worst_reward"])
    print("Success rate:", result["success_rate"])
    print("-" * 40)


bot_result = test_ai_bot()
results.append(bot_result)

print("Agent:", bot_result["name"])
print("Test episodes:", TEST_EPISODES)
print("Average reward:", bot_result["average_reward"])
print("Average steps/time:", bot_result["average_steps"])
print("Best reward:", bot_result["best_reward"])
print("Worst reward:", bot_result["worst_reward"])
print("Success rate:", bot_result["success_rate"])
print("-" * 40)


print("\nSUMMARY")
print("Agent, Average reward, Average steps, Best reward, Worst reward, Success rate")

for result in results:
    print(result["name"], result["average_reward"], result["average_steps"], result["best_reward"], result["worst_reward"], result["success_rate"], sep=", ")
