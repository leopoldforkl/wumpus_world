# Run with: python app.py

from flask import Flask, render_template, jsonify, request
import numpy as np
import os

app = Flask(__name__)

# Matrices representing the game state
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_game_state", methods=["GET"])
def get_game_state():
    return jsonify({
        "world": world.tolist(),
        "breeze": breeze.tolist(),
        "feet": feet.tolist(),
        "agent": agent.tolist(),
        "mask": mask.tolist()  # Include the mask array
    })


@app.route("/move_agent", methods=["POST"])
def move_agent():
    global agent, mask
    data = request.json
    direction = data.get("direction")
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

    # Return updated game state
    return jsonify({
        "status": "pending",
        "agent_position": agent.tolist(),
        "mask": mask.tolist()  # Return updated mask
    })


@app.route("/check_game_status", methods=["GET"])
def check_game_status():
    # Check for game-ending conditions after agent movement
    interaction = np.sum(world * agent)
    if interaction == 2:
        reset_agent()
        return jsonify({"status": "Game Over - Eaten by Wumpus"})
    elif interaction == 4:
        reset_agent()
        return jsonify({"status": "Game Over - Drowned in Pit"})
    elif interaction == 3:
        reset_agent()
        return jsonify({"status": "Gold Found - You Win"})
    else:
        return jsonify({"status": "ok"})

def reset_agent():
    """Reset the agent matrix to the starting position."""
    global agent
    agent.fill(0)
    start_position = (agent.shape[0] - 1, 0)  # Bottom-left corner
    agent[start_position] = 1

def reset_mask():
    global mask
    mask = np.ones_like(world)  # Reset mask to all 1s
    mask[agent.shape[0] - 1, 0] = 0  # Reveal the starting position

@app.route("/restart", methods=["POST"])
def restart_game():
    reset_agent()
    reset_mask()  # Reset the mask when restarting
    return jsonify({"status": "Game Restarted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
