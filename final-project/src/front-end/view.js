const matrix = [];
const gridSize = 30;
const screenWidth = window.innerWidth - gridSize;
const screenHeight = window.innerHeight - 80;
const rows = Math.floor(screenHeight / gridSize);
const cols = Math.floor(screenWidth / gridSize);

let isMouseDown = false;
let targetExists = false;
let sourceExists = false;
let deleteMode = false;
let elementSelection = "obstacle";
let source_element_count = 1;

for (let i = 0; i < rows; i++) {
    matrix[i] = [];
    for (let j = 0; j < cols; j++) {
        const grid = document.createElement("div");
        grid.classList.add("grid");
        grid.style.width = gridSize + "px";
        grid.style.height = gridSize + "px";
        matrix[i][j] = grid;
        document.body.appendChild(grid);

        grid.addEventListener("mousedown", function () {
            isMouseDown = true;
            if (deleteMode) {
                clearElement(this);
            } else {
                setGridType(this);
            }
        });

        grid.addEventListener("mouseup", function () {
            isMouseDown = false;
        });

        grid.addEventListener("mousemove", function () {
            if (isMouseDown) {
                if (deleteMode) {
                    clearElement(this);
                } else {
                    setGridType(this);
                }
            }
        });
    }
}

function clearElement(grid) {
    if (grid.type == 0) {
        targetExists = false;
    } else if (grid.type == 1) {
        sourceExists = false;
    }
    grid.style.backgroundColor = "";
    grid.type = -1;
}

function setGridType(grid) {
    switch (elementSelection) {
        case "target":
            if (!targetExists) {
                grid.style.backgroundColor = "red";
                grid.type = 0;
                targetExists = true;
            }
            break;
        case "source":
            if (!sourceExists) {
                grid.style.backgroundColor = "green";
                grid.type = 1;
                sourceExists = true;
                openPedestrianModal();
            }
            break;
        case "obstacle":
            grid.style.backgroundColor = "#808080";
            grid.type = 2;
            break;
    }
}

function setElementSelection(type) {
    deleteMode = false;
    elementSelection = type;
}

function setDeleteMode() {
    deleteMode = !deleteMode;
    clearSimulation();
    disableButtons();
}

function openPedestrianModal() {
    const modal = document.getElementById("pedestrianModal");
    modal.style.display = "block";
}

function closePedestrianModal() {
    const modal = document.getElementById("pedestrianModal");
    modal.style.display = "none";
    isMouseDown = false;
}

function confirmPedestrianInput() {
    const numPedestriansInput = document.getElementById("pedestrianInput");
    const numPedestrians = parseInt(numPedestriansInput.value);

    if (!isNaN(numPedestrians) && Number.isInteger(numPedestrians)) {
        source_element_count = numPedestrians;
        closePedestrianModal();
    } else {
        alert(
            "Invalid input. Please enter a valid integer for the number of pedestrians."
        );
    }
}

function closeModelModal() {
    const modal = document.getElementById("modelModal");
    modal.style.display = "none";
}

const confirmModelButton = document.getElementById("confirmModelButton");
confirmModelButton.addEventListener("click", function () {
    const selectedModel = modelSelect.value;
    if (selectedModel) {
        closeModelModal();
        clearSimulation();
        disableButtons();

        if (targetExists && sourceExists) {
            sendApiRequest(selectedModel);
        }
    }
});

function clearSimulation() {
    const circles = document.querySelectorAll(".circle");
    circles.forEach((circle) => circle.parentNode.removeChild(circle));
}

const startSimulationButton = document.getElementById("startSimulationButton");
const stopSimulationButton = document.getElementById("stopSimulationButton");
const fastForwardButton = document.getElementById("fastForwardButton");
const previousStepButton = document.getElementById("previousStepButton");
const nextStepButton = document.getElementById("nextStepButton");
const currentStepSpan = document.getElementById("currentStep");

startSimulationButton.addEventListener("click", startSimulation);
stopSimulationButton.addEventListener("click", stopSimulation);
fastForwardButton.addEventListener("click", fastForwardSimulation);
previousStepButton.addEventListener("click", previousStep);
nextStepButton.addEventListener("click", nextStep);

function startSimulation() {
    if (maxStepCount == 0) {
        alert("Simulation data is empty");
        return;
    }

    simulationInterval = setInterval(() => {
        if (currentStep < maxStepCount) {
            displaySimulationResults(currentStep);
            currentStep++;

            updateCurrentStepDisplay();
        } else {
            stopSimulation();
        }
    }, 1000);
}

function stopSimulation() {
    clearInterval(simulationInterval);
}

function fastForwardSimulation() {
    if (maxStepCount == 0) {
        alert("Simulation data is empty");
        return;
    }

    if (simulationInterval) {
        stopSimulation();
    }

    simulationInterval = setInterval(() => {
        if (currentStep < maxStepCount) {
            displaySimulationResults(currentStep);
            currentStep++;

            updateCurrentStepDisplay();
        } else {
            stopSimulation();
        }
    }, 250);
}

function previousStep() {
    if (currentStep > 0) {
        currentStep--;
        removeCirclesByStep(currentStep);
        updateCurrentStepDisplay();
    }
}

function nextStep() {
    if (currentStep <= maxStepCount - 1) {
        displaySimulationResults(currentStep);
        currentStep++;
        updateCurrentStepDisplay();
    }
}

function updateCurrentStepDisplay() {
    currentStepSpan.textContent = `Step: ${currentStep}`;
}

function removeCirclesByStep(step) {
    const circles = document.querySelectorAll('.circle[id="' + step + '"]');

    circles.forEach((circle) => {
        circle.parentNode.removeChild(circle);
    });
}

function enableButtons() {
    startSimulationButton.disabled = false;
    stopSimulationButton.disabled = false;
    fastForwardButton.disabled = false;
    previousStepButton.disabled = false;
    nextStepButton.disabled = false;
}

function disableButtons() {
    startSimulationButton.disabled = true;
    stopSimulationButton.disabled = true;
    fastForwardButton.disabled = true;
    previousStepButton.disabled = true;
    nextStepButton.disabled = true;
    currentStepSpan.textContent = "Step: 0";
}
