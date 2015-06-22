from flask import render_template, abort
from app.models.Page import Page
from app.models.Menu import Menu
from . import site
import CommonMark


@site.route('/', defaults={'slug': ''})
@site.route('/<path:slug>')
def page(slug):
    """ This is the main route of the site. It handles the index and all other 'static' pages. """

    # Some sensible defaults
    the_page = {'Title': "", 'Content': ""}
    template_path = "site/index.html"

    # Init menu to a blank one
    menu = Menu

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    if slug == "":
        home_page = Page.query.filter_by(is_homepage=True).first()
        if home_page is not None:
            parsed = parser.parse(home_page.content)
            rendered = renderer.render(parsed)

            menu = home_page.menu

            the_page = {
                'Title': home_page.title,
                'Content': rendered
            }
    else:
        template_path = "site/page.html"
        current_page = Page.query.filter_by(slug=slug).first()
        if current_page is None:
            abort(404)

        parsed = parser.parse(current_page.content)
        rendered = renderer.render(parsed)

        menu = current_page.menu

        the_page = {
            'Title': current_page.title,
            'Content': rendered
        }

    # Let's return the page and menu items
    return render_template(template_path, page=the_page, menu=menu)
