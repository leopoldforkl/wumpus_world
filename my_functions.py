import numpy as np
import random


def initialize_world(N):
    # Initialize the agent matrix
    agent = np.zeros((N, N), dtype=int)
    agent_position = (random.randint(0, N-1), random.randint(0, N-1))
    agent[agent_position] = 1

    # Initialize the mask matrix
    mask = 1 - agent

    # Initialize the world matrix
    world = np.zeros((N, N), dtype=int)

    # Helper function to check valid placement
    def is_valid_placement(x, y, avoid_pos, world):
        if (x, y) in avoid_pos or not (0 <= x < N and 0 <= y < N) or world[x, y] != 0:
            return False
        return True

    # Place objects in the world
    def place_objects_in_world(world, avoid_pos, num, count):
        positions = []
        for _ in range(count):
            loop_count = 0
            while True:
                x, y = random.randint(0, N-1), random.randint(0, N-1)
                loop_count+=1
                if is_valid_placement(x, y, avoid_pos, world):
                    world[x, y] = num
                    avoid_pos.update([(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])
                    positions.append((x, y))
                    break
                if loop_count > 1000: #in case no valid solution can be found
                    break
        return positions

    # Set up avoid positions around the agent
    avoid_positions = set(
        [(agent_position[0] + dx, agent_position[1] + dy) 
         for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    )
    avoid_positions.add(agent_position)

    # Place objects
    place_objects_in_world(world, avoid_positions, 2, 1)  # Place one '2'
    place_objects_in_world(world, avoid_positions, 3, 1)  # Place one '3'
    place_objects_in_world(world, avoid_positions, 4, 3)  # Place three '4's

    # Initialize the breeze matrix
    breeze = np.zeros((N, N), dtype=int)
    for x, y in zip(*np.where(world == 4)):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                breeze[nx, ny] = 1

    # Initialize the feet matrix
    feet = np.zeros((N, N), dtype=int)
    for x, y in zip(*np.where(world == 2)):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                feet[nx, ny] = 1

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
