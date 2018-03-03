import sys
import usb.core
import usb.util
import codecs

from codes import *

class Reader:
    
    """ Initialize the reader class. """
    def __init__(self):
        self.vid = VENDOR_ID
        self.pid = PRODUCT_ID

    """ Rest card reader interface. """
    def reset(self):
        msg = '\xc2%s' % RESET
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

    """ Test communication link with car reader. """
    def test_comms(self):
        self.reset()
        print("Checking communication link...")
        
        msg = '\xc2%s' % TEST_COMM
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)
        ret = self.dev.read(0x81, 1024, 5000)
        result = [hex(x) for x in ret]

        if result[1] == '0x1b' and result[2] == '0x79':
            print("Card reader connection is up and running.")
        else:
            sys.exit("MagWorks lost connection to the card reader.")
        

    """ Read card with ISO format. """
    def read_ISO(self):
        self.reset()

        msg = '\xc2%s' % READ_ISO
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

        print("Waiting to process swipe...")
        ret = self.dev.read(0x81, 1024, 3000)
        result = [hex(x).replace('0x', '') for x in ret]
        print(str(result))

        i = 0
        s = ''
        for h in result:
            if i >= 5 and i < len(result)-1:
                s += h
            i += 1
        print(s.decode("hex"))

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

        self.test_comms()
