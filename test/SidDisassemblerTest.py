
import unittest
from src.sidDisassembler import SidDisassembler
from src.sidDisassembler import AddressModes

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
        result = (output == ["LDA", AddressModes.ABSOLUTE])
        self.assertTrue(result)

