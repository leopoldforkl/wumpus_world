
# The Wumpus Game

The Wumpus Game is a web-based grid game where players navigate an agent through a customizable grid, avoiding dangers such as pits and the Wumpus while aiming to collect gold. The game includes both manual controls and an optional autopilot mode for automated gameplay.

---

## Features

- **Dynamic Grid Size**: The grid size is configurable (default is 5x5).
- **Interactive Gameplay**: Use arrow keys to control the agent or enable autopilot for automated movements.
- **Game Feedback**: Provides real-time updates on game status, including:
  - **Game Over**: When encountering a Wumpus or falling into a pit.
  - **You Win**: Upon finding gold.
- **Autopilot Mode**: Lets the system navigate the agent automatically.
- **Restart Functionality**: Reset the game to start fresh at any time.

---

## Technologies Used

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Handling**: NumPy for matrix operations

---

## Project Structure

```
root/
├── static/
│   ├── media/              # Game assets (images)
│   │   ├── agent.png
│   │   ├── breeze.png
│   │   ├── feet.png
│   │   ├── gold.png
│   │   ├── pit.png
│   │   ├── unknown.png
│   │   └── wumpus.png
│   ├── styles.css          # CSS for styling
│   └── script.js           # JavaScript for interactivity
├── templates/
│   └── index.html          # HTML for the game interface
├── app.py                  # Flask backend
├── my_functions.py         # Core game logic and helper functions
├── auto_pilot.py           # Autopilot functionalities
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── development.ipynb       # Notebook for debugging and experiments
```

---

## Installation and Setup

### Prerequisites

Ensure you have Python 3.7+ installed on your system.

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv wumpus_venv
   source wumpus_venv/bin/activate  # On Windows: wumpus_venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8080/
   ```

---

## How to Play

1. **Manual Mode**:
   - Use the arrow keys to move the agent:
     - **Up Arrow**: Move up
     - **Down Arrow**: Move down
     - **Left Arrow**: Move left
     - **Right Arrow**: Move right

2. **Autopilot Mode**:
   - Click the **Start Auto Pilot** button to let the system play the game for you.
   - Stop the autopilot at any time by clicking the **Stop Auto Pilot** button.

3. **Restart the Game**:
   - Click the **Restart** button to reset the game.

---

## Gameplay Rules

- The agent starts in a random position on the grid.
- The **mask** obscures unexplored areas until the agent moves to them.
- Game objects include:
  - **Wumpus**: Instant game over if encountered.
  - **Pits**: Instant game over if fallen into.
  - **Gold**: Win the game upon collecting it.
  - **Breeze**: Indicates nearby pits.
  - **Feet**: Indicates the proximity of the Wumpus.
- The agent can move in four directions (up, down, left, right).
- Autopilot mode allows the system to decide movements based on randomized logic.

---

## Advanced Features

- **Autopilot Integration**: The autopilot algorithm chooses a random direction for the agent's next move.
- **Customizable Grid Size**: Change the grid size by modifying the `N` variable in `app.py`.
- **Dynamic Rendering**: The game board updates in real-time based on the agent's movements and interactions.

---

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features. Contributions are welcome!

---

## License

To be determined.

---