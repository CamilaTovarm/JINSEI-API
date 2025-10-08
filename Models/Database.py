from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from Models.User import User
    from Models.Session import Session
    from Models.DocumentType import DocumentType
    from Models.Consent import Consent
    from Models.ContactType import ContactType
    from Models.Contact import Contact
    from Models.RiskLevel import RiskLevel
    from Models.Message import Message
    db.create_all()
