import influxdb_client as infdb
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfDBSession:
    def __init__(self, config: dict) -> None:
        self.token: str
        self.url: str
        self.org: str
        self.bucket: str
        self.__dict__.update(config)
        self.__points_queue: list = []

        self.__client = infdb.InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org,
        )
        self.__write_api = self.__client.write_api(write_options=SYNCHRONOUS)

    def add(self, point: dict) -> None:
        print(point)
        self.__points_queue.append(Point.from_dict(point))
        print(len(self.__points_queue))

    def commit(self) -> None:
        while self.__points_queue:
            self.__write_api.write(
                org=self.org,
                bucket=self.bucket,
                record=self.__points_queue.pop(0),
            )
