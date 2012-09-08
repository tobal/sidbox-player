
class AddressModes():
    ABSOLUTE = "Absolute"
    ZERO_PAGE = "Zero page"
    ZERO_PAGE_X = "Zero page with X"
    ZERO_PAGE_Y = "Zero page with Y"
    ACCUMULATOR = "Accumulator"
    IMMEDIATE = "Immediate"
    INDIRECT_X = "Indirect with X"
    INDIRECT_Y = "Indirect with Y"
    INDEXED_X = "Indexed with X"
    INDEXED_Y = "Indexed with Y"
    RELATIVE = "Relative"
    IMPLIED = "Implied"

class Instruction():
    mnemonic = ""
    address = []
    comment = ""

class SidDisassembler(object):

    def __init__(self):
        self.sidFile = None

        self.NumOfBytes = {
                AddressModes.ABSOLUTE : 2,
                AddressModes.ZERO_PAGE : 1,
                AddressModes.ZERO_PAGE_X : 1,
                AddressModes.ZERO_PAGE_Y : 1,
                AddressModes.ACCUMULATOR : 0,
                AddressModes.IMMEDIATE : 1,
                AddressModes.INDIRECT_X : 1,
                AddressModes.INDIRECT_Y : 1,
                AddressModes.INDEXED_X : 2,
                AddressModes.INDEXED_Y : 2,
                AddressModes.RELATIVE : 1,
                AddressModes.IMPLIED : 0
                        }

        self.InstructionTypes = {
                0x00 : ["BRK", AddressModes.IMPLIED],
                0xAD : ["LDA", AddressModes.ABSOLUTE],
                        }

        self.Comments = {
                "LDA" : "Loads data from address into accumulator",
                "LDX" : "Loads data from address into X register",
                "LDY" : "Loads data from address into Y register",
                "STA" : "Stores data from accumulator to address",
                "STX" : "Stores data from X register to address",
                "STY" : "Stores data from Y register to address",
                "INC" : "Increments the addressed data by one",
                "DEC" : "Decrements the addressed data by one",
                "TAX" : "Loads data from accumulator to X register",
                "TAY" : "Loads data from accumulator to Y register",
                "TXA" : "Loads data from X register to accumulator",
                "TYA" : "Loads data from Y register to accumulator",
                "TXS" : "Loads data from X register to stack pointer",
                "TSX" : "Loads data from stack pointer to X register",
                "SEC" : "Sets the carry bit to high",
                "SED" : "Sets decimal-mode bit to high",
                "CLC" : "Clears the carry bit",
                "CLD" : "Clears the decimal-mode bit",
                "CLV" : "Clears the overflow bit",
                "CLI" : "Clears the interrupt bit (enables maskable interrupts)",
                "SEI" : "Sets the interrupt bit to high (disables maskable interrupts)",
                "DEX" : "Decrements the value of X register by one",
                "DEY" : "Decrements the value of Y register by one",
                "INX" : "Increments the value of X register by one",
                "INY" : "Increments the value of Y register by one",
                "JMP" : "Sets the instruction pointer to given address",
                "JSR" : "Calls a subroutine",
                "RTS" : "Returns from a subroutine",
                "RTI" : "Returns from an interrupt-handler",
                "BRK" : "Cause software interrupt",
                "BCC" : "The operand is added to the value of the instruction pointer (loops), if carry-bit is cleared",
                "BCS" : "The operand is added to the value of the instruction pointer (loops), if carry-bit is set",
                "BNE" : "The operand is added to the value of the instruction pointer (loops), if null-bit is cleared",
                "BEQ" : "The operand is added to the value of the instruction pointer (loops), if null-bit is set",
                "BPL" : "The operand is added to the value of the instruction pointer (loops), if negative-bit is cleared",
                "BMI" : "The operand is added to the value of the instruction pointer (loops), if negative-bit is set",
                "BVC" : "The operand is added to the value of the instruction pointer (loops), if overflow-bit is cleared",
                "BVS" : "The operand is added to the value of the instruction pointer (loops), if overflow-bit is set",
                "PHA" : "Push to stack from accumulator",
                "PLA" : "Pop from stack to accumulator",
                "PHP" : "Push stateregister to stack",
                "PLP" : "Pop stateregister from stack",
                "ASL" : "Bitwise step to left (lowest bit will be zero)",
                "ROL" : "Bitwise step to left (lowest bit comes from carry bit)",
                "ASR" : "Bitwise step to right (highest bit will be zero)",
                "ROR" : "Bitwise step to right (highest bit comes from carry bit)",
                "AND" : "Bitwise AND between accumulator and addressed byte",
                "ORA" : "Bitwise OR between accumulator and addressed byte",
                "EOR" : "Bitwise XOR between accumulator and addressed byte",
                "BIT" : "Bitwise AND between accumulator and addressed byte (result not loaded into accumulator)",
                "ADC" : "Add instruction (accumulator = accumulator + specific_byte + carry_bit)",
                "SBC" : "Subtract instruction",
                "CMP" : "Compares accumulator with specific byte (acc - byte)",
                "CPX" : "Compares X register with specific byte (X - byte)",
                "CPY" : "Compares Y register with specific byte (Y - byte)",
                "NOP" : "No operation"
                        }

    def setSidFile(self, sidFile):
        self.sidFile = sidFile

    def disassembleInstruction(self, byte):
        return self.InstructionTypes[byte]

    def getAddrModeNumOfBytes(self, addrMode):
        return self.NumOfBytes[addrMode]

    def getCommentForMnemonic(self, mnemonic):
        return self.Comments[mnemonic]

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

    def getBytesFromFile(self, numOfBytes):
        bytesAsString = self.sidFile.read(numOfBytes)
        outputBytes = []
        for char in bytesAsString:
            outputBytes.append(ord(char))
        return outputBytes

    def getNextInstruction(self):
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

