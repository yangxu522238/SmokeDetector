# SmokeDetector

This is a smart smoke detection system based on qualcomm QCA4020, qualcomm dragonboard 410c development board. 
Its biggest feature is that it can detect the smoke concentration in the home and update it to the server in real time.
If it exceeds a certain concentration, it will send an alarm to the user. 

Hardware Requirements 
-------
qualcomm dragonboard 410c
qualcomm QCA4020 board
mq-2 smoke detector
pixel

Software requirements 
------
pyqt envirment
ubunutu develop envirment
QCA4020 developments 

Instruction
==========

Hardware setup
------
0. Preface
The QCA4020 monitors the status of the smoke sensor. When the monitored value is greater than a certain threshold, the level value of gpio is set to indicate that an event has occurred. For specific implementation, please see QCA4020 Smoke Sensor Data Read.docx

1. Purpose
This article aims to achieve:
(1) The 410c development board monitors the state change of the gpio port to which the QCA4020 is connected, thereby generating an interruption.
(2) Provide a node for the upper layer to view the status of the smoke sensor. One of them indicates that an event has occurred. You can set the node value to 0 by writing to this node

The connection diagram you can find it on QCA4020reciver.doc 

Software Setup
----------
1.Environmental construction
(1) Pyqt environment and python environment to build
(2) Wilddog-python environment to build
In the development environment of Windows 7 and the running environment of the 410c development board, the development environment of wilddog-python needs to be built as follows:
1. Open the cmd command line (open the terminal in the 410c development board), enter the pip list, and the following image appears to indicate that the pip is installed.
2. If the above image does not appear, you need to reinstall PIP. First download the corresponding version of the PIP file in the https://pypi.python.org/pypi/pip#downloads link, extract the PIP installation package to a folder, and then open it. Terminal, enter the decompressed directory, enter python setup.py install, and then add C:\ Python34 \ Scripts to the computer environment variable;
3. After Pip confirms the installation, enter pip install pygatt, pip install requests == 1.1.0 and pip install wilddog-python in the terminal. The following image is displayed indicating that the installation is complete.
4. Open the async.py file in the path C:\Python34\lib\site-packages\wilddog. Modify from lazy import LazyLoadProxy to from .lazy import LazyLoadProxy


Building the application
----------
you can find it in developer detail doc

How to start the application
----------
you can find it in developer detail doc

how to use the application
----------
you can find it in developer detail doc

how to stop appilication
----------
you can find it in developer detail doc










