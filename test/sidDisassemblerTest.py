
import unittest
from src.sidDisassembler import sidDisassembler

class sidDisassemblerTest(unittest.TestCase):

    def setUp(self):
        self.sut = sidDisassembler()    # system under test

    def tearDown(self):
        pass

    def testOutputIsString(self):
        output = self.sut.disassembleInstruction(0xA1)
        self.assertTrue( type(output) is str )

