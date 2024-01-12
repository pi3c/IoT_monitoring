from src.device import FakeInverter
from src.monitor import Monitor


def run_test_monitor(config: dict):
    monitor = Monitor(session_config=config)
    device_conf = {
        "name": "myinv",
        "model": "12345",
        "location": "my_home",
        "port": "COM",
    }
    device = FakeInverter(**device_conf)
    monitor.init_device(device)
    monitor.demo_get_device_data_from_file()


if __name__ == "__main__":
    pass
