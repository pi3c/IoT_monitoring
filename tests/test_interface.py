from src.session import InfDBSession
from src.config import test_config


def test_intarface_creation():
    interface = InfDBSession(config=test_config)
