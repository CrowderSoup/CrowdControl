from datetime import datetime
from werkzeug.contrib.atom import AtomFeed
from rfeed import *
from flask import render_template, abort, url_for, request, make_response
from app.models.BlogPost import BlogPost
from app.models.BlogCategory import BlogCategory
from app.models.Menu import Menu
from app.models.User import User
from app.models.SiteSetting import SiteSetting
from . import blog
import CommonMark


@blog.route('/blog', defaults={'page': 1})
@blog.route('/blog/<int:page>')
def the_blog(page):
    # Get all the site settings
    site_settings = SiteSetting.query.all()
    settings = {}
    for setting in site_settings:
        settings[setting.name] = setting.value

    # Get the menu we want to use for this page...
    if 'blog_menu' in settings and \
        settings['blog_menu'] is not None:
        main_menu = Menu.query.filter_by(id=int(settings['blog_menu'])).first()
    else:
        main_menu = Menu()

    blog_posts = BlogPost.query.filter(BlogPost.blogpoststatus_id == 2, \
                                    BlogPost.published_on <= datetime.utcnow())\
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
    return render_template("blog/blog.html", menu=main_menu, \
                            blog_posts=blog_posts, posts=posts, \
                            categories=categories, settings=settings)


@blog.route('/blog/post/<path:slug>')
def blog_post(slug):
    # Get all the site settings
    site_settings = SiteSetting.query.all()
    settings = {}
    for setting in site_settings:
        settings[setting.name] = setting.value

    # Get the menu we want to use for this page...
    if 'blog_menu' in settings and \
        settings['blog_menu'] is not None:
        main_menu = Menu.query.filter_by(id=int(settings['blog_menu'])).first()
    else:
        main_menu = Menu()

    the_post = BlogPost.query.filter_by(slug=slug).first()

    if the_post is None or the_post.blogpoststatus_id != 2:
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

    return render_template("blog/blog_post.html", menu=main_menu, \
                            blog_post=post, category=None, settings=settings)


@blog.route('/blog/category/<path:slug>', defaults={'page': 1})
@blog.route('/blog/category/<path:slug>/<int:page>')
def blog_category(slug, page):
    category = BlogCategory.query.filter_by(slug=slug).first()

    if category is None:
        abort(404)

    # Get all the site settings
    site_settings = SiteSetting.query.all()
    settings = {}
    for setting in site_settings:
        settings[setting.name] = setting.value

    # Get the menu we want to use for this page...
    if 'blog_menu' in settings and \
        settings['blog_menu'] is not None:
        main_menu = Menu.query.filter_by(id=int(settings['blog_menu'])).first()
    else:
        main_menu = Menu()

    blog_posts = BlogPost.query.filter(BlogPost.blogcategory_id == category.id, \
                                    BlogPost.blogpoststatus_id == 2,
                                    BlogPost.published_on <= datetime.utcnow())\
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
    return render_template("blog/blog.html", menu=main_menu, \
                            blog_posts=blog_posts, posts=posts, \
                            categories=categories, category=category, \
                            settings=settings)


@blog.route('/blog/feed.rss')
def blog_rss():
    root_url = '{0}blog'.format(request.url_root)
    feed = Feed(title = "CrowderSoup.com Blog",
                link = '{0}/feed.rss'.format(root_url),
                description = "This is the blog description",
                language = "en-US",
                lastBuildDate = datetime.utcnow(),
                items = [])

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    blog_posts = BlogPost.query.filter(BlogPost.blogpoststatus_id == 2, \
                                    BlogPost.published_on <= datetime.utcnow())\
        .order_by(BlogPost.published_on.desc()).paginate(1, 5)

    for post in blog_posts.items:
        parsed = parser.parse(post.content)
        rendered = renderer.render(parsed)

        #Get username for by-line
        by = User.query.filter_by(id=post.user_id).first().username or "Unknown"
        post_url = "{0}/post/{1}".format(root_url, post.slug)

        item = Item(title = post.title,
                    link = post_url,
                    description = '<![CDATA[{0}\r\n]]>'.format(rendered),
                    author = by,
                    guid = Guid(post_url),
                    pubDate = post.published_on)

        feed.items.append(item)

    response= make_response(feed.rss())
    response.headers["Content-Type"] = "application/xml"

    return response


@blog.route('/blog/feed.atom')
def blog_feed():
    root_url = '{0}/blog'.format(request.url_root)
    feed = AtomFeed('CrowderSoup.com Blog',
                    feed_url='{0}/feed.atom'.format(root_url),
                    url=root_url)

    # Markdown Parser and Renderer
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    blog_posts = BlogPost.query.filter(BlogPost.blogpoststatus_id == 2, \
                                    BlogPost.published_on <= datetime.utcnow())\
        .order_by(BlogPost.published_on.desc()).paginate(1, 5)

    for post in blog_posts.items:
        parsed = parser.parse(post.content)
        rendered = renderer.render(parsed)

        # Get username for by-line
        by = User.query.filter_by(id=post.user_id).first().username or "Unknown"

        feed.add(post.title, rendered,
                 content_type='html',
                 author=by,
                 url='{0}/post/{1}'.format(root_url, post.slug),
                 updated=post.published_on,
                 published=post.published_on)

    return feed.get_response()
