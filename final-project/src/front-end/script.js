function clearElemets() {
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            matrix[i][j].style.backgroundColor = "";
            matrix[i][j].type = -1;
        }
    }

    const circles = document.querySelectorAll(".circle");
    circles.forEach((circle) => circle.parentNode.removeChild(circle));

    targetExists = false;
    sourceExists = false;
    source_element_count = 1;
    elementSelection = "obstacle";
    disableButtons();
}

function uploadJsonFile() {
    const fileInput = document.getElementById("jsonFile");
    fileInput.click();
}

function initializeMap() {
    const fileInput = document.getElementById("jsonFile");
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const content = e.target.result;
            try {
                const json = JSON.parse(content);
                initializeMapFromJSON(json);
            } catch (error) {
                alert("Invalid JSON file.");
            }
        };
        reader.readAsText(file);
    }
}

function initializeMapFromJSON(json) {
    clearElemets();

    json.obstacles.forEach((obstacle) => {
        const { locationX, locationY, type } = obstacle;
        if (
            locationX >= 0 &&
            locationX < rows &&
            locationY >= 0 &&
            locationY < cols
        ) {
            setObstacleType(type);
            const rowIndex = locationX;
            const colIndex = locationY;
            matrix[rowIndex][colIndex].isObstacle = true;

            if (type === "target") {
                targetExists = true;
            }
        }
    });
}

function toggleDropdown() {
    const dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.classList.toggle("hidden");
}

window.onclick = function (event) {
    if (!event.target.matches(".dropdown button")) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (!openDropdown.classList.contains("hidden")) {
                openDropdown.classList.add("hidden");
            }
        }
    }
};
