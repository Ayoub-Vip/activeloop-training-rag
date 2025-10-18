from ..structured_output.invoice import Invoice
from ..structured_output.contract import Contract
from ..structured_output.repair_report import RepairReport
from ..structured_output.charge_statement import ChargeStatement
from ..structured_output.base import BaseStructuredOutput


def get_output_cls(doc_class: str):
    switch = {
        "contract": Contract,
        "charge_statement": ChargeStatement,
        "invoice": Invoice,
        "repair_report": RepairReport
    }
    
    return switch.get(doc_class, default=BaseStructuredOutput)

