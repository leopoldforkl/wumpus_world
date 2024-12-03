
import numpy as np
import random

def get_direction_from_auto_pilot(world, mask, agent, breeze, feet):
    possible_directions = ["up","down", "left", "right"]
    direction = random.choice(possible_directions)  # Randomly choose a direction
    return direction