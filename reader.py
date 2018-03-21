import sys
import usb.core
import usb.util
import time

from codes import *
from parser import *

""" Class for handling all communication with the MSR Device. """
class Reader:
    
    """ Initialize the reader class. """
    def __init__(self, vid=VENDOR_ID, pid=PRODUCT_ID):
        self.vid = vid
        self.pid = pid

    """ Rest card reader interface. """
    def reset(self):
        msg = '\xc2%s' % RESET
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

    """ Test communication link with card reader. """
    def test_comms(self):
        self.reset()
        print('Checking communication link...')
        
        msg = '\xc2%s' % TEST_COMM
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

        try:
            ret = self.dev.read(0x81, 1024, 5000)
        except usb.core.USBError as e:
            self.reset()
            sys.exit('MagWorks lost connection to the card reader.')

        result = [hex(x) for x in ret]
        if result[1] == '0x1b' and result[2] == '0x79':
            print('\t\t...connection is up and running.\n')
        else:
            sys.exit('MagWorks lost connection to the card reader.')

    """ Test card reader sensor. """
    def test_sensor(self):
        self.reset()
        print('Testing card reading sensor...')
        msg = '\xc2%s' % TEST_SENSOR
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        print("Swipe card to test sensor.")

        try:
            ret = self.dev.read(0x81, 1024, 5000)
        except usb.core.USBError as e:
            self.reset()
            print('\t\t...sensor test timed out. (WARNING, reader may still work\n')
            return

        result = [hex(x) for x in ret]
        if result[1] == '0x1b' and result[2] == '0x30':
            print('\t\t...sensor test successful.\n')
        elif result[1] == '0x1b' and result[2] == '0x41':
            print('\t\t...sensor test failed. (WARNING, reader may still work)\n')
        else:
            sys.exit('Obtained unreadable result while testing the sensor.')

    """ Test card reader memory. """
    def test_ram(self):
        self.reset()
        print('Testing card reader memory...')
        msg = '\xc2%s' % TEST_RAM
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)

        try:
            ret = self.dev.read(0x81, 1024, 5000)
        except usb.core.USBError as e:
            self.reset()
            print('\t\t...memory test timed out. (WARNING, reader may still work.\n')
            return

        result = [hex(x) for x in ret]
        if result[1] == '0x1b' and result[2] == '0x30':
            print('\t\t...memory test successful.\n')
        elif result[1] == '0x1b' and result[2] == '0x41':
            print('\t\t...memory test failed. (WARNING, reader may still work)\n')
        else:
            sys.exit('Obtained unreadable result while testing memory.')

    """ Test card reader LEDs """
    def test_leds(self):
        self.reset()
        print('Testing LEDs...')

        print('\t\t...disabling all LEDs.')
        msg = '\xc2%s' % LED_OFF
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        time.sleep(1.5)

        print('\t\t...testing green LED.')
        msg = '\xc2%s' % LED_GREEN
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        time.sleep(1.5)

        print('\t\t...testing yellow(and green) LED.')
        msg = '\xc2%s' % LED_YELLOW
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        time.sleep(1.5)

        print('\t\t...testing red LED.')
        msg = '\xc2%s' % LED_RED
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        time.sleep(1.5)

        print('\t\t...testing all LEDs.')
        msg = '\xc2%s' % LED_ON
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        time.sleep(1.25)

        print('\t\t...re-enabling green LED.')
        msg = '\xc2%s' % LED_GREEN
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        
        print('Test complete.')    

    """ Read card with ISO format. Param is timeout checker."""
    def read_ISO(self, iters):
        self.reset()
        msg = '\xc2%s' % READ_ISO
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

        if iters == 0:
            print('Please swipe your card.\n')
        elif iters == 10:
            print('Operation is about to timeout.\n')
        elif iters >= 15:
            self.reset()
            print('Operation timed out.\n')
            return
        
        try:
            data = self.dev.read(0x81, 1024, 500)
        except usb.core.USBError as e:
            if str(e) == ('[Errno 110] Operation timed out'):
                return self.read_ISO(iters+1)
            else:
                self.reset()
                sys.exit('Read operation failed: %s' % str(e))

        #TODO Check on return bytes for better parsing/handling read errors
        parse_ISO(data)
        #self.reset()

    """ Erase card data. """
    def erase(self, track, iters):
        self.reset()
        msg = '\xc2%s%s' % (ERASE_CARD, track)
        assert self.dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

        if iters == 0:
            print('Please swipe your card.\n')
        elif iters == 10:
            print('Operation is about to timeout.\n')
        elif iters >= 15:
            self.reset()
            print('Operation timed out.\n')
            return

        try:
            ret = self.dev.read(0x81, 1024, 500)
        except usb.core.USBError as e:
            if str(e) == ('[Errno 110] Operation timed out'):
                return self.erase(track, iters+1)
            else:
                self.reset()
                sys.exit('...Erase operation failed: %s' % str(e))

        result = [hex(x) for x in ret]
        print(str(result))

        if result[1] == '0x1b' and result[2] == '0x30':
            print('\t\t...card data successfully erased.\n')
        elif result[1] == '0x1b' and result[2] == '0x41':
            print('\t\t...failed to erase card data.\n')
        else:
            sys.exit('Obtained invalid response while attempted to delete card data.\n')

    """ Obtain msr device model. """
    def get_model(self):
        self.reset()
        print('Obtaining device information...')
        msg = '\xc2%s' % GET_MODEL
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        
        try:
            ret = self.dev.read(0x81, 1024, 3000)
        except usb.core.USBError as e:
            self.reset()
            print('\t\t...device request timed out.')
            return

        result = [hex(x).replace('0x', '') for x in ret]
        print(str(result)) #TODO clean this up

    """ Obtain msr device firmware version. """
    def get_firmware(self):
        self.reset()
        print('Obtaining device information...')
        msg = '\xc2%s' % GET_FIRMWARE
        assert self.dev.ctrl_transfer(0x21, 9, 0x300, 0, msg) == len(msg)
        
        try:
            ret = self.dev.read(0x81, 1024, 3000)
        except usb.core.USBError as e:
            self.reset()
            print('\t\t...device request timed out.')
            return

        result = [hex(x).replace('0x', '') for x in ret]
        print(str(result)) #TODO clean this up

        
    """ Initialize the device and claim it."""
    def claim_reader(self):
        print('Locating device...')
        self.dev = usb.core.find(idVendor = self.vid, idProduct = self.pid)

        # ensure msr exists
        if self.dev is None:
            sys.exit('\t\t...failed to locate a magnetic stripe reader. Exiting.')
        print('\t\t...magnetic stripe reader found.')

        # disable any existing drivers
        print('Searching for active drivers...')
        if self.dev.is_kernel_driver_active(0):
            try:
                self.dev.detach_kernel_driver(0)
                print('\t\t...detached existing kernel driver.')
            except usb.core.USBError as e:
                sys.exit('\t\t...failed to detach an existing kernel driver: %s' % str(e))
        else:
            print('\t\t...no active drivers found.')

        # set up msr configuration
        print('Configuring USB device...')
        try:
            self.dev.set_configuration()
            self.dev.reset()
        except usb.core.USBError as e:
            sys.exit('\t\t...failed to set device configuration: %s' % str(e))
        print('\t\t...set device configuration.\n')
