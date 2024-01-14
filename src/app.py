from src.config import test_config
from src.device import FakeInverter
from src.monitor import Monitor


def demo_test():
    monitor = Monitor(session_config=test_config)
    device_conf = {
        "name": "myinv",
        "model": "12345",
        "location": "my_home",
        "port": "COM",
    }
    device = FakeInverter(**device_conf)
    monitor.init_device(device)
    monitor.mainloop()
