from datetime import datetime
from dineder import db, login_manager
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dump({'user_id':self.id}).decode('utf-8')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Product(db.Model):
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    description = db.Column(db.String(200), nullable=False, default="******** description ********")
    size = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.category}', '{self.code}', '{self.quantity}', '{self.price}')"

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)
    grandtotal = db.Column(db.Float)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ski_pass = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return'<Ticket %r>' % self.ski_pass


class CustomerTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ski_pass = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float)
    grandtotal = db.Column(db.Float)

    def __repr__(self):
        return'<CustomerTicket %r>' % self.invoice

# utworzenie nowych modeli
class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ski_pass = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float)
    grandtotal = db.Column(db.Float)

    def __repr__(self):
        return'<CustomerTicket %r>' % self.invoice
