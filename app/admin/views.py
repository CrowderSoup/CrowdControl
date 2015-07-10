import os
from flask import render_template
from flask.ext.login import login_required
from . import admin
import app.admin.page_views
import app.admin.blog_views
import app.admin.user_views
import  app.admin.menu_views
import app.admin.settings_views

@admin.route('/')
@login_required
def index():
    env = os.getenv('FLASK_CONFIG') or 'default'
    return render_template('admin/index.html', js='pages/index', env=env)
