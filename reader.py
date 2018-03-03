import sys
import usb.core
import usb.util

from codes import *

class Reader:
    
    """ Initialize the reader class. """
    def __init__(self):
        self.vid = VENDOR_ID
        self.pid = PRODUCT_ID

    """ Initialize the device and claim it."""
    def claim_reader(self):
        self.dev = usb.core.find(idVendor = self.vid, idProduct = self.pid)

        # ensure msr exists
        if self.dev is None:
            sys.exit("MagWorks could not find any card readers.")
        print("Card reader located.")

        # disable any existing drivers
        if self.dev.is_kernel_driver_active(0):
            try:
                self.dev.detach_kernel_driver(0)
                print("Existing kernel driver has been detached.")
            except usb.core.USBError as e:
                sys.exit("MagWorks was unable to detach the existing kernel driver: %s" % str(e))

        # set up msr configuration
        try:
            self.dev.set_configuration()
            self.dev.reset()
        except usb.core.USBError as e:
            sys.exit("MagWorks failed to set the MSR configuration: %s" % str(e))
        print("Card reader configuration set.")

        msg = '\xc2%s' % RESET
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

        msg = '\xc2%s' % COMM_TEST
        print("Checking communication link...")
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)
        ret = self.dev.read(0x81, 1024, 5000)

        result = [hex(x) for x in ret]
        if result[1] == '0x1b' and result[2] == '0x79':
            print("Card reader connection is up and running.")
        else:
            sys.exit("MagWorks lost connection to the card reader.")


