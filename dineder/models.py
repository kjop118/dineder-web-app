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
    restaurants = db.relationship('Post', backref='author', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dump({'user_id':self.id}).decode('utf-8')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


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
