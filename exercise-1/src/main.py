"""
Cellular Automata Simulation GUI

This script serves as the entry point for a graphical user interface (GUI) for a cellular automata simulation.
The GUI allows users to create, load, and interact with scenarios involving pedestrians, targets, and obstacles.

Usage:
To run the GUI application, execute this script. It will import the MainGUI class from the `gui` module and
start the GUI, enabling users to work with cellular automata scenarios.

Example:
```python
python main.py
```
"""

from gui import MainGUI


if __name__ == '__main__':
    gui = MainGUI()
    gui.start_gui()


