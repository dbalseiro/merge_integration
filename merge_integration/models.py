from typing import Optional
from pydantic import BaseModel


class ThrvContact(BaseModel):
    name: str
    email: Optional[str]
