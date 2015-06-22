from flask import render_template
from app.models.Menu import Menu
from . import site


@site.app_errorhandler(404)
def page_not_found(e):
    # Get the menu we want to use for this page...
    # TODO: make this more dynamic... probably tie it to the page
    mainMenu = Menu.query.filter_by(name="Main").first()

    return render_template('404.html', menu=mainMenu), 404


@site.app_errorhandler(500)
def internal_server_error(e):
    # Get the menu we want to use for this page...
    # TODO: make this more dynamic... probably tie it to the page
    mainMenu = Menu.query.filter_by(name="Main").first()

    return render_template('500.html', menu=mainMenu), 500
