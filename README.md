# MagWorks
A command-line tool for interfacing magnetic stripe devices. 

# Devices
This tool was designed and tested with the MSR605X magentic stripe reader.

The MSR605X is an HID USB device powered solely by the USB port and terminal it is connected to. It is **not** a serial USB device like the MSR605. While this offers the convenience of not needing a power supply or wall outlet, the lack of a serial connection means USB communication with this device is impossible via the convenience of serial libraries. Therefore, this tool is written using PyUSB, a python module that offers complete control of USB ports and connections via device and product identification numbers.

Noting the above, this tool should work with *any* device that uses MSR206 firmware, including the following:
* MSR206
* MSR605
* MSR605X
* MSR606

# Development
This tool is still under development, with the end-goal of achieving complete command-line control of all functions offered by the MSR device.
