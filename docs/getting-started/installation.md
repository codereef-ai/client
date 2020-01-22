# CodeReef client installation

You can install the CodeReef client (CodeReef SDK) on most platforms using PIP as follows:

```
pip install codereef
```

You can also install the CodeReef client using a specific Python version (for example, Python 3.6):
```
python3.6 -m pip install codereef
```

*You may need to add flag "--user" to install the client in the user space:*
```
pip install codereef --user
python3.6 -m pip install codereef --user
```

You should now be able to run this client using one of the following alternative commands:
```
cr

codereef

python3.6 -m codereef
```

If the installation is successful, you will see the list of all [available commands](../guide/commands).

## Prerequisites

The CodeReef client requires minimal dependencies: Python 2.7+ or 3.x, PIP and Git. 

### Linux

You need to have the following packages installed (Ubuntu example):

```
sudo apt-get install python3 python3-pip git wget
```

### MacOS

```
brew install python3 python3-pip git wget
```

### Windows

* Download and install Git from [git-for-windows.github.io](https://git-for-windows.github.io).
* Download and install any Python from [www.python.org/downloads/windows](https://www.python.org/downloads/windows).

### Android (Linux host)

These dependencies are needed to cross-compile for Android (tested on Ubuntu 18.04 including Docker and Windows 10 Subsystem for Linux). 

```
 sudo apt update
 sudo apt install git wget libz-dev curl cmake
 sudo apt install gcc g++ autoconf autogen libtool
 sudo apt install android-sdk
 sudo apt install google-android-ndk-installer
```

### Docker

We prepared several Docker images with CodeReef at [CodeReef Docker hub](https://hub.docker.com/u/codereef).
Select the most relevant image and run it as follows:
```
docker run -p 4444:4444 -it codereef/demo-obj-detection-mlperf-coco-tf-cpu-benchmark-linux-portable-workflows /bin/bash
```
