import datetime
from pydantic import BaseModel, Field
from base import BaseStructuredOutput


class ChargeStatement(BaseStructuredOutput):
    """Document detailing expenses (energy, insurance, maintenance, taxes, etc.) to be re-invoiced to tenants, taking into account provisions."""
    