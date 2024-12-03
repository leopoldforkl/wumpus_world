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

            // Middle layers: Wumpus, Gold, and Pit (overwrite background)
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

            // Foreground layer: Agent (always on top)
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
    if (result.status === "ok") {
        loadGameState();
    } else {
        document.getElementById("game-status").innerText = result.status;
        setTimeout(() => {
            loadGameState(); // Reload the board after a brief delay
        }, 1500); // 1.5-second delay
    }
}
