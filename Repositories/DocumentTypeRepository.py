from ConfigDB import db
from Models.DocumentType import DocumentType
from sqlalchemy.exc import SQLAlchemyError

class DocumentTypeRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):

        if include_deleted:
            return DocumentType.query.all()
        return DocumentType.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, document_type_id, include_deleted=False):

        if include_deleted:
            return DocumentType.query.filter_by(DocumentTypeId=document_type_id).first()
        return DocumentType.query.filter_by(DocumentTypeId=document_type_id, IsDeleted=False).first()

    def create(self, description):

        try:
            new_document_type = DocumentType(Description=description, IsDeleted=False)
            self.db.session.add(new_document_type)
            self.db.session.commit()
            return new_document_type
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, document_type_id, description):

        try:
            existing = DocumentType.query.get(document_type_id)
            if not existing or existing.IsDeleted:
                return None
            
            existing.Description = description
            self.db.session.commit()
            return existing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete(self, document_type_id):

        try:
            document_type = DocumentType.query.get(document_type_id)
            if not document_type:
                return None
            
            document_type.IsDeleted = True
            self.db.session.commit()
            return document_type
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, document_type_id):

        try:
            document_type = DocumentType.query.get(document_type_id)
            if not document_type:
                return None
            
            document_type.IsDeleted = False
            self.db.session.commit()
            return document_type
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e