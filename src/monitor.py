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

        self.device_list: List[Device] = []
        self.session_config: dict = session_config
        self.pooling_delay: int | float = pooling_delay

    def init_device(self, device: Device) -> None:
        """Инициализация конечного устройства для наблюдения"""
        if isinstance(device, Device):
            self.device_list.append(device)
        else:
            raise TypeError(
                'Не могу инициализировать конечное устройство,\n' \
                'init_device притимает только объекты-наследники класса Device'
            )

    def __get_device_data(self, device: Device) -> dict:
        """Запрос данных от класса устройства
        Нужно сделать валидацию структуры и параметры данных
        """
        answer = device.get_data()
        return answer

    def __send_devices_data_to_db(self) -> None:
        """Сбор данных от всех устройств и отправка на сохранение"""
        session = InfDBSession(config=self.session_config)
        for device in self.device_list:
            data: dict = self.__get_device_data(device)
            session.add(data)
        session.commit()

    def mainloop(self) -> None:
        """Главный цикл монитора"""
        while True:
            self.__send_devices_data_to_db()
            time.sleep(self.pooling_delay)
