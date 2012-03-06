import random
from instruction import Instruction

def llwp(program, weight=0):
    """
    Longest latency-weighted path heuristic. Assigns higher priority to 
    the instruction with the highest latency on the critical path.
    A recursive depth first traversal of dependence graph which 
    assigns priorities as it see instructions.
    """
    for instruction in reversed(program):
        if instruction.priority == 0:
            _llwp_h(instruction)

def _llwp_h(instruction, weight=0):
    """
    Helper function for llwp()
    """
    priority = instruction.latency + weight
    instruction.priority = priority
    deps = instruction.deps['true'].union(instruction.deps['anti'])
    for dep in deps:
        if dep.priority == 0:
            _llwp_h(dep, priority)

def highest_latency(program):
    """
    Assigns a higher priority for instructions with highest latency.
    Recursive breadth traversal of dependence graph.
    """
    for instruction in reversed(program):
        if instruction.priority == 0:
            _highest_latency_h(instruction)

def _highest_latency_h(instruction, seq=0, choices=None):
    """
    Helper function for highest_latency()
    """
    priority = seq+1
    instruction.priority = priority
    deps = instruction.deps['true'].union(instruction.deps['anti'])
    if choices:
        deps = deps.union(choices)
    if not deps:
        return
    d = max(deps, key=Instruction.get_latency)
    deps.remove(d)  
    _highest_latency_h(d, priority, deps)

def rand(program):
    """
    Assigns random priority to instructions
    """
    random.seed(None) #seed with current system time
    num_ops = len(program)
    for instruction in program:
        instruction.priority = random.randint(1,num_ops)
