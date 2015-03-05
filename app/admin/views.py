import os
from flask import render_template
from flask.ext.login import login_required
from . import admin
from . import page_views
from . import blog_views
from . import user_views
from . import  menu_views

@admin.route('/')
@login_required
def index():
    env = os.getenv('FLASK_CONFIG') or 'default'
    return render_template('admin/index.html', env=env)
