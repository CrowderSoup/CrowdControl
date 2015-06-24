from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required
from . import admin
from app import db
from app.models.Menu import Menu
from app.models.MenuItem import MenuItem
from app.admin.forms.EditMenuForm import EditMenuForm
from app.admin.forms.EditMenuItemForm import EditMenuItemForm


@admin.route('/menus')
@login_required
def menus():
    all_menus = Menu.query.all()
    return render_template('admin/menus/menus.html', js='menus/menus', menus=all_menus)


@admin.route('/menus/menu/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def menu(menu_id):
    the_menu = Menu.query.filter_by(id=menu_id).first()
    form = EditMenuForm()

    if the_menu is None:
        abort(404)

    if form.validate_on_submit():
        the_menu.name = form.name.data

        db.session.add(menu)
        flash("{0} has been saved".format(the_menu.name))

        return redirect(url_for('.menus'))

    form.name.data = the_menu.name

    menu_items = the_menu.menu_items.order_by(MenuItem.weight)

    return render_template('admin/menus/menu.html', js='menus/menu', form=form, menu=the_menu, menu_items=menu_items)


@admin.route('/menus/menu/new', methods=['GET', 'POST'])
@login_required
def add_menu():
    form = EditMenuForm()

    if form.validate_on_submit():
        the_menu = Menu()

        the_menu.name = form.name.data
        the_menu.created_on = datetime.utcnow()

        db.session.add(the_menu)
        flash("{0} has been created".format(the_menu.name))

        return redirect(url_for('.menus'))

    return render_template("admin/menus/new.html", js='menus/new', form=form)


@admin.route('/menus/menu/delete/<int:menu_id>')
@login_required
def delete_menu(menu_id):
    the_menu = Menu.query.filter_by(id=menu_id).first()

    if the_menu is not None:
        # Delete all menu items within this menu
        for item in the_menu.menu_items.all():
            db.session.delete(item)

        db.session.delete(the_menu)

        flash("{0} has been deleted".format(menu.name))
        return redirect(url_for(".menus"))

    flash("That menu does not exist")
    return redirect(url_for(".menus"))


@admin.route('/menus/menu/<int:menu_id>/menu-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def menu_item(menu_id, item_id):
    the_menu_item = MenuItem.query.filter_by(menu_id=menu_id, id=item_id).first()
    form = EditMenuItemForm()

    if form.validate_on_submit():
        the_menu_item.name = form.name.data
        the_menu_item.slug = form.slug.data
        the_menu_item.menu_id = form.menu.data
        the_menu_item.weight = form.weight.data

        items = MenuItem.query.filter_by(menu_id=menu_id, name=the_menu_item.name).all()
        for item in items:
            if item.id != the_menu_item.id:
                flash("Menu Item can't use the same name as another item in the same menu")
                return render_template("admin/menus/menu-item/menu-item.html", form=form, menu_item=the_menu_item)

        db.session.add(the_menu_item)
        flash("{0} has been saved".format(the_menu_item.name))

        return redirect(url_for(".menu", menu_id=the_menu_item.menu_id))

    form.name.data = the_menu_item.name
    form.slug.data = the_menu_item.slug
    form.menu.data = the_menu_item.menu_id
    form.weight.data = the_menu_item.weight

    return render_template("admin/menus/menu-item/menu-item.html", js='menus/menu-item/menu-item', form=form,
                           menu_item=the_menu_item)


@admin.route("/menus/menu/<int:menu_id>/menu-item/new", methods=['GET', 'POST'])
@login_required
def add_menu_item(menu_id):
    form = EditMenuItemForm()
    the_menu = Menu.query.filter_by(id=menu_id).first()

    if form.validate_on_submit():
        the_menu_item = MenuItem()

        the_menu_item.name = form.name.data
        the_menu_item.slug = form.slug.data
        the_menu_item.weight = form.weight.data
        the_menu_item.menu_id = form.menu.data
        the_menu_item.created_on = datetime.utcnow()

        items = MenuItem.query.filter_by(menu_id=menu_id, name=the_menu_item.name).all()
        if len(items) > 0:
            flash("Menu Item can't use the same name as another item in the same menu")
            return render_template("admin/menus/menu-item/menu-item.html", form=form, menu_item=the_menu_item)

        db.session.add(the_menu_item)
        flash("{0} has been created".format(the_menu_item.name))

        return redirect(url_for(".menu", menu_id=the_menu_item.menu_id))

    form.menu.data = menu_id

    return render_template("admin/menus/menu-item/new.html", js='menus/menu-item/new', form=form, menu=the_menu)


@admin.route("/menus/menu/<int:menu_id>/menu-item/delete/<int:item_id>")
@login_required
def delete_menu_item(menu_id, item_id):
    the_menu_item = MenuItem.query.filter_by(menu_id=menu_id, id=item_id).first()

    if the_menu_item is not None:
        db.session.delete(the_menu_item)

        flash("{0} has been deleted".format(the_menu_item.name))
        return redirect(url_for(".menu", menu_id=menu_id))

    flash("That menu item doesn't exist")
    return redirect(url_for(".menu", menu_id=menu_id))
