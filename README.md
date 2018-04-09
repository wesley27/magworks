# MagWorks
A command-line tool for interfacing magnetic stripe devices. 

# Background
This tool was designed for and tested with the MSR605X magentic stripe reader.

The MSR605X is a USB HID device powered by the USB port and computer it is connected to. It is **not** a USB serial device like the MSR605. While this eliminates the inconvenience of requiring a power supply, the lack of a serial connection means USB communication with this device is impossible via the convenience of serial libraries. 

Therefore, this tool is written using [PyUSB](http://pyusb.github.io/pyusb/), a module for accessing and controlling a computer's USB system. Assuming an understanding of the functionality of USB as well as the device-to-device communication that occurs across a USB connection, [PyUSB](http://pyusb.github.io/pyusb/) allows you to control any device that is connected to a USB port.

Information on the device's firmware was found in the programming manual that is included in this repository.

# Intent
This tool is essentially a command-line driver for MSR devices. It offers HID-based control of any MSR device sporting MSR206 firmware. It offers the reading, writing, and manipulation of data stored on magentic stripe cards.

1. There are numerous tools out there written for serial MSR devices (all utilize serial libraries).
    * Serial libraries handle USB communications for you, only requiring knowledge of the device's firmware.
2. There is next-to-nothing in existence concerning an HID based approach.
3. There is very limited documentation on the direct control of USB devices without using serial libraries.

Hopefully, this repository will act as both a tool, and a reference for those attempting to interface HID devices. Even if you're working with a serial device, taking a non-serial approach will force you to gain a deeper understanding of how USB interactions work.

# Devices
This tool should work with *any* device that uses MSR206 firmware, including the following:
* MSR206
* MSR605
* MSR605X
* MSR606

# Development
This tool is still under development, with the end-goal of achieving complete command-line control of all functions offered by the MSR device.

Current progress and development:
- [x] locate and gain control of msr device
- [x] run device test functions
- [x] led control and led test function
- [x] read ISO card data
- [x] parse ISO card data
- [ ] parse service codes
- [x] read raw card data
- [x] parse raw card data
- [ ] write ISO card data
- [ ] write raw card data
- [ ] clone card data
- [x] erase card data
- [x] get msr-device model (encoded)
- [x] get msr-device firmware (encoded)
