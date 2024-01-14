from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime, timedelta
from typing import Any


class Device(ABC):
    """Абстрактный базовый класс прибора
    Описывает необходимые к реализации атрибуты/методы, для подключения прибора
    к системе мониторинга и сбора данных

    Атрибуты обязятельные к определению в приборе
    ---------------------------------------------------------------------------
    ...

    Методы обязательные к определению в приборе
    ---------------------------------------------------------------------------
    def connect(self) -> None
        реализация подключения к прибору

    def get_data(self) -> dict
        Получение текущих показаний прибора. Функция должна вернуть
        словарь определенной структуры(см. соответствующий пункт документации)
    """

    @abstractmethod
    def _connect_and_read(self) -> Any:
        """Реализуется физическое подключение к прибору, и считывание данных"""
        raise NotImplementedError

    @abstractmethod
    def get_data(self) -> dict:
        """Реализует получение данных "Монитором" от прибора.
        Возвращает словарь.
        Считанные данные привести к dict описанной ниже структуры:
            dict_structure = {
                "measurement": "<name>",
                "tags": {"<tag_name>": "<tag_value>"},
                "fields": {"<field_name>": <field_value>},
                "time": <measurement_time>
            }
        Допустимые типы данных в описанном словаре:
            <name>: str
            <tag_name>: str
            <tag_value>: str
            <field_name>: str
            <field_value>: str | int | float | bool
            <measurement_time>: datetime
        """
        raise NotImplementedError


class Inverter(Device):
    def __init__(self, **kwargs) -> None:
        self.name: str = "Invertor"
        self.model: str = "model"
        self.location: str = "location"
        self._raw_data: str
        self.port: str = "COM_port"
        self.__dict__.update(kwargs)

    def _connect_and_read(self) -> str:
        """Подключение к прибору
        Реализует подключение к прибору и считывает поток данных
        в виде строки.
        Считанную строку сохранить в self._raw_data и вернуть
        """
        return self._raw_data

    def get_data(self, **kwargs) -> dict:
        """"""
        current_time = kwargs.get('current_time', datetime.now())
        val_template = namedtuple(
            "InvertorData",
            [
                "VVV",  # O/P Voltage
                "QQQ",  # O/P load percent (Digital) 0, - 0%
                "SS_S",  # Battery voltage 12,24,48
                "BBB",  # Battery capacity (as O/P load percent)
                "TT_T",  # Heat Sink Temperature (0-99.9)оо
                "MMM",  # Utility Power Voltage (0-250VACоооо)
                "RR_R",  # Output Power Frequency (40.0-70.0) Hz
                "DDD",  # DC BUS Voltage (0V)
                "PPP",  # O/P load Percent (Analog) (0-100%)u
                "command_bits",
            ],
        )
        raw = self._raw_data.strip().lstrip("(").rstrip(")").split()
        if len(raw) != 10:
            raise TypeError("неверный формат ответа")
        values = val_template(*map(float, raw[:-1]), raw[-1])
        answer: dict = {
            "measurement": self.name,
            "tags": {"model": self.model, "location": self.location},
            "fields": values._asdict(),
            "time": current_time,
        }
        print(answer)
        return answer


class FakeInverter(Inverter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cur_datetime: datetime = datetime.now() - timedelta(hours=23)
        self.delta: timedelta = timedelta(minutes=10)
        self.line_counter = 0

    def __getattribute__(self, __name: str) -> Any:
        if __name == "cur_datetime":
            self.__dict__["cur_datetime"] += self.delta

        if __name == "_raw_data":
            with open("telemetry.txt", mode="r") as f:
                for _ in range(self.line_counter):
                    f.readline()
                line = f.readline().strip()
                self.__dict__["_raw_data"] = line
                self.line_counter += 2

        return super().__getattribute__(__name)

    def get_data(self, **kwargs) -> dict:
        return super().get_data(current_time=self.cur_datetime)
