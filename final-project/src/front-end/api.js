function generateApiInput(modelName) {
    const apiInput = {
        model_name: modelName,
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

let groupedData = {};
let currentStep = 0;
let maxStepCount = 0;

function sendApiRequest(modelName) {
    const apiInput = generateApiInput(modelName);

    groupedData = {};
    currentStep = 0;
    maxStepCount = 0;

    fetch("http://127.0.0.1:5000/run-scenario", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(apiInput),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("API Response:", data);
            groupedData = groupByPedestrianId(data.data);
            maxStepCount = findMaxIterationCount(groupedData);
            enableButtons();
        })
        .catch((error) => {
            console.error("API Request Error:", error);
        });
}

const groupByPedestrianId = (data) => {
    const grouped = {};
    data.forEach((item) => {
        const pid = item.pedestrianId;
        if (!grouped[pid]) {
            grouped[pid] = [];
        }
        grouped[pid].push(item);
    });
    return grouped;
};

function findMaxIterationCount(groupedData) {
    return Math.max(
        ...Object.values(groupedData).map((dataArray) => dataArray.length)
    );
}

function displaySimulationResults(step) {
    const bottomLeftPositions = matrix[rows - 1][0].getBoundingClientRect();

    Object.keys(groupedData).forEach((pedestrianId) => {
        const dataAtStep = groupedData[pedestrianId][step];

        if (dataAtStep) {
            let circle = document.createElement("div");

            circle.id = step;
            circle.classList.add("circle");
            circle.style.backgroundColor = getRandomColor(pedestrianId);

            circle.style.left =
                bottomLeftPositions.left +
                (dataAtStep["startX-PID1"] - 0.2) * gridSize +
                "px";
            circle.style.top =
                bottomLeftPositions.bottom -
                (dataAtStep["startY-PID1"] + 0.3) * gridSize +
                "px";

            matrix[rows - Math.floor(dataAtStep["startY-PID1"]) - 1][
                Math.floor(dataAtStep["startX-PID1"])
            ].appendChild(circle);
        }
    });
}

function getRandomColor(pedestrianId) {
    const seed = pedestrianId * 17;
    const randomValue = Math.abs(Math.sin(seed));
    const hue = randomValue * 360;
    return `hsl(${hue}, 100%, 50%)`;
}

function openModelModal() {
    const apiUrl = "http://127.0.0.1:5000/get-models";

    fetch(apiUrl)
        .then((response) => response.json())
        .then((models) => {
            populateModelSelect(models);
            modelModal.style.display = "block";
        })
        .catch((error) => console.error("Error fetching models:", error));
}

function populateModelSelect(models) {
    modelSelect.innerHTML = "";
    models.data.forEach((model) => {
        const option = document.createElement("option");
        option.value = model;
        option.text = model.toUpperCase();
        modelSelect.appendChild(option);
    });
}
