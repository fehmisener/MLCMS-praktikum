# Exercise 2

## Project Setup

> **Note**
> There might be different requirements between operation systems, this guid is prepared for macOS.

First you have to initialize environment for [VADERE software](http://www.vadere.org/releases/) as it described in offical software page. We prefer to use Vadere v2.6 and it is located under builds folder.

### Vadere

Java 17 Installation

```bash
$ brew install openjdk@17

$ sudo ln -sfn /usr/local/opt/openjdk@17/libexec/openjdk.jdk \
     /Library/Java/JavaVirtualMachines/openjdk-17.jd
```

To Run Vadere

```bash
$ java -jar builds/vadere.v2.6.linux/vadere-gui.jar
```

### Python

Requirement installation

```bash
pip install -r requirements.txt
```

Start the pedestrian adder for the task 3 (You may find detailed information on file pydoc)

> **Note**
> Becareful about your root path.

```bash
python src/pedestrian_adder.py --path vadere/scenarios/rimea6.scenario --output vadere/scenarios/
```

## Project Structure

```bash
.
├── assignment                # Exercise documents
├── builds                    # Vadere source codes
├── src                       # Source files of the project
├── vadere                    
│   ├── output                # Results of the scenarios
│   └── scenarios             # Scenario files of the exercise
├── README.md
└── requirements.txt
```
