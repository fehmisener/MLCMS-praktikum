function generateApiInput() {
    const apiInput = {
        model_name: "osm",
        width: cols,
        height: rows,
        source: {
            shape: {
                x: -1,
                y: -1,
            },
            event_element_count: source_element_count,
        },
        target: {
            shape: {
                x: -1,
                y: -1,
            },
        },
        obstacles: [],
    };

    // Find source and target positions
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            if (matrix[i][j].type === 0) {
                apiInput.target.shape.x = j;
                apiInput.target.shape.y = rows - i - 1;
            } else if (matrix[i][j].type === 1) {
                apiInput.source.shape.x = j;
                apiInput.source.shape.y = rows - i - 1;
            } else if (matrix[i][j].type === 2) {
                const obstacle = {
                    id: generateUniqueId(i, j),
                    shape: {
                        x: j,
                        y: rows - i - 1,
                        width: 1,
                        height: 1,
                    },
                };
                apiInput.obstacles.push(obstacle);
            }
        }
    }
    return apiInput;
}

function generateUniqueId(x, y) {
    return parseInt(x, 10) * 100 + parseInt(y, 10);
}

function sendApiRequest() {
    const apiInput = generateApiInput();

    fetch("http://localhost:5000/run-scenario", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(apiInput),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("API Response:", data);
            displaySimulationResults(data);
        })
        .catch((error) => {
            console.error("API Request Error:", error);
        });
}

function displaySimulationResults(response) {
    const data = response.data;

    data.forEach((move, index) => {
        const pedestrianId = move.pedestrianId;

        // Create a circle for each move
        const circle = document.createElement("div");
        circle.classList.add("circle");

        bottomLeftPositions = matrix[rows - 1][0].getBoundingClientRect();

        circle.style.left =
            bottomLeftPositions.left +
            (move["startX-PID1"] - 0.2) * gridSize +
            "px";
        circle.style.top =
            bottomLeftPositions.bottom -
            (move["startY-PID1"] + 0.3) * gridSize +
            "px";

        circle.style.backgroundColor = getRandomColor(pedestrianId);

        matrix[rows - Math.floor(move["startY-PID1"]) - 1][
            Math.floor(move["startX-PID1"])
        ].appendChild(circle);

        /*
        if (index > 0) {
            const prevMove = data[index - 1];

            const line = document.createElement('div');
            line.classList.add('line');
            line.style.width = '2px'; // Adjust based on your preference
            line.style.height = Math.sqrt((move.startX - prevMove.endX) ** 2 + (move.startY - prevMove.endY) ** 2) * gridSize + 'px';
            line.style.backgroundColor = 'orange';
            line.style.position = 'absolute';
            line.style.left = move.startX * gridSize + 'px';
            line.style.top = move.startY * gridSize + 'px';
            line.style.transformOrigin = 'top';
            line.style.transform = `rotate(${Math.atan2(move.startY - prevMove.endY, move.startX - prevMove.endX)}rad)`;
            matrix[move.startX][move.startY].appendChild(line);
        }
        */
    });
}

function getRandomColor(pedestrianId) {
    const seed = pedestrianId * 17; // Use a constant multiplier to vary the seed
    const randomValue = Math.abs(Math.sin(seed));
    const hue = randomValue * 360; // Hue value between 0 and 360
    return `hsl(${hue}, 100%, 50%)`; // Convert to HSL color format
}
