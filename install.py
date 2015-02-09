from datetime import datetime
from app import db
from app.models import User, Role, Menu, MenuItem, Page, BlogPost, BlogCategory, PhotoGallery, PhotoGalleryItem


def install_with_sample_content(email):
    """Adds all default and sample data to database

    Creates default and sample data and inserts into the database. Including Users, Roles, Pages, a Blog Post (along
    with a default category), and Photo Gallery with Items.
    """

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

    homeMenuItem = MenuItem()
    homeMenuItem.name = 'Home'
    homeMenuItem.slug = '/'
    homeMenuItem.created_on = datetime.utcnow()
    homeMenuItem.menu = menu
    db.session.add(homeMenuItem)

    aboutMenuItem = MenuItem()
    aboutMenuItem.name = 'About'
    aboutMenuItem.slug = '/about-me'
    aboutMenuItem.created_on = datetime.utcnow()
    aboutMenuItem.menu = menu
    db.session.add(aboutMenuItem)

    # Pages
    homePage = Page()
    homePage.title = 'Index'
    homePage.content = """# Lorem ipsum
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
    homePage.is_homepage = True
    homePage.created_on = datetime.utcnow()
    homePage.published_on = datetime.utcnow()
    homePage.slug = 'index'
    homePage.user = user
    db.session.add(homePage)

    aboutPage = Page()
    aboutPage.title = 'About Me'
    aboutPage.slug = 'about-me'
    aboutPage.content = """This is the about page. It's lots of fun! You can learn about me. For instance:
    - I love the internet
    - I'm typing this right now
    - This is our land (Yes it is!)
    """
    aboutPage.created_on = datetime.utcnow()
    aboutPage.published_on = datetime.utcnow()
    aboutPage.user = user
    aboutPage.is_homepage = True
    db.session.add(aboutPage)

    # Blog Stuff
    blogCategory = BlogCategory()
    blogCategory.name = "Uncategorized"
    blogCategory.description = "All uncategorized posts"
    blogCategory.created_on = datetime.utcnow()
    db.session.add(blogCategory)

    blogPost = BlogPost()
    blogPost.title = "Hello World!"
    blogPost.content = """### This is my first post.
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
    blogPost.slug = "hello-world"
    blogPost.created_on = datetime.utcnow()
    blogPost.published_on = datetime.utcnow()
    blogPost.blogcategory = blogCategory
    blogPost.user = user
    db.session.add(blogPost)

    db.session.commit()

    return