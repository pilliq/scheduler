class Register(object):
    """
    Register methods
    """
    @staticmethod
    def is_reg(s):
        """
        Returns True if s is the name of a valid register, else returns False
        """
        if s[0] == 'r':
            try:
                int(s[1:])
                return True
            except ValueError:
                return False
        return False
