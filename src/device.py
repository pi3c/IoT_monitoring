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
    def connect(self):
        """Реализуется физическое подключение к прибору, для сбора данных"""
        raise NotImplementedError

    @abstractmethod
    def get_data(self) -> dict:
        """Реализует получение данных от прибора возвращает словарь.
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

        Функция должна вернуть созданный словарь
        """
        raise NotImplementedError


class Inverter(Device):
    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs.get("name", "fakeinvertor")
        self.model: str = kwargs.get("model", "fakemodel")
        self.location: str = kwargs.get("name", "fakelocation")
        self._raw_data: str
        self.port: str = kwargs.get("name", "fakeCOMport")
        self.__dict__.update(kwargs)

    def connect(self):
        pass

    def get_data(self, current_time: datetime = datetime.now()) -> dict:
        val_template = namedtuple(
            "InvertorData",
            [
                "VVV",  # O/P Voltage
                "QQQ",  # O/P load percent (Digital) 0, - 0%
                "SS_S",  # Battery voltage 12,24,48
                "BBB",  # Battery capacity (as O/P load percent)
                "TT_T",  # Heat Sink Temperature (0-99.9)
                "MMM",  # Utility Power Voltage (0-250VACоооо)
                "RR_R",  # Output Power Frequency (40.0-70.0) Hz
                "DDD",  # DC BUS Voltage (0V)
                "PPP",  # O/P load Percent (Analog) (0-100%)u
                "command_bits",
            ],
        )
        raw = self._raw_data.strip().lstrip("(").rstrip(")").split()
        print(raw)

        values = val_template(*map(float, raw[:-1]), raw[-1])
        answer: dict = {
            "measurement": self.name,
            "tags": {"model": self.model, "location": self.location},
            "fields": values._asdict(),
            "time": current_time,
        }
        return answer


class FakeInverter(Inverter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cur_datetime: datetime = datetime.now() - timedelta(hours=23)
        self.delta: timedelta = timedelta(minutes=10)

    def __getattribute__(self, __name: str) -> Any:
        if __name == "cur_datetime":
            self.__dict__["cur_datetime"] += self.delta
        return super().__getattribute__(__name)

    def set_fake_answer(self, line: str) -> None:
        self._raw_data = line

    def get_data(self, current_time: datetime = datetime.now()) -> dict:
        return super().get_data(self.cur_datetime)
