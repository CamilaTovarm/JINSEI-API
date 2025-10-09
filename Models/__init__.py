# Models/__init__.py

# Importa TODAS las clases de modelo (tablas) para que SQLAlchemy las detecte.

from .Consent import Consent
from .Contact import Contact
from .ContactType import ContactType
from .DocumentType import DocumentType 
from .Message import Message
from .RiskLevel import RiskLevel
from .ChatSession import ChatSession
from .User import User

# Opcional, pero bueno para la limpieza
__all__ = [
    'Consent', 'Contact', 'ContactType',
    'DocumentType', 'Message', 'RiskLevel', 'ChatSession', 'User'
]