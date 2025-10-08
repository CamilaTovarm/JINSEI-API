from Models.DocumentType import DocumentType
from Models.Database import db

class DocumentTypeRepository:

    def get_all(self):
        return DocumentType.query.all()

    def get_by_id(self, id):
        return DocumentType.query.get(id)

    def create(self, code, description):
        doc_type = DocumentType(code=code, description=description)
        db.session.add(doc_type)
        db.session.commit()
        return doc_type

    def update(self, id, code=None, description=None):
        doc_type = self.get_by_id(id)
        if not doc_type:
            return None
        if code: doc_type.code = code
        if description: doc_type.description = description
        db.session.commit()
        return doc_type

    def delete(self, id):
        doc_type = self.get_by_id(id)
        if not doc_type:
            return False
        db.session.delete(doc_type)
        db.session.commit()
        return True
