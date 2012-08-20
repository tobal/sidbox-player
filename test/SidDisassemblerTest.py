
import unittest
from src.SidDisassembler import SidDisassembler
from src.SidDisassembler import AddressModes

class SidDisassemblerTest(unittest.TestCase):

    def setUp(self):
        self.sut = SidDisassembler()    # system under test
        # TODO: write the file in the test
        self.testFile = file("testfile", "rb")

    def tearDown(self):
        self.testFile.close()

    def testAbsoluteAddressedLoadAccumulator(self):
        output = self.sut.disassembleInstruction(0xAD)
        self.assertEquals(output, ["LDA", AddressModes.ABSOLUTE])

    def testAbsoluteHasTwoByteAddress(self):
        numOfBytes = self.sut.getAddrModeNumOfBytes(AddressModes.ABSOLUTE)
        self.assertEquals(numOfBytes, 2)

    def testGetAnInstructionWithAddress(self):
        self.sut.setSidFile(self.testFile)
        instr = self.sut.getNextInstruction()

        self.assertEquals(instr.mnemonic, "LDA")
        self.assertEquals(instr.address, [0x02, 0x01])

    def testInstructionComments(self):
        comment = self.sut.getCommentForMnemonic("LDA")
        self.assertEquals(comment, "Loads data from address into accumulator")

    def testGetInstructionAsAssembly(self):
        self.sut.setSidFile(self.testFile)
        instruction = self.sut.getNextInstruction()
        asmCode = self.sut.getInstructionAsAssembly(instruction)
        self.assertEquals(asmCode, "LDA 02 01   ; Loads data from address into accumulator")

    def testGetBytesFromFile(self):
        self.sut.setSidFile(self.testFile)
        byte = self.sut.getBytesFromFile(1)
        twoBytes = self.sut.getBytesFromFile(2)
        self.assertEquals(len(byte), 1)
        self.assertEquals(len(twoBytes), 2)

