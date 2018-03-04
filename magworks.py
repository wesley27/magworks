import argparse
from reader import *

version = '0.0.1'

def cli():
    parser = argparse.ArgumentParser(prog='magworks', description='A command-line tool for intefacing MSR devices.(MSR206/MSR605/MSR605X/MSR606)', epilog='Operational arguments (such as -r, read) must be used individually, and will be processed in the order they appear below.')
    
    parser.add_argument('-r', choices=['iso', 'raw'], help='read data from a magnetic stripe card')
    parser.add_argument('-w', choices=['iso', 'raw'], help='write data to a magnetic stripe card')
    parser.add_argument('-e', action='store_true', help='erase data from a magnetic stripe card')
    parser.add_argument('-t', choices=['conn', 'sensor', 'ram', 'led'], help='test connection and msr device')
    parser.add_argument('-m', action='store_true', help='get model of msr device')
    parser.add_argument('-f', action='store_true', help='get firmware version of msr device')
    parser.add_argument('-v', action='version', version='%(prog)s v' + version, help='display %(prog)s version')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args()

def main():
    args = cli()
    #print(args.e)
    
    msr = Reader()
    msr.claim_reader()

    if args.r is not None:
        msr.read_ISO(0) if (args.r == 'iso') else msr.read_raw(0)
    
    elif args.w is not None:
        print('This operation does not exist yet!')

    elif args.e is not False:
        print('This operation does not exist yet!')
    
    elif args.t is not None:
        msr.test_comms() if args.t == 'conn' else msr.test_sensor() if args.t == 'sensor' else msr.test_ram() if args.t == 'ram' else msr.test_leds()

    elif args.m is not False:
        msr.get_model()

    elif args.f is not False:
        msr.get_firmware()

main()
