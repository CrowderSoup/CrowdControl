from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required, current_user
from . import admin
from app import db
from app.models.BlogPost import BlogPost
from app.models.BlogCategory import BlogCategory
from app.admin.forms.PostForm import PostForm
from app.admin.forms.EditCategoryForm import EditCategoryForm


@admin.route('/blog/posts', defaults={'page': 1})
@admin.route('/blog/posts/<int:page>')
@login_required
def blog_posts(page):
    the_posts = BlogPost.query.order_by(BlogPost.published_on.desc()).paginate(page, 5)
    return render_template('admin/blog/posts/posts.html', js='posts/index', posts=the_posts)


@admin.route('/blog/posts/post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):
    form = PostForm()
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is None:
        abort(404)

    if form.validate_on_submit():
        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data
        post.blogcategory_id = form.category.data

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('.blog_posts'))

    form.slug.data = post.slug
    form.title.data = post.title
    form.content.data = post.content
    form.published_on.data = post.published_on
    form.category.data = post.blogcategory_id

    return render_template('admin/blog/posts/edit_post.html', js='posts/edit_post', form=form, post=post)


@admin.route('/blog/posts/new', methods=['GET', 'POST'])
@login_required
def add_blog_post():
    form = PostForm()

    if form.validate_on_submit():
        post = BlogPost()

        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data
        post.user_id = current_user.id
        post.created_on = datetime.utcnow()
        post.blogcategory_id = form.category.data

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('.blog_posts'))

    return render_template('admin/blog/posts/add_post.html', js='posts/add_post', form=form)


@admin.route('/blog/posts/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_blog_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is not None:
        db.session.delete(post)

        flash('"{0}" has been deleted.'.format(post.title))
        return redirect(url_for('.blog_posts'))

    flash('Post does not exist')
    return redirect(url_for('.blog_posts'))


@admin.route('/blog/categories', defaults={'page': 1})
@admin.route('/blog/categories/<int:page>')
@login_required
def blog_categories(page):
    the_categories = BlogCategory.query.order_by(BlogCategory.name).paginate(page, 5)
    return render_template('admin/blog/categories/categories.html', categories=the_categories)


@admin.route('/blog/categories/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_blog_category(category_id):
    form = EditCategoryForm()
    category = BlogCategory.query.filter_by(id=category_id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data

        db.session.add(category)
        flash('"{0}" has been saved'.format(category.name))

        return redirect(url_for('.blog_categories'))

    form.name.data = category.name
    form.slug.data = category.slug
    form.description.data = category.description

    return render_template('admin/blog/categories/edit_category.html', js='posts/add_edit_category', form=form,
                           category=category)


@admin.route('/blog/categories/new', methods=['GET', 'POST'])
@login_required
def add_blog_category():
    form = EditCategoryForm()

    if form.validate_on_submit():
        category = BlogCategory()

        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        category.created_on = datetime.utcnow()

        db.session.add(category)
        flash('"{0}" has been saved'.format(category.name))

        return redirect(url_for('.blog_categories'))

    return render_template('admin/blog/categories/add_category.html', js='posts/add_edit_category', form=form)


@admin.route('/blog/categories/delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
def delete_blog_category(category_id):
    category = BlogCategory.query.filter_by(id=category_id).first()

    if category is not None:
        db.session.delete(category)

        flash('"{0}" has been deleted'.format(category.name))
        return redirect(url_for('.blog_categories'))

    flash('Category does not exist')
    return redirect('.blog_categories')
