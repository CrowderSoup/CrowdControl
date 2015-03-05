from flask import render_template, abort
from ..models import BlogPost, BlogCategory, Menu, User
from . import blog
import CommonMark


@blog.route('/blog', defaults={'page': 1})
@blog.route('/blog/<int:page>')
def the_blog(page):
    # Get the menu we want to use for this page...
    # TODO: make this more dynamic... probably tie it to the page
    main_menu = Menu.query.filter_by(name="Main").first()

    blog_posts = BlogPost.query.order_by(BlogPost.published_on.desc()).paginate(page, 5)
    categories = BlogCategory.query.all()

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    posts = []

    for blogPost in blog_posts.items:
        parsed = parser.parse(blogPost.content)
        rendered = renderer.render(parsed)

        # Get username for by-line
        by = User.query.filter_by(id=blogPost.user_id).first().username or "Unknown"

        posts.append({
            'title': blogPost.title,
            'slug': blogPost.slug,
            'published_on': blogPost.published_on,
            'content': rendered,
            'by': by
        })

    # Let's return the page and menu items
    return render_template("blog/blog.html", menu=main_menu, blogPosts=blog_posts, posts=posts, categories=categories)


@blog.route('/blog/post/<path:slug>')
def blog_post(slug):
    # Get the menu we want to use for this page...
    # TODO: make this more dynamic... probably tie it to the page
    mainMenu = Menu.query.filter_by(name="Main").first()

    blogPost = BlogPost.query.filter_by(slug=slug).first()

    if blogPost is None:
        abort(404)

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    parsed = parser.parse(blogPost.content)
    rendered = renderer.render(parsed)

    # Get username for by-line
    by = User.query.filter_by(id=blogPost.user_id).first().username or "Unknown"

    post = {
        'title': blogPost.title,
        'slug': blogPost.slug,
        'published_on': blogPost.published_on,
        'content': rendered,
        'by': by
    }

    return render_template("blog/blog_post.html", menu=mainMenu, blogPost=post)


@blog.route('/blog/category/<path:slug>', defaults={'page': 1})
@blog.route('/blog/category/<path:slug>/<int:page>')
def blog_category(slug, page):
    category = BlogCategory.query.filter_by(slug=slug).first()

    if category is None:
        abort(404)

    # Get the menu we want to use for this page...
    # TODO: make this more dynamic... probably tie it to the page
    main_menu = Menu.query.filter_by(name="Main").first()

    blog_posts = BlogPost.query.filter_by(blogcategory_id=category.id)\
        .order_by(BlogPost.published_on.desc()).paginate(page, 5)
    categories = BlogCategory.query.all()

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    posts = []

    for blogPost in blog_posts.items:
        parsed = parser.parse(blogPost.content)
        rendered = renderer.render(parsed)

        # Get username for by-line
        by = User.query.filter_by(id=blogPost.user_id).first().username or "Unknown"

        posts.append({
            'title': blogPost.title,
            'slug': blogPost.slug,
            'published_on': blogPost.published_on,
            'content': rendered,
            'by': by
        })

    # Let's return the page and menu items
    return render_template("blog/blog.html", menu=main_menu, blogPosts=blog_posts, posts=posts, categories=categories)