function generateApiInput() {
    const apiInput = {
        model_name: "osm",
        source: {
            shape: {
                x: -1,
                y: -1,
            },
            event_element_count: 0,
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
                apiInput.target.shape.y = rows-i-1;
            } else if (matrix[i][j].type === 1) {
                apiInput.source.shape.x = j;
                apiInput.source.shape.y = rows-i;
                apiInput.source.event_element_count = 1;
            } else if (matrix[i][j].type === 2){
                const obstacle = {
                    id: generateUniqueId(i, j),
                    shape: {
                        x: j,
                        y: rows-i-1,
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
        })
        .catch((error) => {
            console.error("API Request Error:", error);
        });
}
