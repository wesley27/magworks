import argparse
from reader import *

version = '0.0.1'

def cli():
    parser = argparse.ArgumentParser(prog='magworks', description='A command-line tool for intefacing MSR devices.(MSR206/MSR605/MSR605X/MSR606)', epilog='Operational arguments (such as -r, read) must be used individually, and will be processed in the order they appear below.')
    
    parser.add_argument('-r', choices=['iso', 'raw'], help='read data from a magnetic stripe card')
    parser.add_argument('-t', choices=['conn', 'sensor', 'ram'], help='test connection and msr device')
    parser.add_argument('-v', action='version', version='%(prog)s v' + version, help='display %(prog)s version')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args()

def main():
    args = vars(cli())
    #print(args)
    
    msr = Reader()
    msr.claim_reader()

    if args['r'] is not None:
        msr.read_ISO(0) if args['r'] == 'iso' else msr.read_RAW(0)
    
    elif args['t'] is not None:
        msr.test_comms() if args['t'] == 'conn' else msr.test_sensor() if args['t'] == 'sensor' else msr.test_ram()



main()
