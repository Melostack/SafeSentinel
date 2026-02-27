import unittest
from core.gatekeeper import Gatekeeper

class TestGatekeeper(unittest.TestCase):
    def test_gatekeeper_blacklist(self):
        gk = Gatekeeper()
        # Mocking blacklist behavior if needed, or testing actual blacklist if available
        # Assuming blacklist is empty by default or checking non-blacklisted address
        result = gk.check_blacklist("0x1234567890123456789012345678901234567890")
        self.assertIsNone(result)

    def test_validate_address_format(self):
        gk = Gatekeeper()
        valid, msg = gk.validate_address_format("0x1234567890123456789012345678901234567890", "ERC20")
        self.assertTrue(valid)
        valid, msg = gk.validate_address_format("InvalidAddress", "ERC20")
        self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()
