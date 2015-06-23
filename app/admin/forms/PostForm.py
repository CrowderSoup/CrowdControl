from flask.ext.wtf import Form
from wtforms import StringField, SelectField, DateTimeField
from app.wtform_widgets import MarkdownField
from wtforms.validators import DataRequired, Length
from app.models.BlogCategory import BlogCategory
from app.models.BlogPostStatus import BlogPostStatus


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = MarkdownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    status = SelectField('Status', coerce=int)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.category.choices = [(category.id, category.name)
                                 for category in BlogCategory.query.order_by(BlogCategory.name)]
        self.status.choices = [(status.id, status.name)
                               for status in BlogPostStatus.query.order_by(BlogPostStatus.name)]
