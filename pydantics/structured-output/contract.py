import datetime
from pydantic import BaseModel, Field
from base import BaseStructuredOutput


class Contract(BaseStructuredOutput):
    # net_price: float = Field(description="the totalenet price to pay")
    # brut_price: float = Field(description="the totale brut price to pay")
    terms: list[str] = Field(description="a list of all contract terms")