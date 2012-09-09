
import unittest
import os
from src.SidDisassembler import SidDisassembler
from src.SidCommon import AddressModes

class SidDisassemblerTest(unittest.TestCase):

    def setUp(self):
        self.testFileName = "testfile"
        self.testSidFileName = "testsidfile"
        self.sut = SidDisassembler()    # system under test
        self.writeTestfile()
        self.testFile = file(self.testFileName, "rb")
        self.sut.setSidFile(self.testFile)

    def tearDown(self):
        self.testFile.close()
        os.remove(self.testFileName)

    def writeTestfile(self):
        testFile = file(self.testFileName, "wb")
        testFile.write("\xad\x01\x02\x00\x02")
        testFile.close()

    def testAbsoluteAddressedLoadAccumulator(self):
        output = self.sut.disassembleInstruction(0xAD)
        self.assertEquals(output, ["LDA", AddressModes.ABSOLUTE])

    def testAbsoluteHasTwoByteAddress(self):
        numOfBytes = self.sut.getAddrModeNumOfBytes(AddressModes.ABSOLUTE)
        self.assertEquals(numOfBytes, 2)

    def testGetBytesFromFile(self):
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
        self.sut.getBytesFromFile(3)
        ins = self.sut.getNextInstruction()
        self.assertEquals(ins.address, [])

    def createSidFile(self):
        sidFile = file(self.testSidFileName, "wb")
        for byte in range(0, 124):
            sidFile.write("\x00")
        for byte in range(0, 2):
            sidFile.write("\x88")
        for byte in range(0, 100):
            sidFile.write("\xFF")
        sidFile.close()
        sidFile = file(self.testSidFileName, "rb")
        return sidFile

    def deleteSidFile(self, sidFile):
        sidFile.close()
        os.remove(self.testSidFileName)

    def testReadSidFile(self):
        sidFile = self.createSidFile()
        self.sut.setSidFile(sidFile)
        sidStruct = self.sut.readSidFile()
        for byte in sidStruct.header:
            self.assertEquals(byte, "\x00")
        for byte in sidStruct.offset:
            self.assertEquals(byte, "\x88")
        for byte in sidStruct.data:
            self.assertEquals(byte, "\xFF")
        self.sut.setSidFile(self.testFile)
        self.deleteSidFile(sidFile)

