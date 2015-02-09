from flask.ext.wtf import Form
from wtforms import StringField, DateTimeField, BooleanField, SelectField, PasswordField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..wtform_widgets import MarkdownField
from ..models import User, Role, Menu, MenuItem, Page, BlogPost


class EditMenuForm(Form):
    name = StringField('Menu Name', validators=[DataRequired(), Length(1, 32)])


    def validate_name(self, field):
        if MenuItem.query.filter_by(name=field.data).first():
            raise ValidationError('Menu Name is already in use')


class EditMenuItemForm(Form):
    name = StringField('Menu Item Name', validators=[DataRequired(), Length(1, 32)])
    menu = SelectField('Menu', coerce=int)
    slug = SelectField('Url')
    weight = IntegerField('Item Weight')

    def __init__(self, *args, **kwargs):
        super(EditMenuItemForm, self).__init__(*args, **kwargs)

        self.menu.choices = [(menu.id, menu.name)
                             for menu in Menu.query.order_by(Menu.name)]

        pageSlugs = [("/{0}".format(page.slug)) for page in Page.query.filter_by(is_homepage=False).order_by(Page.slug)]
        blogSlugs = [("/blog/{0}".format(post.slug)) for post in BlogPost.query.order_by(BlogPost.slug)]
        slugs = ["/"] + pageSlugs + ["/blog"] + blogSlugs
        self.slug.choices = [(slug, slug) for slug in slugs]


class EditPageForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = MarkdownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])
    is_homepage = BooleanField('Is Homepage?')


class AddPageForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = MarkdownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])
    is_homepage = BooleanField('Is Homepage?')


class EditPostForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = MarkdownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])


class AddPostForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = MarkdownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])


class EditUserForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])

    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])

    password = PasswordField('Password', validators=[EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password')

    role = SelectField('Role', coerce=int)


    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name)]

        self.user = user


    def validate_email(self, field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            # The email is already in use by another user
            raise ValidationError('Email has already been used by another user')


    def validate_username(self, field):
        if field.data != self.user.username and \
            User.query.filter_by(username=field.data).first():
            # The username is already in use by another user
            raise ValidationError('Username has already been used by another user')


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
            raise ValidationError('Email has already been used by another user')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username has already been used by another user')