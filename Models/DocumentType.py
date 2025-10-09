from ConfigDB import db

class DocumentType(db.Model):
    __tablename__ = "DocumentTypes"

    DocumentTypeId = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(50), nullable=False)
    IsDeleted = db.Column(db.Boolean, default=False)

    consents = db.relationship("Consent", backref="DocumentType", cascade="all, delete-orphan")
