#!/usr/bin/env python

import sys
import heuristic
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
    if instruction.op == 'nop':
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
        # add rmem when instruction reads from memory
        if instruction.is_mem_read():
            regs.add('rmem')
        else:
            [regs.add(y) for y in instruction.args if Register.is_reg(y)]
    elif dep_type == 'anti':
        # add rmem when instruction write to memory
        if instruction.is_mem_write():
            regs.add('rmem')
        else:
            [regs.add(x) for x in instruction.dest if Register.is_reg(x)]

    return regs

def dependent(dep_type, reg, instruction):
    """
    Checks if reg is dependent on completion of op based on
    dependency type. Returns True if dependent, else returns False
    """
    if dep_type == 'true':
        if reg in instruction.dest:
            return True
        elif reg == 'rmem':
            if instruction.is_mem_write():
                return True
    elif dep_type == 'anti':
        if reg in instruction.args:
            return True
        elif reg == 'rmem':
            if instruction.is_mem_read():
                return True
    return False


def find_true(instruction, program):
    """
    Searches for true dependencies for instruction in program. Returns
    a add of Instructions that instruction depends on
    
    true dep: b depends on a if a writes to a location that b later reads
    """
    deps = set([])
    for reg in select_regs('true', instruction):
        for op in reversed(program[:instruction.line]):
            if dependent('true', reg, op):
                deps.add(op)
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
        for op in reversed(program[:instruction.line]):
            if dependent('anti', reg, op):
                deps.add(op)
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

def choose_ready(program):
    """
    Helper function to choose next instruction to execute
    """
    i = max(program, key=Instruction.get_priority())
    program.remove(i)
    return i

def schedule(program):
    """
    Given a program that contains prioritized instructions and dependencies,
    schedules instructions according to the Local Forward List Scheduling
    algorithm. Returns a list of scheduled instructions
    """
    cycle  = 1
    ready  = set([x for x in program if x.deps['anti'].union(x.deps['true']) == set([])]) #leaves of the graph
    active = set([])
    
    while ready.union(active) != set([]):
        if ready != set([]):
            op = choose_ready(ready)
            
if __name__ == '__main__':
    program  = load(sys.stdin)
    build_dependencies(program)
    #heuristic.llwp(program)
    heuristic.highest_latency(program)
    for i in program:
        print str(i)
        sys.stdout.write("\ttrue: ")
        print([str(x) for x in i.deps['true']])
        sys.stdout.write("\tanti: ")
        print([str(x) for x in i.deps['anti']])
        print("\n")
    for i in program:
        print(str(i)+ ' ' + str(i.priority))
