from flask.ext.wtf import Form
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from app.models.Page import Page
from app.models.BlogPost import BlogPost
from app.models.Menu import Menu


class EditMenuItemForm(Form):
    name = StringField('Menu Item Name', validators=[DataRequired(), Length(1, 32)])
    menu = SelectField('Menu', coerce=int)
    slug = SelectField('Url')
    weight = IntegerField('Item Weight')

    def __init__(self, *args, **kwargs):
        super(EditMenuItemForm, self).__init__(*args, **kwargs)

        self.menu.choices = [(menu.id, menu.name)
                             for menu in Menu.query.order_by(Menu.name)]

        pageslugs = [("/{0}".format(page.slug)) for page in Page.query.filter_by(is_homepage=False).order_by(Page.slug)]
        blogslugs = [("/blog/post/{0}".format(post.slug)) for post in BlogPost.query.order_by(BlogPost.slug)]
        slugs = ["/"] + pageslugs + ["/blog"] + blogslugs
        self.slug.choices = [(slug, slug) for slug in slugs]
