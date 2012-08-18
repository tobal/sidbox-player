
import unittest
import sidDisassemblerTest

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(sidDisassemblerTest)

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

