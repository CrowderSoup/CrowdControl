from datetime import datetime
from app import db
from app.models.SiteSetting import SiteSetting
from app.models.User import User
from app.models.Role import Role
from app.models.Menu import Menu
from app.models.MenuItem import MenuItem
from app.models.Page import Page
from app.models.BlogPost import BlogPost
from app.models.BlogCategory import BlogCategory
from app.models.BlogPostStatus import BlogPostStatus



def install_with_sample_content(email):
    """Adds all default and sample data to database

    Creates default and sample data and inserts into the database. Including Users, Roles, Pages, a Blog Post (along
    with a default category), and Photo Gallery with Items.
    """

    # Site Settings
    ss_posts_per_page = SiteSetting()
    ss_posts_per_page.name = 'blog_posts_per_page'
    ss_posts_per_page.value = '5'
    db.session.add(ss_posts_per_page)

    ss_blog_menu = SiteSetting()
    ss_blog_menu.name = 'blog_menu'
    ss_blog_menu.value = '1'
    db.session.add(ss_blog_menu)

    # Roles
    role = Role()
    role.name = 'Admin'
    role.created_on = datetime.utcnow()
    db.session.add(role)

    # Users
    user = User()
    user.email = email
    user.username = 'Admin'
    user.password = 'P@ssw0rd'
    user.role = role
    user.created_on = datetime.utcnow()
    db.session.add(user)

    # Menus
    menu = Menu()
    menu.name = 'Main'
    menu.created_on = datetime.utcnow()
    db.session.add(menu)

    homemenuitem = MenuItem()
    homemenuitem.name = 'Home'
    homemenuitem.slug = '/'
    homemenuitem.created_on = datetime.utcnow()
    homemenuitem.menu = menu
    db.session.add(homemenuitem)

    # Committing the session so that we ge a menu id
    db.session.commit()

    aboutmenuitem = MenuItem()
    aboutmenuitem.name = 'About'
    aboutmenuitem.slug = '/about-me'
    aboutmenuitem.created_on = datetime.utcnow()
    aboutmenuitem.menu = menu
    db.session.add(aboutmenuitem)

    # Pages
    homepage = Page()
    homepage.title = 'Index'
    homepage.content = """# Lorem ipsum
<div class="row">
    <div class="col-md-3">
        <div class="panel panel-default">
            <div class="panel-heading">
                <div class="panel-title">Lorem ipsum</div>
            </div>
            <div class="panel-body">
                Lorem ipsum dolor sit amet, eu sea nostrum reprimique, stet novum omnium et nam. Est ferri
                voluptatibus eu. Ne nam augue iriure molestie, eos id fierent sensibus suscipiantur, ad eam
                nonumes vocibus. Tota elaboraret at nec. Eos vide solet no, ex tale feugait eos. Est agam
                legendos ex.
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="panel panel-default">
            <div class="panel-heading">
                <div class="panel-title">Lorem ipsum</div>
            </div>
            <div class="panel-body">
                Lorem ipsum dolor sit amet, eu sea nostrum reprimique, stet novum omnium et nam. Est ferri
                voluptatibus eu. Ne nam augue iriure molestie, eos id fierent sensibus suscipiantur, ad eam
                nonumes vocibus. Tota elaboraret at nec. Eos vide solet no, ex tale feugait eos. Est agam
                legendos ex.
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="panel panel-default">
            <div class="panel-heading">
                <div class="panel-title">Lorem ipsum</div>
            </div>
            <div class="panel-body">
                Lorem ipsum dolor sit amet, eu sea nostrum reprimique, stet novum omnium et nam. Est ferri
                voluptatibus eu. Ne nam augue iriure molestie, eos id fierent sensibus suscipiantur, ad eam
                nonumes vocibus. Tota elaboraret at nec. Eos vide solet no, ex tale feugait eos. Est agam
                legendos ex.
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="panel panel-default">
            <div class="panel-heading">
                <div class="panel-title">Lorem ipsum</div>
            </div>
            <div class="panel-body">
                Lorem ipsum dolor sit amet, eu sea nostrum reprimique, stet novum omnium et nam. Est ferri
                voluptatibus eu. Ne nam augue iriure molestie, eos id fierent sensibus suscipiantur, ad eam
                nonumes vocibus. Tota elaboraret at nec. Eos vide solet no, ex tale feugait eos. Est agam
                legendos ex.
            </div>
        </div>
    </div>
</div>
    """
    homepage.is_homepage = True
    homepage.created_on = datetime.utcnow()
    homepage.published_on = datetime.utcnow()
    homepage.slug = 'index'
    homepage.user = user
    homepage.menu = menu
    db.session.add(homepage)

    aboutpage = Page()
    aboutpage.title = 'About Me'
    aboutpage.slug = 'about-me'
    aboutpage.content = """This is the about page. It's lots of fun! You can learn about me. For instance:
- I love the internet
- I'm typing this right now
- This is our land (Yes it is!)
    """
    aboutpage.is_homepage = False
    aboutpage.created_on = datetime.utcnow()
    aboutpage.published_on = datetime.utcnow()
    aboutpage.user = user
    aboutpage.menu = menu
    db.session.add(aboutpage)

    # Blog Stuff
    blogcategory = BlogCategory()
    blogcategory.name = "Uncategorized"
    blogcategory.slug = "uncategorized"
    blogcategory.description = "All uncategorized posts"
    blogcategory.created_on = datetime.utcnow()
    db.session.add(blogcategory)

    blogpoststatus_draft = BlogPostStatus()
    blogpoststatus_draft.name = "Draft"
    db.session.add(blogpoststatus_draft)

    blogpoststatus_published = BlogPostStatus()
    blogpoststatus_published.name = "Published"
    db.session.add(blogpoststatus_published)

    blogpoststatus_deleted = BlogPostStatus()
    blogpoststatus_deleted.name = "Deleted"
    db.session.add(blogpoststatus_deleted)

    blogpost = BlogPost()
    blogpost.title = "Hello World!"
    blogpost.content = """### This is my first post.
What do you think? I'm writing this with Markdown right now. Pretty neat, right? Markdown has several advantages
over a standard WYSIWYG editor like WordPress and Blogger user.

- You can write everything in plain text. This means you can use your favorite plain text editor (like notepad,
sublime text, textmate, text wrangler, atom, etc.) to write your posts and then copy/paste them here.
- You can inject HTML when needed to create complex layouts.
- Markdown let's you focus on the content, not the formatting.
- Markdown is simple and straightforward.

Some people find that there is a bit of a learning curve with markdown. However, with an hour of patience you'll
have it down pat. And from that point on it'll change your life.
    """
    blogpost.slug = "hello-world"
    blogpost.created_on = datetime.utcnow()
    blogpost.published_on = datetime.utcnow()
    blogpost.blogcategory = blogcategory
    blogpost.blogpoststatus = blogpoststatus_published
    blogpost.user = user
    db.session.add(blogpost)

    db.session.commit()

    return
