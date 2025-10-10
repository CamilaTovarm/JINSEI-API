from ConfigDB import db
from Models.DocumentType import DocumentType
from sqlalchemy.exc import SQLAlchemyError

class DocumentTypeRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return DocumentType.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, document_type_id):
        return DocumentType.query.filter_by(DocumentTypeId=document_type_id, IsDeleted=False).first()

    def create(self, description):
        try:
            new_document_type = DocumentType(Description=description, IsDeleted=False)
            self.db.session.add(new_document_type)
            self.db.session.commit()
            return new_document_type
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, document_type):
        existing = DocumentType.query.get(document_type.DocumentTypeId)
        if not existing or existing.IsDeleted:
            return None
        existing.Description = document_type.Description
        self.db.session.commit()
        return existing

    def delete(self, document_type):
        try:
            self.db.session.add(document_type)
            self.db.session.commit()
            return document_type
        except SQLAlchemyError:
            self.db.session.rollback()
            raise
