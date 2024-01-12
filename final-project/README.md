# Final Project

This final project focuses on developing a Web-based Crowd Trajectory Visualization Framework. The aim is to create an interactive application that facilitates the visualization of crowd trajectories on a 2D grid-based map. The project is divided into five key tasks, each addressing a specific aspect of the framework's functionality.

In conclusion, the Web-based Crowd Trajectory Visualization Framework project addresses diverse aspects of crowd simulation and visualization, from setting up the initial software environment to implementing advanced algorithms and providing API support. The framework aims to be a comprehensive tool for researchers and practitioners in the field.

## Installation

The project consist of two parts:

### Back-end

API support to connect Vadera application through the console on the server side and leverage all features of the application.

To run back-end you will need to have the following dependencies installed

- Python 3.7 or higher
- Vadere 2.6 (OS does not matter, must be placed under the builds folder as named "vadere.v2.6")

You can install necessary python libraries by running the following command:

```bash
pip install -r /path/to/requirements.txt
```

After the dependency installation you can run the back-end from `app.py` script. Do not forget to change the port, ip address and other settings according to your needs.

### Front-end

Web-based trajectory visualization application with HTML/CSS and JavaScript. The application will operate on a 2D grid-based map, laying the foundation for the entire framework.

No need to setup any additional dependencies but you need to change API end-point URL according to back-end application. Only browser and you can access the client from `index.html`.

## API Details

### Run Scenario

This Flask API is designed to execute scenarios using Vadere simulation. The `RunScenarioResource` allows you to send a POST request with scenario input data, and it returns the results of the executed scenario.

**URL** : `/run-scenario`

**Method** : `POST`

**Auth required** : NO

<details>
 <summary><b>Data constraints</b></summary>

---

**model_name**

- **Type:** String
- **Constraints:** Required
- **Value:** osm, fsm, gnm

**source**

- **Type:** Object
- **Constraints:** Required

  **shape**

  - **Type:** Object
  - **Constraints:** Required

    **x**

    - **Type:** Number
    - **Constraints:** Required

    **y**

    - **Type:** Number
    - **Constraints:** Required

**event_element_count**

- **Type:** Number
- **Constraints:** Required

**target**

- **Type:** Object
- **Constraints:** Required

  **shape**

  - **Type:** Object
  - **Constraints:** Required

    **x**

    - **Type:** Number
    - **Constraints:** Required

    **y**

    - **Type:** Number
    - **Constraints:** Required

**obstacles**

- **Type:** Array of Objects
- **Constraints:** Optional (if present, must be an array)

  **Each Object in the Array**

  - **id**

    - **Type:** Number
    - **Constraints:** Required
    - **Value:** Can not be 1 or 2

  - **shape**

    - **Type:** Object
    - **Constraints:** Required

      **x**

      - **Type:** Number
      - **Constraints:** Required

      **y**

      - **Type:** Number
      - **Constraints:** Required

      **width**

      - **Type:** Number
      - **Constraints:** Required

      **height**

      - **Type:** Number
      - **Constraints:** Required

---
</details>

<br />
<details>

 <summary><b>Example Request</b></summary>

```json
{
  "model_name": "osm",
  "source": {
    "shape": {
      "x": 5,
      "y": 5
    },
    "event_element_count": 1
  },
  "target": {
    "shape": {
      "x": 30,
      "y": 30
    }
  },
  "obstacles": [
    {
      "id": 29,
      "shape": {
        "x": 25,
        "y": 15,
        "width": 1,
        "height": 5
      }
    },
    {
      "id": 28,
      "shape": {
        "x": 20,
        "y": 15,
        "width": 2,
        "height": 5
      }
    }
  ]
}
```
</details>

</br>

<details>

 <summary><b>Success Response</b></summary>

**Code** : `200 OK`

**Content example**

```json
{
  "token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```
</details>

---