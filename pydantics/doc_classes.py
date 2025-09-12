from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

class DocumentClasses(BaseModel):
    decompte_charge: str = Field(description="this document contains ..")
    facture: str = Field(description="this document contains the bill")
    repairing_report: str = Field(description="this document contains the description of ")
    repairing_report: str = Field(description="this document contains ...")
    certificates: str = Field(description="this document contains ...")