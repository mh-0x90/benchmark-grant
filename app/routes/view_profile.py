from flask import Blueprint, request, render_template_string, session, redirect, url_for

bp = Blueprint('profile', __name__, url_prefix='/profile')

_users = {
    1: {'username': 'alice', 'email': 'alice@example.com', 'bio': 'Alice loves coding!'},
    2: {'username': 'bob', 'email': 'bob@example.com', 'bio': 'Bob is a designer.'},
    3: {'username': 'charlie', 'email': 'charlie@example.com', 'bio': 'Charlie enjoys hiking.'}
}

def get_user_by_id(user_id):
    return _users.get(user_id)

def get_user_by_username(username):
    for user_id, user in _users.items():
        if user['username'] == username:
            return user_id, user
    return None, None


@bp.route('/<int:user_id>')
def view_profile(user_id):

    user = get_user_by_id(user_id)
    if not user:
        return "User not found.", 404
    return render_template_string('''
        <h1>Profile</h1>
        <p>Username: {{ user.username }}</p>
        <p>Email: {{ user.email }}</p>
        <p>Bio: {{ user.bio }}</p>
        <a href="{{ url_for('profile.login') }}">Login as another user</a>
    ''', user=user)