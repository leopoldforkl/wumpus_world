# Run with: python app.py

from flask import Flask, render_template, jsonify, request
import numpy as np
import os

from my_functions import (
    initialize_world,
    move_agent_py
)

from auto_pilot import (
    get_direction_from_auto_pilot
)

# Add the global variable for autopilot mode
auto_pilot = False  # Default mode is manual
N=5

app = Flask(__name__)

# Matrices representing the game state
world, agent, breeze, feet, mask = initialize_world(N)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/toggle_autopilot", methods=["POST"])
def toggle_autopilot():
    global auto_pilot
    data = request.json
    auto_pilot = data.get("auto_pilot", False)  # Update autopilot mode
    return jsonify({"auto_pilot": auto_pilot, "status": "ok"})


@app.route("/get_game_state", methods=["GET"])
def get_game_state():
    status = "ok"
    return jsonify({
        "world": world.tolist(),
        "breeze": breeze.tolist(),
        "feet": feet.tolist(),
        "agent": agent.tolist(),
        "mask": mask.tolist(),
        "status": status
    })


@app.route("/move_agent", methods=["POST"])
def move_agent():
    global agent, mask
    data = request.json
    direction = data.get("direction")

    if auto_pilot:
        direction = get_direction_from_auto_pilot(world, mask, agent, breeze, feet)

    agent, mask, status = move_agent_py(mask, agent, direction, world)

    # Return updated game state
    return jsonify({
        "world": world.tolist(),
        "breeze": breeze.tolist(),
        "feet": feet.tolist(),
        "agent": agent.tolist(),
        "mask": mask.tolist(),
        "status": status
    })


@app.route("/restart", methods=["POST"])
def restart_game():
    global world, agent, breeze, feet, mask, auto_pilot
    auto_pilot = False  # Ensure autopilot is deactivated during restart
    world, agent, breeze, feet, mask = initialize_world(N)

    status = "ok"

    return jsonify({
        "world": world.tolist(),
        "breeze": breeze.tolist(),
        "feet": feet.tolist(),
        "agent": agent.tolist(),
        "mask": mask.tolist(),
        "auto_pilot": auto_pilot,  # Include autopilot state in the response
        "status": status
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
