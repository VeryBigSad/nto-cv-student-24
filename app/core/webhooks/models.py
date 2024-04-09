from pydantic import BaseModel


class TestResultModel(BaseModel):
    result: bool
    user_id: int
    video_lesson_order_number: int
    is_webinar: bool
