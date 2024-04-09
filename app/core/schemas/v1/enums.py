from enum import Enum


class CityEnum(str, Enum):
    NIJNIY_NOVGOROD = "nizhniy_novgorod"
    YAROSLAVL = "yaroslavl"
    VLADIMIR = "vladimir"
    EKATIRINBURG = "ekatirinburg"

    @classmethod
    def get_city_name(cls, city: str) -> str:
        return {
            "nizhniy_novgorod": "Нижний Новгород",
            "yaroslavl": "Ярославль",
            "vladimir": "Владимир",
            "ekatirinburg": "Екатеринбург",
        }[city]

    @classmethod
    def get_city_name_by_enum(cls, city: "CityEnum") -> str:
        return cls.get_city_name(city.value)

    @classmethod
    def get_all_cities(cls) -> dict[str, str]:
        """Returns city name as in city enum to their pretty value"""
        cities = [city.value for city in CityEnum]
        return {
            city: cls.get_city_name(city) for city in cities
        }
