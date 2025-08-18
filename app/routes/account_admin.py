import os
import hashlib
from flask import Blueprint, request, redirect, make_response, render_template

bp = Blueprint('account_admin', __name__, url_prefix='/admin')

ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASS = os.getenv('ADMIN_PASS')

if not ADMIN_USER or not ADMIN_PASS:
    raise ValueError("ADMIN_USER and ADMIN_PASS environment variables must be set")

ADMIN_PASS_HASH = hashlib.md5(ADMIN_PASS.encode()).hexdigest()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.md5(password.encode()).hexdigest()
        if username == ADMIN_USER and password_hash == ADMIN_PASS_HASH:
            resp = make_response(redirect('/dashboard/home'))
            resp.set_cookie('admin_user', username)
            resp.set_cookie('admin_pass', password)
            return resp
    return render_template('login_admin.html')