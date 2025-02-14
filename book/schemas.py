from pydantic import BaseModel


class BookData(BaseModel):
    title: str
    author: str
    category: str
    image: str
    publish_time: str
    publishing_house: str
    isbn: str
    price: str
    count: int
    serial: str
    desc: str
