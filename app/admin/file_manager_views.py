import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort, request
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename
from . import admin
from app import db
import app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@admin.route('/file-manager')
def file_manager():
    return render_template('admin/file-manager/index.html',
                            js='file-manager/index')


@admin.route('/file-manager/upload', methods=['GET', 'POST'])
def upload_file():
    if(request.method == 'POST'):
        file = request.files['file']
        if(file and allowed_file(file.filename)):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DIR'], filename))

            flash('"{0}" has been saved'.format(filename))
            return redirect(url_for('.file_manager'))

    return render_template('admin/file-manager/upload.html',
                                js='file-manager/upload')
