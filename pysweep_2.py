#!/usr/bin/env python
import subprocess as sub
import time
import os
import re
import argparse

## Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Team Haxxor Kit', description ='Under Dev')
    parser.add_argument('ip', nargs=1, help='Choose ip to scan')
    parser.add_argument('--cidr', '-c', type=int, default=3, help='Select CIDR')

    args = parser.parse_args()

    ## Last digit(s) of IP Address are made replaceable with host numbers
    ippassed = args.ip[0]
    ipaddr = re.sub(r'(\d{1,3})$', '{}', ippassed)

    ## Associate CIPR argument with number of possible hosts
    hostnums = {
        24: 256,
        25: 128,
        26: 64,
        27: 32,
        28: 16,
        29: 8,
        30: 4, 
        31: 2,
    }

    ## If given CIPR is outside limits of Class C, default to 24
    original_cidr = args.cidr
    if(args.cidr > 23 and args.cidr < 32):
        max = hostnums[args.cidr]
    else:
        max = 256
        original_cidr = 24

    ## fping settings
    original_settings = ['fping', '-a', '-C 5', '-q']
    full_param = []
    temp = []
    ip = []
    elapsed_time = 0

    ## Helper Functions
     # Note: This should replace "form_it" function entirely, instead of coming after it
    def form_it():
        print('\nThe following hosts were found to be online and responding to ping requests:')
        print('\nDetected Hosts:')
        print('\n===============')
        for each in temp:
            print(each[0])
        elapsed_time = time.time() - start_time
        print('\n Total time to scan took:', elapsed_time, 'seconds')

        new_file = open('pingsweep-results.txt', 'w')
        new_file.write('PING SWEEP RESULTS\n')
        new_file.close()

        file = open('pingsweep-results.txt', 'a')
        file.write('\nThe following hosts were found to be online and responding to ping requests:\n')
        file.write('\nDetected Hosts:\n')
        file.write('===============\n')
        for each in temp:
            written = '\n {}'.format(each[0])
            file.write(written)
        totaltime = '\n\nTotal time to scan took: {} seconds'.format(elapsed_time)
        file.write(totaltime)
        file.close()
    
    def run_it():
        print('Detecting hosts...')
        for each in full_param:
            output = sub.run(each, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, encoding='utf-8')
            res = output.stderr.split(':')
            if(res[1].split(' ')[1] != '-'):
                temp.append(res)
        form_it()

    ## Main function uses ip address and prepares all possible host numbers to 
    def main():
        print('Currently checking for all host IP up to {}\n'.format(max), 'CIDR: /{}'.format(original_cidr))

        for num in range(0,max):
            ip.append(ipaddr.format(num))
        for each in ip:
            arg_copy = list(original_settings)
            arg_copy.append(each)
            full_param.append(arg_copy)
        run_it()

    start_time = time.time()
    main()
