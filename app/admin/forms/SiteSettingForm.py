from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class SiteSettingForm(Form):
    name = StringField("Name", validators=[DataRequired(), \
                        Length(min=1, max=128)])
    value = StringField("Value", validators=[DataRequired()])
