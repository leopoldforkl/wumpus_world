let gameState = {};
let inputEnabled = true; // Flag to control whether input is accepted

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
    const response = await fetch("/get_game_state");
    gameState = await response.json();
    renderGameBoard();
    inputEnabled = true; // Enable input after game state is loaded
}

function renderGameBoard() {
    const board = document.getElementById("game-board");
    const size = gameState.world.length;
    board.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    board.innerHTML = "";

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
            }

            // Foreground layer: Agent
            if (gameState.agent[i][j] === 1) {
                const img = document.createElement("img");
                img.src = "/static/media/agent.png";
                img.classList.add("foreground");
                cell.appendChild(img);
            }

            board.appendChild(cell);
        }
    }
}

async function moveAgent(direction) {
    inputEnabled = false; // Disable input while processing movement
    const response = await fetch("/move_agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ direction })
    });

    const result = await response.json();
    if (result.status === "pending") {
        renderAgent(result.agent_position); // Render the agent's new position

        // Check for game status after a brief delay
        setTimeout(async () => {
            const statusResponse = await fetch("/check_game_status");
            const statusResult = await statusResponse.json();

            if (statusResult.status === "ok") {
                loadGameState(); // Reload full game state if no game-over
            } else {
                document.getElementById("game-status").innerText = statusResult.status;
                setTimeout(() => {
                    loadGameState(); // Reload the board after a brief delay
                }, 500); // 1.5-second delay
            }
        }, 10); // Delay to visually display agent movement
    }
}

function renderAgent(agentMatrix) {
    const board = document.getElementById("game-board");
    const cells = board.querySelectorAll(".cell");
    const size = Math.sqrt(cells.length); // Grid size

    // Remove existing agent
    cells.forEach(cell => {
        const agentImg = cell.querySelector("img.foreground");
        if (agentImg) cell.removeChild(agentImg);
    });

    // Add the agent at the new position
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            if (agentMatrix[i][j] === 1) {
                const img = document.createElement("img");
                img.src = "/static/media/agent.png";
                img.classList.add("foreground");
                cells[i * size + j].appendChild(img);
            }
        }
    }
}

async function restartGame() {
    inputEnabled = false; // Disable input during restart
    const response = await fetch("/restart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });

    const result = await response.json();
    if (result.status === "Game Restarted") {
        loadGameState(); // Reload the game state
        document.getElementById("game-status").innerText = ""; // Clear game status
    }
}
