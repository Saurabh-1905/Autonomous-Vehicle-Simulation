from stable_baselines3 import PPO
import numpy as np

try:
    model = PPO.load("models/rl_self_driving")
except:
    model = None

def rl_control(state):
    if model is None:
        return 0.0

    action, _ = model.predict(state)
    return float(action[0])