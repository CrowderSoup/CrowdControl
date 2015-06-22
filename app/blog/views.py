from werkzeug.contrib.atom import AtomFeed
from flask import render_template, abort
from app.models.BlogPost import BlogPost
from app.models.BlogCategory import BlogCategory
from app.models.BlogPostStatus import BlogPostStatus
from app.models.Menu import Menu
from app.models.User import User
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

    for post in blog_posts.items:
        parsed = parser.parse(post.content)
        rendered = renderer.render(parsed)

        # Get username for by-line
        by = User.query.filter_by(id=post.user_id).first().username or "Unknown"

        posts.append({
            'title': post.title,
            'slug': post.slug,
            'published_on': post.published_on,
            'content': rendered,
            'by': by
        })

    # Let's return the page and menu items
    return render_template("blog/blog.html", menu=main_menu, blog_posts=blog_posts, posts=posts, categories=categories)


@blog.route('/blog/post/<path:slug>')
def blog_post(slug):
    # Get the menu we want to use for this page...
    # TODO: make this more dynamic... probably tie it to the page
    main_menu = Menu.query.filter_by(name="Main").first()

    the_post = BlogPost.query.filter_by(slug=slug).first()

    if the_post is None:
        abort(404)

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    parsed = parser.parse(the_post.content)
    rendered = renderer.render(parsed)

    # Get username for by-line
    by = User.query.filter_by(id=the_post.user_id).first().username or "Unknown"

    post = {
        'title': the_post.title,
        'slug': the_post.slug,
        'published_on': the_post.published_on,
        'content': rendered,
        'by': by
    }

    return render_template("blog/blog_post.html", menu=main_menu, blog_post=post, category=None)


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

    for post in blog_posts.items:
        parsed = parser.parse(post.content)
        rendered = renderer.render(parsed)

        # Get username for by-line
        by = User.query.filter_by(id=post.user_id).first().username or "Unknown"

        posts.append({
            'title': post.title,
            'slug': post.slug,
            'published_on': post.published_on,
            'content': rendered,
            'by': by
        })

    # Let's return the page and menu items
    return render_template("blog/blog.html", menu=main_menu, blog_posts=blog_posts,
                           posts=posts, categories=categories, category=category)


@blog.route('/blog/feed.atom')
def blog_feed():
    root_url = 'http://crowdersoup.com/blog'
    feed = AtomFeed('CrowderSoup.com Blog',
                    feed_url='{0}/feed.atom'.format(root_url),
                    url=root_url)

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    blog_posts = BlogPost.query.order_by(BlogPost.published_on.desc()).paginate(1, 5)
    for post in blog_posts.items:
        parsed = parser.parse(post.content)
        rendered = renderer.render(parsed)

        # Get username for by-line
        by = User.query.filter_by(id=post.user_id).first().username or "Unknown"

        feed.add(post.title, rendered,
                 content_type='html',
                 author=by,
                 url='{0}/{1}'.format(root_url, post.slug),
                 updated=post.published_on,
                 published=post.published_on)

    return feed.get_response()