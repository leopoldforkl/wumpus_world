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
    [0, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 1]
])

feet = np.array([
    [1, 0, 0, 0],
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
    })


@app.route("/move_agent", methods=["POST"])
def move_agent():
    global agent
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

    # Game status check
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
