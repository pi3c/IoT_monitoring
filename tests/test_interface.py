from nts_ntu.app import InfDBInterface
from nts_ntu.config import test_config


def test_intarface_creation():
    interface = InfDBInterface(config=test_config)
    assert interface.org == "MyOrg"
