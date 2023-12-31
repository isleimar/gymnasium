import gymnasium as gym
import cv2
import imutils

env = gym.make("CarRacing-v2", render_mode="human")


seed = 42
env.action_space.seed(seed)
observation, info = env.reset(seed=seed)


player_coord = 47,65
stage = 96,96
player_dist = {    
    'top': 0,
    'left': 0,
    'right': 0,
    'top_left': 0,
    'top_right': 0    
}

def run():


    


    action = env.action_space.sample()
    action[0] = 0.0  # steering        
    action[1] = 0.15  # speed / gas
    action[2] = 0.0  # brake
    for _ in range(1000):        

        observation, reward, terminated, truncated, info = env.step(action)
        image_cp = observation.copy()
        if terminated or truncated:
            observation, info = env.reset(seed=seed)        
        dist = get_dist(observation)

        left = dist['top_left']
        right = dist['top_right']

        dis_t = left + right

        if dis_t > 0:
            action[0] = (right - left) / dis_t
        
        action[2] = (65 - dist['top']) / 650

        show_player(observation, dist)
    env.close() 

def show_player(observation, dist):   
    x,y = player_coord
    line_color = (255,0,0)
    image_cp = observation.copy()
    cv2.cvtColor(image_cp, cv2.COLOR_RGB2BGR, image_cp)
    

    cv2.line(image_cp, (x,y), (x,y - dist['top']),line_color)
    cv2.line(image_cp, (x,y), (x - dist['left'], y),line_color)
    cv2.line(image_cp, (x,y), (x + dist['right'], y),line_color)
    cv2.line(image_cp, (x,y), (x - dist['top_left'], y - dist['top_left']),line_color)
    cv2.line(image_cp, (x,y), (x + dist['top_right'], y - dist['top_right']),line_color)

    cv2.circle(image_cp, (x,y),1,(0,0,255))


    
    image_cp = imutils.resize(image_cp, 500)
    cv2.imshow("Player", image_cp)
    cv2.waitKey(1)
    pass

def get_dist(observation):
    player_dist = {    
        'top': 0,
        'left': 0,
        'right': 0,
        'top_left': 0,
        'top_right': 0    
    }
    x,y = player_coord

    color = observation[y][x]
    i = 0
    while (y+i > 0) and (color[1] < 200):                
        color = observation[y +i][x]
        i -= 1
    player_dist['top'] = abs(i)

    color = observation[y][x]
    i = 0
    while (x+i > 0) and (color[1] < 200):                
        color = observation[y][x +i]
        i -= 1
    player_dist['left'] = abs(i)

    color = observation[y][x]
    i = 0
    while (x +i < stage[0]) and (color[1] < 200):                
        color = observation[y][x +i]
        i += 1
    player_dist['right'] = abs(i)

    color = observation[y][x]
    i = 0
    while (x+i > 0) and (y+i > 0) and (color[1] < 200):
        color = observation[y +i][x +i]
        i -= 1       
    player_dist['top_left'] = abs(i)

    color = observation[y][x]
    i = 0
    while (x+ abs(i) < stage[0]) and (y+i > 0) and (color[1] < 200):
        color = observation[y +i][x + abs(i)]
        i -= 1
    player_dist['top_right'] = abs(i)
    return player_dist


run()




