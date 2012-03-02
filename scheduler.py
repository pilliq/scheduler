#!/usr/bin/env python

import sys
from graph import Node
from instruction import Instruction

def load(f):
    """
    Loads instructions from file f into instructions and returns
    a list of instructions. f must be an opened file and caller is
    responsible for closing f. 
    """
    num = 0 
    instructions = []
    for line in f:
        instructions.append(Instruction(line, num))
    return instructions

def build_dependencies(instructions):
    """
    Builds a dependency graph out of a list of Instructions. 
    Returns a list of Nodes with dependencies built in as parents
    """
    pass
