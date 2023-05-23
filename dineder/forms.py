from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dineder.models import Users
from flask_login import current_user


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname',
                          validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# class UpdateAccountForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#
#     submit = SubmitField('Update')
#
#     def validate_username(self, username):
#         if username.data != current_user.username:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError('Username is taken. Choose another one.')
#
#     def validate_email(self, email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError('Email is taken. Choose another one.')


# class ProductForm(FlaskForm):
#     name = StringField('Name',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     category = StringField('Category', validators=[DataRequired(), Length(min=2, max=20)])
#     code = IntegerField('Code', validators=[DataRequired()])
#     quantity = IntegerField('Quantity', validators=[DataRequired()])
#     price = FloatField('Price', validators=[DataRequired()])
#     image = FileField('Product image', validators=[FileAllowed(['jpg', 'png'])])


# class PostForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     content = TextAreaField('Content', validators=[DataRequired()])
#     submit = SubmitField('Post')

# class ProductSearchForm(FlaskForm):
#         choices = [('name', 'category'),
#                    ('code', 'Album' ),
#                    ('Publisher', 'Publisher')]
#         select = SelectField('Search for music:', choices=choices)
#         search = StringField('')


# class OrderForm(Form):  # Create Order Form
#     name = StringField('', [validators.length(min=1), validators.DataRequired()],
#                        render_kw={'autofocus': True, 'placeholder': 'Full Name'})
#     mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],
#                              render_kw={'autofocus': True, 'placeholder': 'Mobile'})
#     quantity = SelectField('', [validators.DataRequired()],
#                            choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
#     order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
#                               render_kw={'placeholder': 'Order Place'})
