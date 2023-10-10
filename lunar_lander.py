import gymnasium as gym
import time

env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()

for _ in range(100):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    print ("Reward: ", reward, "steering: ", action)
    time.sleep(.5)

    if terminated or truncated:
        observation, info = env.reset()
env.close() 