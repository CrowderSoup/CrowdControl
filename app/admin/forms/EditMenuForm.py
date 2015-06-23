from flask.ext.wtf import Form
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length
from app.models.MenuItem import MenuItem

class EditMenuForm(Form):
    name = StringField('Menu Name', validators=[DataRequired(), Length(1, 32)])

    def validate_name(self, field):
        if MenuItem.query.filter_by(name=field.data).first():
            raise ValidationError('Menu Name is already in use')
