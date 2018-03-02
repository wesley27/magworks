# Read/Write Codes
READ_ISO = '\x1b\x72'
READ_RAW = '\x1b\x6d'
WRITE_ISO = '\x1b\x77'
WRITE_RAW = '\x1b\x6e'

# Misc Card Codes
ERASE_CARD = '\x1b\x63'
SELECT_BPI = '\x1b\x62' #this is different for each track
SET_BPC = '\x1b\x6f'
SET_HICO = '\x1b\x78'
SET_LOCO = '\x1b\x79'
GET_CO_STATUS = '\x1b\x64'

# Leading Zero Codes
LZERO_CHECK = '\x1b\x7a'
LZERO_SET = '\x1b\x6c'

# LED Codes
LED_OFF = '\x1b\x81'
LED_ON = '\x1b\x82'
LED_GREEN = '\x1b\x83'
LED_YELLOW = '\x1b\x84'
LED_RED = '\x1b\x85'

# MSR 206 Misc Codes
RESET = '\x1b\x61'
COMM_TEST = '\x1b\x65'
SENSOR_TEST = '\x1b\x86'
RAM_TEST = '\x1b\x87'
GET_MODEL = '\x1b\x74'
GET_FIRMWARE = '\x1b\x76'

# USB Identification
VENDOR_ID = 0x0801
PRODUCT_ID = 0x0003
