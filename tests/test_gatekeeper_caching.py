import unittest
import sys
import os
import json
import tempfile

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.gatekeeper import Gatekeeper

class TestGatekeeperCaching(unittest.TestCase):
    def setUp(self):
        # Create a temporary registry file
        self.temp_registry = tempfile.NamedTemporaryFile(mode='w', delete=False)
        json.dump({"initial": "value"}, self.temp_registry)
        self.temp_registry.close()

        self.temp_blacklist = tempfile.NamedTemporaryFile(mode='w', delete=False)
        json.dump([], self.temp_blacklist)
        self.temp_blacklist.close()

    def tearDown(self):
        if os.path.exists(self.temp_registry.name):
            os.remove(self.temp_registry.name)
        if os.path.exists(self.temp_blacklist.name):
            os.remove(self.temp_blacklist.name)

        # Clear cache to avoid side effects on other tests (though redundant if process exits)
        if self.temp_registry.name in Gatekeeper._registry_cache:
            del Gatekeeper._registry_cache[self.temp_registry.name]

    def test_caching_behavior(self):
        # 1. First instantiation
        gk1 = Gatekeeper(registry_path=self.temp_registry.name, blacklist_path=self.temp_blacklist.name)
        self.assertEqual(gk1.registry, {"initial": "value"})

        # 2. Modify file directly
        with open(self.temp_registry.name, 'w') as f:
            json.dump({"modified": "value"}, f)

        # 3. Second instantiation (should use cache)
        gk2 = Gatekeeper(registry_path=self.temp_registry.name, blacklist_path=self.temp_blacklist.name)
        self.assertEqual(gk2.registry, {"initial": "value"})
        self.assertNotEqual(gk2.registry, {"modified": "value"})

        # 4. Verify cache content directly
        self.assertIn(self.temp_registry.name, Gatekeeper._registry_cache)
        self.assertEqual(Gatekeeper._registry_cache[self.temp_registry.name], {"initial": "value"})

if __name__ == '__main__':
    unittest.main()
