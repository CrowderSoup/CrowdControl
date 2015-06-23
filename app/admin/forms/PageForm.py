from flask.ext.wtf import Form
from wtforms import StringField, SelectField, DateTimeField, BooleanField
from app.wtform_widgets import MarkdownField
from wtforms.validators import DataRequired, Length
from app.models.Menu import Menu


class PageForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = MarkdownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])
    is_homepage = BooleanField('Is Homepage?')
    menu = SelectField("Menu", coerce=int)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        self.menu.choices = [(menu.id, menu.name)
                             for menu in Menu.query.order_by(Menu.name)]