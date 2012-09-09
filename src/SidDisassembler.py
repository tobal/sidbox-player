
import os
from src import LanguageData
from src.SidCommon import Instruction
from src.SidCommon import SidStruct

class SidDisassembler(object):

    def __init__(self):
        self.sidFile = None
        self.dataPointer = 0

        self.NumOfBytes = LanguageData.NumOfBytes
        self.InstructionTypes = LanguageData.InstructionTypes
        self.Comments = LanguageData.Comments

    def setSidFile(self, sidFile):
        self.sidFile = sidFile
        self.readSidFile()

    def readSidFile(self):
        self.sidStruct = SidStruct()
        self.sidStruct.header = self.getBytesFromFile(124)
        self.sidStruct.offset = self.getBytesFromFile(2)
        self.sidStruct.data = self.getBytesFromFileTillEnd()

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
        asmCode += ", addr: "
        asmCode += instruction.addressing
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

    def getBytesFromFileTillEnd(self):
        fileSize = os.path.getsize(self.sidFile.name)
        bytesToRead = fileSize - self.sidFile.tell()
        outputBytes = self.getBytesFromFile(bytesToRead)
        return outputBytes

    def getNextDataBytes(self, numOfBytes):
        pnt = self.dataPointer
        self.dataPointer += numOfBytes
        return self.sidStruct.data[pnt:pnt + numOfBytes]

    def getNextInstruction(self):
        instrByte = self.getNextDataBytes(1)
        instrType = self.disassembleInstruction(instrByte[0])
        addrModeNumOfBytes = self.getAddrModeNumOfBytes(instrType[1])
        address = self.getNextDataBytes(addrModeNumOfBytes)
        instruction = self.makeInstruction(instrType, address)
        return instruction

    def makeInstruction(self, instrType, address):
        instruction = Instruction()
        instruction.mnemonic = instrType[0]
        instruction.address = address[::-1]     # addresses are in a reversed manner in the assembly list
        instruction.comment = self.getCommentForMnemonic(instrType[0])
        instruction.addressing = instrType[1]
        return instruction

