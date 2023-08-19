import time
from flask import url_for

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.dialects.mysql import INTEGER

db = SQLAlchemy()


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(self._only_full_mapper_zero('get'),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None


class User(db.Model):
    __tablename__ = 'users'
    # __table_args__ = (
    #     # this can be replaced with db.PrimaryKeyConstraint if it to be a primary key
    #     db.UniqueConstraint('merchant_id', 'mobile', 'country_code'),
    # )
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    mobile = db.Column(db.String(10))
    email = db.Column(db.String(50), nullable=False)
    channel_id = db.Column(INTEGER(unsigned=True), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.Integer, default=lambda: int(time.time()))
    updated_on = db.Column(db.Integer, default=lambda: int(time.time()), onupdate=lambda: int(time.time()))
    deleted = db.Column(db.Boolean(), default=False)

    query_class = QueryWithSoftDelete

    def __repr__(self):
        return '<User - {} {}>'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User - {} {}>'.format(self.first_name, self.last_name)

    def to_dict(self):
        return {'id': self.id, 'name': self.message,
                'first_name': self.first_name, 'last_name': self.last_name,
                'url': url_for('get_user', id=self.user_id)
                }


class FlowStep(db.Model):
    __tablename__ = "flow_steps"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_root  = db.Column(db.Boolean, default=False)
    step = db.Column(db.Integer, nullable=False)
    parent = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text)
    file_url = db.Column(db.String(50))
    file_type = db.Column(db.String(50))
    option1 = db.Column(db.String(50))
    option2 = db.Column(db.String(50))
    option3 = db.Column(db.String(50))
    created_on = db.Column(db.Integer, default=lambda: int(time.time()))
    updated_on = db.Column(db.Integer, default=lambda: int(time.time()), onupdate=lambda: int(time.time()))

