import gymnasium as gym

env = gym.make("CarRacing-v2", render_mode="human")
observation, info = env.reset()
r_max, r_min = 0, 0
for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    r_max = r_max if (r_max > reward)  else reward 
    r_min = r_min if (r_min < reward)  else reward
    print ("Observation: ", observation)
    print ("Reward: ", reward)
    print ("Terminated: ", terminated)
    print ("Truncated: ", truncated)
    print ("Info: ", info)           
    if terminated or truncated:
        observation, info = env.reset()        
env.close() 
print("Mínimo: ", r_min, " Máximo: ", r_max)