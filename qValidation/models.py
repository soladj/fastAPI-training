from typing import Optional

from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., title='name title', min_length=1, max_length=10)
    price: float = Field(..., title='price title', gt=0)
    is_offer: Optional[bool] = None
