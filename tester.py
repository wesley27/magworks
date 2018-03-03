from codes import *
import sys
import usb.core
import usb.util
import time

def test():
    dev = usb.core.find(idVendor = VENDOR_ID, idProduct = PRODUCT_ID)

    if dev is None:
        sys.exit("System was unable to find a magnetic card reader.")

    if dev.is_kernel_driver_active(0):
        try:
            dev.detach_kernel_driver(0)
            print("kernel driver detached")
        except usb.core.USBError as e:
            print(str(e))


    dev.set_configuration()
    dev.reset()

    for cfg in dev:
        sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
        for intf in cfg:
            sys.stdout.write('\t' + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting) + '\n')
            for ep in intf:
                sys.stdout.write('\t\t' + str(ep.bEndpointAddress) + '\n')

    alt = usb.util.find_descriptor(dev[0], find_all=True, bInterfaceNumber=0)
    for alts in alt:
        print(str(alt)+ '\n')

    
    #usb.util.claim_interface(dev, 0)
    #print("claimed device")

    msg = '\xc2%s' % LED_YELLOW
    assert dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

    time.sleep(2)

    msg = '\xc2%s' % LED_OFF
    assert dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

    msg = '\xc2%s' % COMM_TEST
    assert dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg) == len(msg)

    #
    ret = dev.read(0x81, 1024, 5000)
    #print(str(ret))
    print(str([hex(x) for x in ret]))
    #print((''.join([hex(x) for x in ret])).replace("0x", " "))

    """
    #resp = dev.read(0x81, 2048, 3000)
    #print(str(resp))

    #msg2 = '\xc2%' % LED_RED
    #assert len(dev.write((dev[0][(0, 0)][0]).bEndpointAddress, msg2), 5000) == len(msg2)
    
    resp = dev.read(0x81, 2048, 5000)
    print(str(resp))
    """

    ###
    """data = []
    swiped = False

    for bleh in range(5):
        try:
            if swiped:
                print(str(data))
                return

            data += dev.read((dev[0][(0, 0)][0]).bEndpointAddress, (dev[0][(0, 0)][0]).wMaxPacketSize, 5000)

            if len(data) >= 500:
                swiped = true
        except usb.core.USBError as e:
            print(str(e))
            continue"""

test()
