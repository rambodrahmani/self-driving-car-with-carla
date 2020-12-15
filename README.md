# Self-driving car with CARLA Simulator
Self-driving car with CARLA Simulator and Python 3.7 on Ubuntu 18.04.

# Prerequisites
Install Python 3.7:
```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install python3.7
python3.7 --version
```

Install libxerces-c-dev by entering the following commands in the terminal:
```bash
sudo apt install libxerces-c-dev
```

Install Python packages required for CARLA Simulator:
```bash
python3.7 -m pip install --user pygame numpy networkx
```

# Install Carla Simulator
The repository contains different versions of the simulator available.
Development and stable sections list the packages for the different official
releases. The later the version the more experimental it is. The nightly build
is the current development version as today and so, the most unstable.

**CARLA Version: 0.9.10**

[Carla Simulator Download](https://github.com/carla-simulator/carla/blob/master/Docs/download.md)
