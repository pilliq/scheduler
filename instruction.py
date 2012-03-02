#!/usr/bin/env python

latency = {'nop':1, 'addI':1, 'add':1, 'subI':1, 'sub':1, 'mult':3, 'div':3, 'load':5, 'loadI':1, 'loadAI':5, 'loadAO':5, 'store':5, 'storeAO':5, 'storeAI':5, 'output':1}

class Instruction():
    def __init__(self, instruction, line):
        """
        Given a string instruction and a line number, parses and creates a new Instruction object
        """
        parts        = [x.strip(',') for x in instruction.split()]
        self.line    = line
        self.op      = parts[0]
        self.latency = latency[self.op]
        self.args    = []
        self.dest    = []
        for i in parts[1:parts.index('=>')]:
            self.args.append(i)
        for j in parts[parts.index('=>')+1:]:
            self.dest.append(j)

    def __str__(self):
        s = self.op + ' '
        s = s + ', '.join(self.args)
        s = s + ' => '
        s = s + ', '.join(self.dest)
        return s
