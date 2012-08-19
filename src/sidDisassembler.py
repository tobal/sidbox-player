
class AddressModes():
    ABSOLUTE = 0
    NULL_PAGE = 1
    DIRECT = 2
    INCLUSIVE = 3
    RELATIVE = 4
    INDIRECT = 5
    INDEXED = 6
    ABS_INDEXED = 7
    INDIR_INDEXED =8

class SidDisassembler(object):

    def __init__(self):
        pass

    def getInstructionAsAssembly(self, byte):
        pass

    def disassembleInstruction(self, byte):
        return "LDA"

