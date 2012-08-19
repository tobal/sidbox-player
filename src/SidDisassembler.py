
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
    comment = ""

class SidDisassembler(object):

    def __init__(self):
        self.InstructionTypes = {
                0xAD : ["LDA", AddressModes.ABSOLUTE]
                        }

        self.NumOfBytes = {
                AddressModes.ABSOLUTE : 2
                        }

        self.Comments = {
                "LDA" : "Loads data from address into accumulator"
                        }

    def getInstructionAsAssembly(self, instruction):
        asmCode = instruction.mnemonic
        asmCode += " "
        for byte in instruction.address:
            asmCode += self.intToHexa(byte)
            asmCode += " "
        asmCode += "  ; "
        asmCode += instruction.comment
        return asmCode

    def intToHexa(self, integer):
        if integer > 0xFF:
            integer = 0xFF
        hexa = hex(integer)
        if(len(hexa) == 3):
            output = "0" + hexa[2]
        else:
            output = hexa[2:]
        return output

    def disassembleInstruction(self, byte):
        return self.InstructionTypes[byte]

    def getAddrModeNumOfBytes(self, addrMode):
        return self.NumOfBytes[addrMode]

    def getCommentForMnemonic(self, mnemonic):
        return self.Comments[mnemonic]

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
        instruction.comment = self.getCommentForMnemonic(instrType[0])
        return instruction

