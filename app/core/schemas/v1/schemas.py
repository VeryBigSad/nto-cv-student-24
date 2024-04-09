from core.schemas.v1.enums import CityEnum
from pydantic import BaseModel, HttpUrl


class CoordinateModel(BaseModel):
    longitude: float
    latitude: float


class BaseClassifyResponse(BaseModel):
    xid: str
    name: str
    category: str
    city: CityEnum
    coordinates: CoordinateModel
    probability: float


class ClassifyText:
    class Request(BaseModel):
        text: str

    class Response(BaseClassifyResponse):
        pass


class ClassifyImage:
    class Response(BaseClassifyResponse):
        image_url: HttpUrl
