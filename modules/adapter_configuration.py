import json
import pathlib


from tools import singleton


@singleton
class AdapterConfiguration:
    def __init__(self) -> None:
        self.__avatar_configuration = None
        self.__deepal_configuration = None
        self.__hima_configuration = None
        self.__voyah_configuration = None
        self.__configurations = {
            "avatar": self.__avatar_configuration,
            "deepal": self.__deepal_configuration,
            "hima": self.__hima_configuration,
            "voyah": self.__voyah_configuration,
        }

    @property
    def avatar_configuration(self) -> dict:
        return self.__avatar_configuration

    @property
    def deepal_configuration(self) -> dict:
        return self.__deepal_configuration

    @property
    def hima_configuration(self) -> dict:
        return self.__hima_configuration

    @property
    def voyah_configuration(self) -> dict:
        return self.__voyah_configuration

    @property
    def configurations(self) -> dict:
        return self.__configurations

    def load_configuration_by_name(self, name: str) -> dict:
        config = self.__configurations.get(name, dict())
        path = pathlib.Path(f"cat/configurations/{name}.json")
        if not config and path.exists():
            with open(path, "r") as config_file:
                config = json.load(config_file)
                self.__configurations.update({name: config})
        return config

    def load_configurations(self) -> dict:
        self.__avatar_configuration = self.load_configuration_by_name("avatar")
        self.__deepal_configuration = self.load_configuration_by_name("deepal")
        self.__hima_configuration = self.load_configuration_by_name("hima")
        self.__voyah_configuration = self.load_configuration_by_name("voyah")
        return self.__configurations
