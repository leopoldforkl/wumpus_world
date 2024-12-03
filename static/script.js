let gameState = {};
let inputEnabled = true; // Flag to control whether input is accepted

let autopilotEnabled = false; // Track autopilot state
let autopilotInterval = null; // Interval for autopilot moves

document.addEventListener("DOMContentLoaded", () => {
    loadGameState();

    document.addEventListener("keydown", (event) => {
        if (!inputEnabled) return; // Ignore key strokes when input is disabled

        const directionMap = {
            ArrowUp: "up",
            ArrowDown: "down",
            ArrowLeft: "left",
            ArrowRight: "right"
        };

        if (directionMap[event.key]) {
            moveAgent(directionMap[event.key]);
        }
    });
});

async function loadGameState() {
    try {
        const response = await fetch("/get_game_state");
        gameState = await response.json();
        renderGameBoard();
        updateGameStatus(gameState.status);
        inputEnabled = true; // Enable input after game state is loaded
    } catch (error) {
        console.error("Error loading game state:", error);
    }
}

function renderGameBoard() {
    const board = document.getElementById("game-board");
    const size = gameState.world.length;
    board.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    board.innerHTML = ""; // Clear the board

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");

            // Render "unknown" if the mask is 1
            if (gameState.mask[i][j] === 1) {
                const img = document.createElement("img");
                img.src = "/static/media/unknown.png";
                img.classList.add("background");
                cell.appendChild(img);
            } else {
                // Check if agent is on a dangerous tile or gold
                if (
                    gameState.agent[i][j] === 1 &&
                    [2, 3, 4].includes(gameState.world[i][j])
                ) {
                    // Render only the dangerous tile or gold image
                    const img = document.createElement("img");
                    if (gameState.world[i][j] === 2) {
                        img.src = "/static/media/wumpus.png";
                    } else if (gameState.world[i][j] === 3) {
                        img.src = "/static/media/gold.png";
                    } else if (gameState.world[i][j] === 4) {
                        img.src = "/static/media/pit.png";
                    }
                    img.classList.add("middle");
                    cell.appendChild(img);
                } else {
                    // Background layers: Breeze and Feet
                    if (gameState.breeze[i][j] === 1 && gameState.world[i][j] === 0) {
                        const img = document.createElement("img");
                        img.src = "/static/media/breeze.png";
                        img.classList.add("background");
                        cell.appendChild(img);
                    }
                    if (gameState.feet[i][j] === 1 && gameState.world[i][j] === 0) {
                        const img = document.createElement("img");
                        img.src = "/static/media/feet.png";
                        img.classList.add("background");
                        cell.appendChild(img);
                    }

                    // Middle layers: Wumpus, Gold, and Pit
                    if (gameState.world[i][j] === 2) {
                        const img = document.createElement("img");
                        img.src = "/static/media/wumpus.png";
                        img.classList.add("middle");
                        cell.appendChild(img);
                    } else if (gameState.world[i][j] === 3) {
                        const img = document.createElement("img");
                        img.src = "/static/media/gold.png";
                        img.classList.add("middle");
                        cell.appendChild(img);
                    } else if (gameState.world[i][j] === 4) {
                        const img = document.createElement("img");
                        img.src = "/static/media/pit.png";
                        img.classList.add("middle");
                        cell.appendChild(img);
                    }

                    // Foreground layer: Agent
                    if (gameState.agent[i][j] === 1) {
                        const img = document.createElement("img");
                        img.src = "/static/media/agent.png";
                        img.classList.add("foreground");
                        cell.appendChild(img);
                    }
                }
            }

            board.appendChild(cell);
        }
    }
}

async function toggleAutoPilot() {
    autopilotEnabled = !autopilotEnabled; // Toggle state
    document.getElementById("autopilot-button").innerText = autopilotEnabled
        ? "Stop Auto Pilot"
        : "Start Auto Pilot";

    // Notify server about autopilot state
    try {
        await fetch("/toggle_autopilot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ auto_pilot: autopilotEnabled })
        });

        if (autopilotEnabled) {
            startAutoPilot();
        } else {
            stopAutoPilot();
        }
    } catch (error) {
        console.error("Error toggling autopilot:", error);
    }
}

function startAutoPilot() {
    inputEnabled = false; // Disable manual controls
    autopilotInterval = setInterval(async () => {
        if (!autopilotEnabled) {
            stopAutoPilot();
            return;
        }

        try {
            const response = await fetch("/move_agent", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ direction: null }) // Server decides direction
            });

            const updatedState = await response.json();
            gameState = updatedState; // Update gameState with response
            renderGameBoard();
            updateGameStatus(updatedState.status);

            // Stop autopilot on game over
            if (updatedState.status !== "ok") {
                stopAutoPilot();
            }
        } catch (error) {
            console.error("Error during autopilot move:", error);
            stopAutoPilot();
        }
    }, 1000); // Move every second
}

function stopAutoPilot() {
    inputEnabled = true; // Re-enable manual controls
    autopilotEnabled = false;
    clearInterval(autopilotInterval);
    autopilotInterval = null;

    document.getElementById("autopilot-button").innerText = "Start Auto Pilot";
}

async function moveAgent(direction) {
    if (!inputEnabled) return; // Prevent input if disabled
    inputEnabled = false; // Disable input while processing movement

    try {
        const response = await fetch("/move_agent", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ direction })
        });

        const updatedState = await response.json();
        gameState = updatedState; // Update gameState with the response
        renderGameBoard();
        updateGameStatus(updatedState.status);

        // Disable input if game has ended
        if (updatedState.status !== "ok") {
            inputEnabled = false;
        } else {
            inputEnabled = true;
        }
    } catch (error) {
        console.error("Error moving agent:", error);
        inputEnabled = true; // Re-enable input if an error occurs
    }
}

async function restartGame() {
    stopAutoPilot(); // Ensure autopilot stops on reset
    inputEnabled = false; // Disable input during restart

    try {
        const response = await fetch("/restart", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const resetState = await response.json();
        gameState = resetState; // Update gameState with response
        renderGameBoard();
        updateGameStatus(resetState.status);
        inputEnabled = true; // Re-enable input after game restart
    } catch (error) {
        console.error("Error restarting game:", error);
        inputEnabled = true; // Re-enable input if an error occurs
    }
}

function updateGameStatus(status) {
    const statusElement = document.getElementById("game-status");
    if (status === "ok") {
        statusElement.innerText = ""; // Clear status if the game is ongoing
    } else {
        statusElement.innerText = status; // Display the game status message
    }
}
