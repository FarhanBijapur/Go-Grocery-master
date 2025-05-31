from app_grocery import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


buys = db.Table('buy',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False),
                db.Column('product_id', db.Integer, db.ForeignKey('product.id'),nullable=False),
                db.Column('count', db.Integer,nullable=False),
                db.Column('total_price',db.Integer,nullable=False)
                )

#user info
class user(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    bought = db.relationship('Product', secondary=buys, backref='bought')
    def is_authenticated(self):
        return True



#admin info
class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    

#category info
class Category(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20), unique=True)
        pr = db.relationship('Product', backref='Category',cascade="all, delete-orphan")
        def get_product_count(self):
            return len(self.pr)

 #product info
class Product(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        exp_date = db.Column(db.String(60))
        price = db.Column(db.Integer)
        stock = db.Column(db.Integer)
        image=db.Column(db.String(20),nullable=False,default='default.jpg')
        category_id = db.Column(db.Integer, db.ForeignKey('category.id'))