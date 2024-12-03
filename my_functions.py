import numpy as np
import random

def initialize_world():
    world = np.array([
    [0, 0, 0, 4],
    [2, 3, 4, 0],
    [0, 0, 0, 0],
    [0, 0, 4, 0]
    ])

    breeze = np.array([
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 1]
    ])

    feet = np.array([
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0]
    ])

    agent = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 0, 0, 0]
    ])

    mask = np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 1]
    ])
    return world, agent, breeze, feet, mask

def move_agent_py(mask, agent, direction, world):

    pos = np.argwhere(agent == 1)[0]
    x, y = pos

    # Move logic
    if direction == "up" and x > 0:
        agent[x, y], agent[x - 1, y] = 0, 1
    elif direction == "down" and x < agent.shape[0] - 1:
        agent[x, y], agent[x + 1, y] = 0, 1
    elif direction == "left" and y > 0:
        agent[x, y], agent[x, y - 1] = 0, 1
    elif direction == "right" and y < agent.shape[1] - 1:
        agent[x, y], agent[x, y + 1] = 0, 1

    # Update mask: reveal the new agent position
    mask[np.argwhere(agent == 1)[0][0], np.argwhere(agent == 1)[0][1]] = 0

    interaction = np.sum(world * agent)
    if interaction == 2:
        status = "Game Over - Eaten by Wumpus"
    elif interaction == 4:
        status = "Game Over - Drowned in Pit"
    elif interaction == 3:
        status = "Gold Found - You Win"
    else:
        status = "ok"

    return agent, mask, status


def get_direction_from_auto_pilot(world, mask, agent, breeze, feet):
    possible_directions = ["up","down", "left", "right"]
    direction = random.choice(possible_directions)  # Randomly choose a direction
    return direction