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
        [regs.add(y) for y in instruction.args if Register.is_reg(y)]
        # also add registers to right of '=>' since they are read from
        [regs.add(y) for y in instruction.dest if Register.is_reg(y)]
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
        true_deps = find_true(instruction, program)
        anti_deps = find_anti(instruction, program)
        instruction.deps['true'] = true_deps
        # only add anti-deps that are not satisfied by true deps
        instruction.deps['anti'] = anti_deps.difference(true_deps)

        # add this instruction to the successor set of all dependencies
        for dep in true_deps.union(anti_deps):
            dep.successors.add(instruction)

def choose_ready(ready_set):
    """
    Helper function to choose next instruction to execute
    """
    max_priority = 0
    instruction = None
    for op in ready_set:
        print("op.schedule: "+str(op.schedule))
        if op.schedule == 0:
            if op.priority > max_priority:
                max_priority = op.priority
                instruction = op
    print("ready before remove: "+str([str(x) for x in ready_set]))
    ready_set.remove(instruction)
    print("ready after remove: "+str([str(x) for x in ready_set]))
    return instruction

def is_ready(op):
    """
    Returns True if op's dependencies have been executed, and op has not been scheduled yet,
    else returns False
    """
    if op.schedule != 0:
        return False
    for dep in op.get_all_deps():
        if dep.schedule <= 0:
            return False
    return True

def schedule(program):
    """
    Given a program that contains prioritized instructions and dependencies,
    schedules instructions according to the Local Forward List Scheduling
    algorithm. Returns a list of scheduled instructions
    """
    cycle  = 1
    ready  = set([x for x in program if x.get_all_deps() == set([])]) #leaves of the graph
    active = set([])
    
    while ready.union(active) != set([]):
        print("ready: "+ str([str(x) for x in ready]))
        print("active: "+ str([str(x) for x in active]))
        if ready != set([]):
            i = choose_ready(ready)
            i.schedule = cycle
            active.add(i)

        cycle = cycle + 1

        for op in active.copy(): # use copy() to allow change of active at runtime
            print(str(op.schedule + op.latency) + ' ' + str(cycle))
            if op.schedule + op.latency <= cycle:
                active.remove(op)
                for dep in op.successors:
                    if is_ready(dep):
                        ready.add(dep)

if __name__ == '__main__':
    program  = load(sys.stdin)
    build_dependencies(program)
    heuristic.llwp(program)
    #heuristic.highest_latency(program)
    schedule(program)
    for i in program:
        print str(i)
        sys.stdout.write("\ttrue: ")
        print([str(x) for x in i.deps['true']])
        sys.stdout.write("\tanti: ")
        print([str(x) for x in i.deps['anti']])
        print("\n")
    for i in program:
        print(str(i)+ ' ' + str(i.priority))

    print 
    for i in sorted(program, key=Instruction.get_schedule):
        print(str(i) + ' ' + str(i.schedule))
