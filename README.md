# The Wumpus Game

The Wumpus Game is a web-based grid game where players navigate an agent through a 4x4 matrix, avoiding dangers such as pits and the Wumpus while aiming to collect gold. The game is built using Flask for the backend and JavaScript for dynamic user interactions.

---

## Features

- A 4x4 grid representing the game world.
- Dynamic rendering of game objects like Wumpus, gold, pits, breeze, feet, and the agent.
- Keyboard controls for moving the agent (arrow keys).
- Interactive feedback based on the agent's position:
  - **Game Over** when encountering a Wumpus or falling into a pit.
  - **You Win** upon finding gold.
- Restart button to reset the game.

---

## Technologies Used

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Data Handling:** NumPy for matrix operations

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
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## Installation and Setup

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

1. Use the arrow keys to move the agent:
   - **Up Arrow:** Move up
   - **Down Arrow:** Move down
   - **Left Arrow:** Move left
   - **Right Arrow:** Move right

2. Avoid dangers:
   - **Wumpus:** (Game Over - Eaten by Wumpus)
   - **Pit:** (Game Over - Drowned in Pit)

3. Collect the gold to win the game:
   - (Gold Found - You Win)

4. Restart the game using the "Restart" button.

---

## Gameplay Rules

- The agent starts in the bottom-left corner.
- The breeze and feet tiles provide hints about nearby pits and Wumpus respectively.
- Landing on a tile with the gold wins the game.
- The game ends immediately if the agent lands on a tile with the Wumpus or a pit.

---

## Screenshots

![Game Board Example](static/media/screenshot.png) <!-- Replace with an actual screenshot if available -->

---

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features!

---

## License

t.b.d

--- 
