class Heuristic(object):
    """
    Base class for priority assignment heuristics
    """
    @staticmethod
    def run():
        pass

class LLWP(Heuristic):
    """
    Longest latency-weighted path heuristic. Assigns higher priority to 
    the instruction with the highest latency on the critical path.
    """
    @staticmethod
    def run(program):
        return self.llwp(program)
    
    def llwp(program, weight=0):
        """
        Recursive depth first traversal of dependence graph which 
        assigns priorities as it see instructions.
        """
        for instruction in reversed(program):
            if instruction.priority == 0:
                self._llwp_h(instruction)
                    
    def _llwp_h(instruction, weight=0):
        """
        Helper function for llwp()
        """
        priority = instruction.latency + weight
        instruction.priority = priority
        deps = instruction.deps['true'].union(instruction.deps['anti'])
        for dep in deps:
            if dep.priority == 0:
                self._llwp_h(dep, priority)
        
class HighestLatency(Heuristic):
    """
    Assigns a higher priority for instructions with highest latency
    """
    @staticmethod
    def run(program):
        raise
