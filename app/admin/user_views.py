from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required
from . import admin
from app import db
from app.models.User import User
from app.models.Role import Role
from app.admin.forms.EditUserForm import EditUserForm
from app.admin.forms.AddUserForm import AddUserForm


@admin.route('/users')
@login_required
def users():
    all_users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/users/index.html', users=all_users, roles=roles)


@admin.route('/users/user/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = EditUserForm(user=user)

    if user is None:
        abort(404)

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role_id = form.role.data

        if form.password.data != "":
            user.password = form.password.data

        db.session.add(user)
        flash('"{0}" has been saved'.format(user.username))

        return redirect(url_for('.users'))

    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id

    return render_template('admin/users/edit_user.html', form=form, user=user)


@admin.route('/users/new', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()

    if form.validate_on_submit():
        user = User()

        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        user.role_id = form.role.data
        user.created_on = datetime.utcnow()

        db.session.add(user)
        flash('"{0}" has been added'.format(user.username))

        return redirect(url_for('.users'))

    return render_template('admin/users/add_user.html', form=form)


@admin.route('/users/delete/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is not None:
        db.session.delete(user)

        flash('"{0}" has been deleted.'.format(user.username))
        return redirect(url_for('.users'))

    flash('User does not exist')
    return redirect(url_for('.users'))
