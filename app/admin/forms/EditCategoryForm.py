from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class EditCategoryForm(Form):
    name = StringField("Name", validators=[DataRequired(), Length(1, 64)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    description = StringField("Description", validators=[Length(1, 512)])
