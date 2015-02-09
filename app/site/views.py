from flask import render_template, abort
from ..models import Page, Menu
from . import site
import CommonMark


@site.route('/', defaults={'slug': ''})
@site.route('/<path:slug>')
def page(slug):
    """ This is the main route of the site. It handles the index and all other 'static' pages. """

    # Some sensible defaults
    page = { 'Title': "", 'Content': "" }
    templatePath = "site/index.html"

    # Get the menu we want to use for this page...
    # TODO: make this more dynamic... probably tie it to the page
    mainMenu = Menu.query.filter_by(name="Main").first()

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    if slug == "":
        homePage = Page.query.filter_by(is_homepage=True).first()
        if homePage is not None:
            parsed = parser.parse(homePage.content)
            rendered = renderer.render(parsed)

            page = {
                'Title': homePage.title,
                'Content': rendered
            }
    else:
        templatePath = "site/page.html"
        currentPage = Page.query.filter_by(slug=slug).first()
        if currentPage is None:
            abort(404)

        parsed = parser.parse(currentPage.content)
        rendered = renderer.render(parsed)

        page = {
            'Title': currentPage.title,
            'Content': rendered
        }

    # Let's return the page and menu items
    return render_template(templatePath, page=page, menu=mainMenu)
