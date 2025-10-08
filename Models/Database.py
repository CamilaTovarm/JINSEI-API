from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from models.user import User
    from models.session import Session
    from models.document_type import DocumentType
    from models.consent import Consent
    from models.contact_type import ContactType
    from models.contact import Contact
    from models.risk_level import RiskLevel
    from models.message import Message
    db.create_all()
