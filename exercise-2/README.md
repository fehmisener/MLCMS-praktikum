# Exercise 2

## Project Setup

> **Note**
> There might be different requirements between operation systems, this guid is prepared for macOS.

First you have to initialize environment for [VADERE software](http://www.vadere.org/releases/) as it described in offical software page. We prefer to use Vadere v2.6.

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

## Project Structure

```bash
.
├── assignment                # Exercise documents
├── builds                    # Vadere source codes
├── vadere                    # Vadere project files 
├── README.md
└── requirements.txt
```