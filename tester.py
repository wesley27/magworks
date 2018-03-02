from codes import *
import sys
import usb.core


def test():
    dev = usb.core.find(idVendor = VENDOR_ID, idProduct = PRODUCT_ID)

    if dev is None:
        sys.exit("System was unable to find a magnetic card reader.")

    #TESTING STUFF HERE
    for cfg in dev:
        sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
        for intf in cfg:
            sys.stdout.write('\t' + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting) + '\n')
            for ep in intf:
                sys.stdout.write('\t\t' + str(ep.bEndpointAddress) + '\n')
    #TESTING STUFF HERE

test()
