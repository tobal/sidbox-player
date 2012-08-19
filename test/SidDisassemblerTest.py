
import unittest
from src.SidDisassembler import SidDisassembler
from src.SidDisassembler import AddressModes

class SidDisassemblerTest(unittest.TestCase):

    def setUp(self):
        self.sut = SidDisassembler()    # system under test

    def tearDown(self):
        pass

    def testOutputIsString(self):
        output = self.sut.getInstructionAsAssembly(0xA1)
        self.assertTrue( type(output) is str )

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
        instrByte = self.sut.getBytesFromFile(1)
        instrType = self.sut.disassembleInstruction(instrByte[0])
        addrModeNumOfBytes = self.sut.getAddrModeNumOfBytes(instrType[1])
        address = self.sut.getBytesFromFile(addrModeNumOfBytes)
        instr = self.sut.makeInstruction(instrType, address)

        self.assertEquals(instr.mnemonic, "LDA")
        self.assertEquals(instr.address, [0x02, 0x01])

