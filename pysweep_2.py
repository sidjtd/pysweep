#!/usr/bin/env python
import subprocess

ipaddr = '10.0.2.{}'
iplist = []
call_arg = ['fping', '-a', '-C 5', '-q']
bash_args = []
temp = []

def run_it():
    for each_set in bash_args:
        res = subprocess.run(each_set, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        splitten = res.stderr.split(':')
        if(splitten[1].split(' ')[1] != '-'):
             temp.append(splitten)
    print(temp)

def main():
    for num in range(0,6):
        iplist.append(ipaddr.format(num))

    for each_ip in iplist:
        call_copy = list(call_arg)
        call_copy.append(each_ip)
        bash_args.append(call_copy)
    run_it()

main()
