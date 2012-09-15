
import unittest
import os
from src.SidDisassembler import SidDisassembler
from src.SidCommon import AddressModes

class SidDisassemblerTest(unittest.TestCase):

    def setUp(self):
        self.testFileName = "testfile"
        self.sut = SidDisassembler()    # system under test
        self.createSidFile()
        self.testFile = file(self.testFileName, "rb")
        self.sut.setSidFile(self.testFile)

    def tearDown(self):
        self.deleteSidFile()

    def createSidFile(self):
        self.testFile = file(self.testFileName, "wb")
        for byte in range(0, 124):
            self.testFile.write("\x00")
        for byte in range(0, 2):
            self.testFile.write("\x88")
        self.testFile.write("\xad\x01\x02\x00")
        self.testFile.close()

    def deleteSidFile(self):
        self.testFile.close()
        os.remove(self.testFileName)

    def testAbsoluteAddressedLoadAccumulator(self):
        output = self.sut.disassembleInstruction(0xAD)
        self.assertEquals(output, ["LDA", AddressModes.ABSOLUTE])

    def testAbsoluteHasTwoByteAddress(self):
        numOfBytes = self.sut.getAddrModeNumOfBytes(AddressModes.ABSOLUTE)
        self.assertEquals(numOfBytes, 2)

    def testReadSidFile(self):
        self.assertEquals(len(self.sut.sidStruct.header), 124)
        self.assertEquals(len(self.sut.sidStruct.offset), 2)
        self.assertEquals(len(self.sut.sidStruct.data), 4)
        for byte in self.sut.sidStruct.header:
            self.assertEquals(byte, 0x00)
        for byte in self.sut.sidStruct.offset:
            self.assertEquals(byte, 0x88)

    def testGetBytesFromFile(self):
        self.sut.sidFile.seek(0)
        byte = self.sut.getBytesFromFile(1)
        twoBytes = self.sut.getBytesFromFile(2)
        self.assertEquals(len(byte), 1)
        self.assertEquals(len(twoBytes), 2)

    def testGetAnInstructionWithAddress(self):
        instr = self.sut.getNextInstruction()
        self.assertEquals(instr.mnemonic, "LDA")
        self.assertEquals(instr.address, [0x02, 0x01])

    def testInstructionComments(self):
        comment = self.sut.getCommentForMnemonic("LDA")
        self.assertEquals(comment, "Loads data from address into accumulator")

    def testGetInstructionAsAssembly(self):
        instruction = self.sut.getNextInstruction()
        asmCode = self.sut.getInstructionAsAssembly(instruction)
        self.assertEquals(asmCode, "LDA 02 01   ; Loads data from address into accumulator, addr: Absolute")

    def testImpliedAddressing(self):
        self.sut.getNextInstruction()
        ins = self.sut.getNextInstruction()
        self.assertEquals(ins.address, [])

    def testReadWholeFileAndGetAsm(self):
        printOutput = ""
        instruction = self.sut.getNextInstruction()
        while instruction:
            printOutput += self.sut.getInstructionAsAssembly(instruction) + "\n"
            instruction = self.sut.getNextInstruction()
        self.assertEquals(printOutput, "LDA 02 01   ; Loads data from address into accumulator, addr: Absolute\nBRK   ; Cause software interrupt, addr: Implied\n")

