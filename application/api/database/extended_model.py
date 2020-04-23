from application.api.database import db


class ExtendedModel(db.Model):
    __abstract__ = True

    def upsert_this(self):
        if (isinstance(self, db.Model)):
            ExtendedModel.upsert_one(self, False)
        else:
            raise Exception('ERROR UPSERT_THIS - self %r' % self)

    def delete_this(self):
        if (isinstance(self, db.Model)):
            ExtendedModel.delete_one(self, False)
        else:
            raise Exception('ERROR DELETE_THIS - self %r' % self)

    @classmethod
    def upsert(ExtendedModel, items):
        try:
            if (isinstance(items, list)):
                [db.session.add(item) for item in items]
            else:
                ExtendedModel.upsert_one(items)
            db.session.commit()
            return items
        except:
            db.session.rollback()
            raise Exception('ERROR UPSERT - ROLLED BACK items%r' % items)

    @classmethod
    def upsert_one(ExtendedModel, item, lazy=True):
        if (isinstance(item, db.Model)):
            db.session.add(item)
            if (not lazy):
                db.session.commit()
        else:
            raise Exception('ERROR UPSERT_ONE - item %r' % item)

    @classmethod
    def delete(ExtendedModel, items):
        try:
            if (isinstance(items, list)):
                [db.session.delete(item) for item in items]
            else:
                ExtendedModel.delete_one(items)
            db.session.commit()
            return items
        except:
            db.session.rollback()
            raise Exception('ERROR UPSERT - ROLLED BACK items%r' % items)

    @classmethod
    def delete_one(ExtendedModel, item, lazy=True):
        if (isinstance(item, db.Model)):
            db.session.delete(item)
            if (not lazy):
                db.session.commit()
        else:
            raise Exception('ERROR UPSERT_ONE - item %r' % item)

    @classmethod
    def clear_all(ExtendedModel):
        try:
            num_rows_deleted = db.session.query(ExtendedModel).delete()
            db.session.commit()
            return num_rows_deleted
        except:
            db.session.rollback()
            raise Exception('ERROR CLEAR_ALL')
