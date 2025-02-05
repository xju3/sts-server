from dataclasses import dataclass
from dataclass_wizard import JSONWizard

@dataclass
class Ticket(JSONWizard):
    """ticket id after uploading image successfully."""
    clientId: str
    
    def __init__(self, _ticket_id: str = None):
        self.clientId = _ticket_id

