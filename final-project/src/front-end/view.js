const matrix = [];
const gridSize = 30;
const screenWidth = window.innerWidth - gridSize;
const screenHeight = window.innerHeight - 80;
const rows = Math.floor(screenHeight / gridSize);
const cols = Math.floor(screenWidth / gridSize);

let isMouseDown = false;
let targetExists = false;
let sourceExists = false;
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
            setGridType(this);
        });

        grid.addEventListener("mouseup", function () {
            isMouseDown = false;
        });

        grid.addEventListener("mousemove", function () {
            if (isMouseDown) {
                setGridType(this);
            }
        });
    }
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
    elementSelection = type;
}

function openPedestrianModal() {
    const modal = document.getElementById('pedestrianModal');
    modal.style.display = 'block';
}

function closePedestrianModal() {
    const modal = document.getElementById('pedestrianModal');
    modal.style.display = 'none';
}

function confirmPedestrianInput() {
    const numPedestriansInput = document.getElementById('pedestrianInput');
    const numPedestrians = parseInt(numPedestriansInput.value);

    if (!isNaN(numPedestrians) && Number.isInteger(numPedestrians)) {
		source_element_count = numPedestrians;
        closePedestrianModal();
    } else {
        alert('Invalid input. Please enter a valid integer for the number of pedestrians.');
    }
}