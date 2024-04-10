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


class PlaceListResponse(BaseClassifyResponse):
    image_url: HttpUrl


class CategoryModel(BaseModel):
    value: str
    probability: float


class ClassifyImage:
    class Response(BaseModel):
        predicts: list[PlaceListResponse]
        categories: list[CategoryModel]
