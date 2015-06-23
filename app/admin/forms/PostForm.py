from flask.ext.wtf import Form
from wtforms import StringField, SelectField, DateTimeField
from app.wtform_widgets import MarkdownField
from wtforms.validators import DataRequired, Length
from app.models.BlogCategory import BlogCategory


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = MarkdownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.category.choices = [(category.id, category.name)
                                 for category in BlogCategory.query.order_by(BlogCategory.name)]
