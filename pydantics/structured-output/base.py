import datetime
from pydantic import BaseModel, Field
from ...utils.query_helpers import is_gestionnaire_from_db

#TODO: implement and add required Fields, validation methods, correct description... for all subclasses
class BaseStructuredOutput(BaseModel):
    """this contains basic fields commonly used for all types of documents, such as parts, date, signator, locataire, gestionnaire, meubles..."""
    
    title: str = Field(description="the title of the document, typically explicitly found in the begining or can be resumed from fisrt paragraphs ")
    manager: str = Field(description="A company that manages several real estate assets of various types.the full name of the persone representing the company, can be found from the from the given list",
                              validate_default=is_gestionnaire_from_db)
    tenant: str = Field(description="Occupant of real estate assets (private, business, non-profit organization, etc.). the full name of the persone that is , can be found from the from the given list",
                              validate_default=is_gestionnaire_from_db)
    building: str = Field(alias="entity", description="the real estate itself (also called entity)")
    date: datetime = Field(description="the date of releasing the document")



# Manager: A company that manages several real estate assets of various types.
# Tenant: Occupant of real estate assets (private, business, non-profit organization, etc.).
# Real estate asset: Building (=entity).
# Portfolio: Several real estate assets (=group of entities).
# Invoice: (general definition) Invoice sent by the manager to the tenant (rent payment, provision, etc.).
# Unpaid amounts: Difference between the amount invoiced and the amount actually collected.
# Charge statement: Document detailing expenses (energy, insurance, maintenance, taxes, etc.) to be re-invoiced to tenants, taking into account provisions.
# Provisions: Advance payment by the tenant of charges and taxes relating to their occupancy of the building.