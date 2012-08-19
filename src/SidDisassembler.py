
class AddressModes():
    ABSOLUTE = 0
    NULL_PAGE = 1
    DIRECT = 2
    INCLUSIVE = 3
    RELATIVE = 4
    INDIRECT = 5
    INDEXED = 6
    ABS_INDEXED = 7
    INDIR_INDEXED = 8

class Instruction():
    mnemonic = ""
    address = []

class SidDisassembler(object):

    def __init__(self):
        self.InstructionTypes = {
                0xAD : ["LDA", AddressModes.ABSOLUTE]
                        }
        self.NumOfBytes = {
                AddressModes.ABSOLUTE : 2
                        }

    def getInstructionAsAssembly(self, byte):
        return ""

    def disassembleInstruction(self, byte):
        return self.InstructionTypes[byte]

    def getAddrModeNumOfBytes(self, addrMode):
        return self.NumOfBytes[addrMode]

    def getBytesFromFile(self, numOfBytes):
        # TODO: do file handling
        if numOfBytes == 1:
            return [0xAD]
        elif numOfBytes == 2:
            return [0x01, 0x02]
        else:
            return [None]

    def getInstructionWithAddress(self):
        instrByte = self.getBytesFromFile(1)
        instrType = self.disassembleInstruction(instrByte[0])
        addrModeNumOfBytes = self.getAddrModeNumOfBytes(instrType[1])
        address = self.getBytesFromFile(addrModeNumOfBytes)
        instruction = self.makeInstruction(instrType, address)
        return instruction

    def makeInstruction(self, instrType, address):
        instruction = Instruction()
        instruction.mnemonic = instrType[0]
        instruction.address = address[::-1]     # addresses are in a reversed manner in the assembly list
        return instruction

