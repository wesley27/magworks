from reader import *

def main():
    msr = Reader()
    msr.claim_reader()
    print('\n')
    msr.read_ISO()

main()
