class BaseEntity:
    def __init__(self, name: str, birthday: str, sex: str, race: str, lat: int, lon: int):
        self.name: str = name
        self.birthday: str = birthday
        self.sex: str = sex
        self.race: str = race
        self.lat: int = lat
        self.lon: int = lon