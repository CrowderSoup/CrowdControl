from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo
from app.models.Role import Role
from app.models.User import User


class AddUserForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])

    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])

    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])

    role = SelectField('Role', coerce=int)

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name)]

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            # The email is already in use by another user
            raise ValidationError('Email has already been used by another user')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            # The username is already in use by another user
            raise ValidationError('Username has already been used by another user')
