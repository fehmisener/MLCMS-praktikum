# Exercise 1

In this exercise, you will learn how to model and simulate a human crowd using a basic cellular automaton.

As a group of four, we have successfully completed all four tasks.

## Project Setup

First you have to initialize environment
> **Note**
> Using virtual environment would be better

```bash
pip install -r requirements.txt
```

Start the GUI

```bash
python src/main.py
```

## Project Structure

```bash
.
├── assignment              # Exercise documents
├── scenarios               # JSON files of the scenarios
├── src                     # Source files of project
├── README.md
└── requirements.txt
```

## Project Flow

Once you start the application, the simulation gui will be popup and you will be able to start simulations with manual or pre-defined json files but main flow always starts with [main.py](src/main.py) and it creates `new GUI` object from [gui.py](src/gui.py). 

As it described in the class document, `Class MainGUI` contains graphical interface elements, controls workflows between application logics and provides inital setup. It uses both `Pedestrian` and `Scenario` classes from [scenario_elements.py](src/scenario_elements.py) to perform simulations. This `scenario_elements` is used to hold simulation objects and necessary methods.

Detailed task explanations can be found on [report file.](assignment/exercise%20sheet%201.pdf)