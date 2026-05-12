import sys
from unittest.mock import MagicMock
sys.modules['fastapi'] = MagicMock()
sys.modules['fastapi.middleware'] = MagicMock()
sys.modules['fastapi.middleware.cors'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['core'] = MagicMock()
sys.modules['core.gatekeeper'] = MagicMock()
sys.modules['core.humanizer'] = MagicMock()
sys.modules['core.sourcing_agent'] = MagicMock()
sys.modules['core.connectors'] = MagicMock()
sys.modules['core.connectors.web3_rpc_connector'] = MagicMock()

import api.server
print("api.server imported successfully")
