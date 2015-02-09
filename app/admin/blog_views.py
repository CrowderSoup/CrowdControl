from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required, current_user
from . import admin
from ..models import db, BlogPost
from .forms import EditPostForm, AddPostForm

@admin.route('/posts')
@login_required
def posts():
    all_posts = BlogPost.query.all()
    return render_template('admin/posts/posts.html', posts=all_posts)


@admin.route('/posts/post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = EditPostForm()
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is None:
        abort(404)

    if form.validate_on_submit():
        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data

        # If the user isn't set, let's set it to the current user.
        if post.user_id is None:
            post.user_id = current_user.id

        # If created_on isn't set let's set it (this SHOULDN'T happen)
        if post.created_on is None:
            post.created_on = datetime.utcnow()

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('.posts'))

    form.slug.data = post.slug
    form.title.data = post.title
    form.content.data = post.content
    form.published_on.data = post.published_on

    return render_template('admin/posts/edit_post.html', form=form, post=post)


@admin.route('/posts/new', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()

    if form.validate_on_submit():
        post = BlogPost()

        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data
        post.user_id = current_user.id
        post.created_on = datetime.utcnow()

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('.posts'))

    return render_template('admin/posts/add_post.html', form=form)


@admin.route('/posts/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is not None:
        db.session.delete(post)

        flash('"{0}" has been deleted.'.format(post.title))
        return redirect(url_for('.posts'))

    flash('Page does not exist')
    return redirect(url_for('.posts'))