#!/usr/bin/env python

import sys

latency = {'nop':1, 'addI':1, 'add':1, 'subI':1, 'sub':1, 'mult':3, 'div':3, 'load':5, 'loadI':1, 'loadAO':5, 'store':5, 'storeAO':5, 'storeAI':5, 'output':1}

body = []

if __name__ == '__main__':
    for line in sys.stdin:
	body.append([x.strip(',') for x in line.split()])
    print body
    for i in latency:
	print(i+'\t: '+str(latency[i]))
