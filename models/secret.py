import dataclasses
import json

@dataclasses.dataclass
class Secret:
    name: str
    passw: str = ""
    path: str = ""
    uri: str = ""
    user: str = ""
    # data: dict = {}

    def __str__(self):
        return json.dumps(self.__dict__)