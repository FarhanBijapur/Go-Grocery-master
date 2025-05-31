from flask_wtf  import FlaskForm
from wtforms import *
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import Email,DataRequired,EqualTo
from app_grocery.database import Category
from app_grocery.database import user



class Signup_User(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email=StringField('Email ID',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password','Must be same as password')])
    submit=SubmitField('Sign up')
   


class User_Login(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Sign In')

class Admin_Login(FlaskForm):
    username=StringField('Admin Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Sign In')
    remember=BooleanField('Remember Me')

class create_category(FlaskForm):
    name=StringField('Category Name:',validators=[DataRequired()])
    submit=SubmitField('Create/Update')

class create_product(FlaskForm):
    name=StringField('Product Name:',validators=[DataRequired()])
    exp_date = StringField('Expiry Date:',validators=[DataRequired()])
    price =IntegerField('Price: ',validators=[DataRequired()])
    stock =IntegerField('Quantity: ')
    category_id = SelectField('Select Category:', validators=[DataRequired()])
    image=FileField('Product Image',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Create/Update')
    def initialize(self):
        self.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

class search_field(FlaskForm):
    search=SearchField('Search by category/Product')
    submit=SubmitField('Search')

class quantity_order(FlaskForm):
    quantity=IntegerField('Quanity',validators=[DataRequired()])
    submit=SubmitField('Update')
    


