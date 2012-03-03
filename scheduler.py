#!/usr/bin/env python

import sys
from graph import Node
from mem import Register, Memory
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
        num += 1
    return instructions

def special(instruction):
    """
    Returns True if instruction cannot have dependencies, else returns False
    """
    if instruction.op == 'nop' or instruction.op == 'output':
        return True
    else:
        return False

def select_regs(dep_type, instruction):
    """
    Helper function to decide which registers need to be checked for 
    dependencies based on dependency type. Returns a set of registers 
    to be checked
    """
    regs = set([])
    if dep_type == 'true':
        # If a mem write op, add regs to right of '=>' since they are read 
        # from and not written to
        if instruction.is_mem_write():
            [regs.add(x) for x in instruction.dest if Register.is_reg(x)]
        [regs.add(y) for y in instruction.args if Register.is_reg(y)]
    elif dep_type == 'anti':
        # dependent if reg appears in dest. not dependendent if instruction
        # is a mem write operation since regs in dest are not written to
        if instruction.is_mem_write():
            pass
        else:
            [regs.add(x) for x in instruction.dest if Register.is_reg(x)]

    return regs

def find_true(instruction, program):
    """
    Searches for true dependencies for instruction in program. Returns
    a add of Instructions that instruction depends on
    
    true dep: b depends on a if a writes to a location that b later reads
    """
    deps = set([])
    for reg in select_regs('true', instruction):
        for inst in reversed(program[:instruction.line]):
            #dependent if reg appears in dest, and the instruction doesn't write to mem
            if reg in inst.dest and not inst.is_mem_write(): 
                deps.add(inst)
                break
    return deps

def find_anti(instruction, program):
    """
    Searches for anti dependencies for instruction in program. Returns
    a set of Instructions that instruction depends on

    anti dep: b depends on a if a reads a location that b later writes 
    """
    deps = set([])
    for reg in select_regs('anti', instruction):
        for inst in reversed(program[:instruction.line]):
            if reg in inst.args:
                deps.add(inst)
                break
            elif inst.is_mem_write():
                if reg in inst.dest:
                    deps.add(inst)
                    break
    return deps

def build_dependencies(program):
    """
    Builds a dependency graph out of a list of Instructions. 
    """
    done = []
    for instruction in reversed(program):
        if special(instruction):
            continue
        instruction.deps['true'] = find_true(instruction, program)
        # only add anti-deps that are not satisfied by true deps
        instruction.deps['anti'] = find_anti(instruction, program).difference(instruction.deps['true'])

if __name__ == '__main__':
    program  = load(sys.stdin)
    build_dependencies(program)
    for i in program:
        print str(i)
        sys.stdout.write("\ttrue: ")
        print([str(x) for x in i.deps['true']])
        sys.stdout.write("\tanti: ")
        print([str(x) for x in i.deps['anti']])
        print("\n")
