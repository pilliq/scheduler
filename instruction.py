latencies = {
        'nop': 1, 
        'addI': 1, 
        'add': 1, 
        'subI': 1, 
        'sub': 1, 
        'mult': 3, 
        'div': 3, 
        'load': 5, 
        'loadI': 1, 
        'loadAI': 5, 
        'loadAO': 5, 
        'store': 5, 
        'storeAO': 5, 
        'storeAI': 5, 
        'output': 1
        }

class Instruction(object):
    """
    Represents Instructions, and gives information about certain instructions
    """
    def __init__(self, instruction, line):
        """
        Given a string instruction and a line number, parses and creates a new Instruction object
        """
        parts           = [x.strip(',') for x in instruction.split()]
        self.line       = line
        self.op         = parts[0]
        self.latency    = latencies[self.op]
        self.deps       = {'true':set([]), 'anti':set([])}
        self.successors = set([])
        self.priority   = 0
        self.schedule   = 0
        self.args       = []
        self.dest       = []

        if self.op == 'nop': 
            return
        if self.op == 'output':
            self.args.append(parts[1])
            return

        # add each arg and dest arguments
        for i in parts[1:parts.index('=>')]:
            self.args.append(i)
        for j in parts[parts.index('=>')+1:]:
            self.dest.append(j)

    def __str__(self):
        if self.op == 'nop':
            return self.op
        if self.op == 'output':
            return self.op + ' ' + ' '.join(self.args)
        s = self.op + ' '
        s = s + ', '.join(self.args)
        s = s + ' => '
        s = s + ', '.join(self.dest)
        return s

    def get_all_deps(self):
        """
        Returns a set of both true and anti dependencies
        """
        return self.deps['true'].union(self.deps['anti'])

    def is_mem_write(self):
        """
        Returns True if instruction writes to memory, else returns False
        """
        if self.op in set(['store', 'storeAI', 'storeAO']):
            return True
        return False

    def is_mem_read(self):
        """
        Returns True if instruction reads from memory, else returns False
        """
        if self.op in set(['load', 'loadAI', 'loadAO', 'output']):
            return True
        return False
    
    # static methods used for sort functions

    @staticmethod
    def get_priority(instruction):
        return instruction.priority

    @staticmethod
    def get_schedule(instruction):
        return instruction.schedule

    @staticmethod
    def get_latency(instruction):
        return instruction.latency
