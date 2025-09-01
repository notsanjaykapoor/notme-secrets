import dataclasses
import json


@dataclasses.dataclass
class SecretData:
    """
    Plaintext representation of secrets.data_cipher field.
    """

    name: str
    passw: str = ""
    path: str = ""
    uri: str = ""
    user: str = ""

    def __str__(self):
        return json.dumps(self.__dict__)
