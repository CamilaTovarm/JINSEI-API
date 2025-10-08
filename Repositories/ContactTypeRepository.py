from Models.ContactType import ContactType
from Models.Database import db

class ContactTypeRepository:

    def get_all(self):
        return ContactType.query.all()

    def get_by_id(self, id):
        return ContactType.query.get(id)

    def create(self, name, description):
        ct = ContactType(name=name, description=description)
        db.session.add(ct)
        db.session.commit()
        return ct

    def update(self, id, name=None, description=None):
        ct = self.get_by_id(id)
        if not ct:
            return None
        if name: ct.name = name
        if description: ct.description = description
        db.session.commit()
        return ct

    def delete(self, id):
        ct = self.get_by_id(id)
        if not ct:
            return False
        db.session.delete(ct)
        db.session.commit()
        return True
