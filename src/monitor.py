import time
from typing import List

from src.device import Device
from src.session import InfDBSession


class Monitor:
    def __init__(
        self,
        session_config: dict,
        pooling_delay: int | float = 0.1,
    ) -> None:
        """
        description
        """
        self.device_list: List[Device] = []
        self.session_config: dict = session_config
        self.pooling_delay: int | float = pooling_delay

    def init_device(self, device: Device) -> None:
        self.device_list.append(device)

    def _get_device_data(self, device: Device) -> dict:
        answer = device.get_data()
        return answer

    def __send_devices_data_to_db(self) -> None:
        session = InfDBSession(config=self.session_config)
        for device in self.device_list:
            data: dict = self._get_device_data(device)
            session.add(data)
        session.commit()

    def mainloop(self) -> None:
        while True:
            self.__send_devices_data_to_db()
            time.sleep(self.pooling_delay)

    def demo_get_device_data_from_file(self):
        with open("telemetry.txt", mode="r") as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    self.device_list[0].set_fake_answer(line)
                    self.__send_devices_data_to_db()
