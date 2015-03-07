import re
from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required, current_user
from . import admin
from ..models import db, Page
from .forms import PageForm

@admin.route('/pages')
@login_required
def pages():
    all_pages = Page.query.all()
    return render_template('admin/pages/pages.html', pages=all_pages)


@admin.route('/pages/page/<page_id>', methods=['GET', 'POST'])
@login_required
def edit_page(page_id):
    form = PageForm()
    page = Page.query.filter_by(id=page_id).first()

    if page is None:
        abort(404)

    if form.validate_on_submit():
        page.slug = form.slug.data
        page.title = form.title.data
        page.content = form.content.data
        page.published_on = form.published_on.data
        page.is_homepage = form.is_homepage.data
        page.menu_id = form.menu.data

        # Let's find out if there's another homepage right now. If so, let's unset that from the homepage
        if page.is_homepage:
            current_homepages = Page.query.filter_by(is_homepage=True).all()
            for current_homepage in current_homepages:
                # Is there already a homepage that isn't the page we're editing?
                if current_homepage is not None and current_homepage.id != page.id:
                    current_homepage.is_homepage = False

                    # We need to fix the slug
                    current_homepage.slug = re.sub(r'[^a-z0-9\s]', "", current_homepage.title.lower()).replace(" ", "-")

                    db.session.add(current_homepage)
                    db.session.commit()

            # If this is the homepage, we want to edit the slug to match
            page.slug = "/"

        db.session.add(page)
        flash('"{0}" has been saved'.format(page.title))

        return redirect(url_for('.pages'))

    form.slug.data = page.slug
    form.title.data = page.title
    form.content.data = page.content
    form.published_on.data = page.published_on
    form.is_homepage.data = page.is_homepage
    form.menu.data = page.menu_id

    return render_template('admin/pages/edit_page.html', form=form, page=page)


@admin.route('/pages/new', methods=['GET', 'POST'])
@login_required
def add_page():
    form = PageForm()

    if form.validate_on_submit():
        page = Page()

        page.slug = form.slug.data
        page.title = form.title.data
        page.content = form.content.data
        page.published_on = form.published_on.data
        page.user_id = current_user.id
        page.created_on = datetime.utcnow()
        page.is_homepage = form.is_homepage.data
        page.menu_id = form.menu.data

        # Let's find out if there's another homepage right now. If so, let's unset that from the homepage
        if page.is_homepage:
            current_homepages = Page.query.filter_by(is_homepage=True).all()
            for current_homepage in current_homepages:
                current_homepage.is_homepage = False

                # We need to fix the slug
                current_homepage.slug = re.sub(r'[^a-z0-9\s]', "", current_homepage.title.lower()).replace(" ", "-")

                db.session.add(current_homepage)
                db.session.commit()

            # If this is the homepage, we want to edit the slug to match
            page.slug = "/"

        db.session.add(page)
        flash('"{0}" has been saved'.format(page.title))

        return redirect(url_for('.pages'))

    return render_template('admin/pages/add_page.html', form=form)


@admin.route('/pages/delete/<page_id>', methods=['GET', 'POST'])
@login_required
def delete_page(page_id):
    page = Page.query.filter_by(id=page_id).first()

    if page is not None:
        db.session.delete(page)

        flash('"{0}" has been deleted.'.format(page.title))
        return redirect(url_for('.pages'))

    flash('Page does not exist')
    return redirect(url_for('.pages'))