import unittest

import infrastructure.configuration as target

class ConfigurationTestCase(unittest.TestCase):

    def test_config_can_be_loaded(self):
        """Assert that the configuration can be loaded without errors"""

        result = target.get_config()

        self.assertIsInstance(result, target.Config)

if __name__ == "__main__":
    unittest.main()
