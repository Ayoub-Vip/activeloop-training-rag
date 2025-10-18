import datetime
from pydantic import BaseModel, Field
from base import BaseStructuredOutput


class Invoice(BaseStructuredOutput):
    """Invoice sent by the manager to the tenant (rent payment, provision, etc.).
    """
    net_price: float = Field(description="the totalenet price to pay")
    brut_price: float = Field(description="the totale brut price to pay")