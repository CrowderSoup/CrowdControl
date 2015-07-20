# CrowdControl CMS
#### A Python-based CMS built with Flask
![GitLab CI](https://ci.gitlab.com/projects/4762/status.png?ref=master)

This is a simple Content Management system that's meant to be extendable.

### Features
1. CRUD for pages. A page can be marked as the "Index" page, meaning it will be
at the root of your site.
2. Blog with categories. Posts can be in a single category. Posts can be marked
as a draft, published, or deleted. Post can be scheduled for the future.
3. All content is written an edited in a really basic ACE editor. I'm using
CommonMark, which allows for HTML to accomplish complex layouts. It also allows
really simple writing in Markdown.
4. Menus. A contains menu items, which are links to pages the blog (or even blog
posts). Each page can select a different menu in case you want to do different
things with the menu on each page.
5. Really basic user management. You can add / edit users. You can add / edit
Roles, but the roles don't do anything yet.
6. Site Settings are a key/value store. This allows you to have different
settings for things on the front-end. Things like "What menu should be used for
the blog?", or "How many blog posts should be displayed per page?", or even the
site name if you want to make that dynamic. You can add / edit / delete to your
hearts content. But settings are used in the front-end so if you're not careful
you could break something.

### Roadmap
1. Add content blocks that can be added to any page.
2. Add tags for blog posts
3. Make menu items more flexible (allow adding an item that links to an external
site for instance)
4. Access management via roles. Allow an admin to set access to different parts
of the site based on custom roles
5. Add asset / media management functionality so that images (or any file really)
can be uploaded and used in pages / blogs.
6. Build out admin dashboard. I'm not really sure what I want to do here, but I
want to make it customizable.
