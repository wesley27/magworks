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

    """ Parse ISO card data. """
    def parse_ISO(self, data):
        result = [hex(x).replace('0x', '') for x in data]

        ### TRACK 1 (IATA) ###
        # Start sentinal always begins on index 5, card data on 6
        fcode = codecs.decode(''.join(result[6:7]), 'hex')
        
        #iterator to keep track of current index of result
        start = current = 7

        for h in result[start:]:
            if h == '5e': # field separator value
                break
            current += 1

        pan = codecs.decode(''.join(result[start:current]), 'hex')
        
        if pan[:2] == '59': # requires country code
            cc = codecs.decode(''.join(result[current+1:current+4]), 'hex')
            current += 4
        else:
            cc = 'N/A'
            current += 1

        start = current
        for h in result[start:]:
            if h == '5e': # field separator value
                break
            current += 1

        ch = codecs.decode(''.join(result[start:current]), 'hex').replace('/', ', ')

        current += 1

        if result[current:current+1][0] == '5e': # no expiration date
            ed = 'N/A'
            current += 1
        else:
            ed = codecs.decode(''.join(result[current+2:current+4]), 'hex') + '/' + codecs.decode(''.join(result[current:current+2]), 'hex')
            current += 4

        if result[current:current+3][0] == '5e': # no service code
            sc = 'N/A'
            current += 1
        else:
            sc = codecs.decode(''.join(result[current:current+3]), 'hex')
            current += 3

        if result[current:current+1][0] == '30': # no PVV
            pv = 'N/A'
        else:
            pv = codecs.decode(''.join(result[current+1:current+5]), 'hex')
        current += 5

        if result[current:current+1][0] == '1b': # track 2 starts for gift cards
            dd = 'N/A'
        else:
            start = current
            for h in result[start:]:
                if h == '3f':
                    break
                current += 1

            dd = codecs.decode(''.join(result[start:current]), 'hex')

        card_data = []
        card_data.append('Track 1:')
        card_data.append('  Format Code:\t\t' + fcode)
        card_data.append('  Country Code:\t\t' + cc)
        card_data.append('  Primary Account #:\t' + pan)
        card_data.append('  Card Holder:\t\t' + ch)
        card_data.append('  Expiration Date:\t' + ed)
        card_data.append('  Service Code:\t\t' + sc)#TODO add service code description
        card_data.append('  PVV:\t\t\t' + pv)
        card_data.append('  Discretionary:\t' + dd)

        ### Track 2 (ABA) ###
        start = current
        for h in result[start:]:
            if h == '3b':
                current += 1
                break
            current += 1

        start = current
        for h in result[start:]:
            if h == '3d': # field separator
                break
            current += 1

        pan = codecs.decode(''.join(result[start:current]), 'hex')

        if pan[:2] == '59': # requires country code
            cc == codecs.decode(''.join(result[current+1:current+4]), 'hex')
            current += 4
        else:
            cc = 'N/A'
            current += 1

        if result[current:current+1][0] == '3d': # no expirationd date
            ed = 'N/A'
            current += 1
        else:
            ed = codecs.decode(''.join(result[current+2:current+4]), 'hex') + '/' + codecs.decode(''.join(result[current:current+2]), 'hex')
            current += 4

        if result[current:current+3][0] == '3d': # no service code
            sc = 'N/A'
            current += 1
        else:
            sc = codecs.decode(''.join(result[current:current+3]), 'hex')
            current += 3

        if result[current:current+1][0] == '30': #no PVV
            pv = 'N/A'
        else:
            pv = codecs.decode(''.join(result[current+1:current+5]), 'hex')
        current += 5

        start = current
        for h in result[start:]:
            if h == '3f':
                break
            current += 1

        dd = codecs.decode(''.join(result[start:current]), 'hex')

        card_data.append('Track 2:')
        card_data.append('  Country Code:\t\t' + cc)
        card_data.append('  Primary Account #:\t' + pan)
        card_data.append('  Expiration Date:\t' + ed)
        card_data.append('  Service Code:\t\t' + sc)
        card_data.append('  PVV:\t\t\t' + pv)
        card_data.append('  Discretionary:\t' + dd)

        for v in card_data:
            print(v)

        if current < len(result):
            print('Track 3:\n  This track has proprietary encoding from the issuer.')

        

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

        self.parse_ISO(data)

        
    """ Initialize the device and claim it."""
    def claim_reader(self):
        print('Initializing MagWorks...')
        self.dev = usb.core.find(idVendor = self.vid, idProduct = self.pid)

        # ensure msr exists
        if self.dev is None:
            sys.exit('MagWorks could not find any card readers.')
        print('\t\t...located card reader.')

        # disable any existing drivers
        if self.dev.is_kernel_driver_active(0):
            try:
                self.dev.detach_kernel_driver(0)
                print('\t\t...detached existing kernel driver.')
            except usb.core.USBError as e:
                sys.exit('MagWorks was unable to detach the existing kernel driver: %s' % str(e))

        # set up msr configuration
        try:
            self.dev.set_configuration()
            self.dev.reset()
        except usb.core.USBError as e:
            sys.exit('MagWorks failed to set the MSR configuration: %s' % str(e))
        print('\t\t...set card reader configuration.\n')

        self.test_comms()
        #self.test_sensor()
        #self.test_ram()
