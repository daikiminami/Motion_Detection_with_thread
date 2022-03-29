import sys
import concurrent.futures
import time

from cap_data import CapData

def main(argc, argv):
    cap_data = CapData(argc - 1, argv[1:])

    cap_data.cap_function()



if __name__ == '__main__':
    argv = sys.argv
    print('Start main')
    main(len(argv), argv)
    print('End main')