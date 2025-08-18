from flask import Blueprint, request, render_template_string

bp = Blueprint('settings', __name__, url_prefix='/settings')

@bp.route('/update', methods=['POST'])
def update():
    email = request.form.get('email', '').strip()
    
    html = f"""
    <html>
        <head><title>Settings</title></head>
        <body>
            <h2>Update Successful</h2>
            <div>Your new email is: <span id="user-email">{email}</span></div>
            <a href="/dashboard/home">Return to Dashboard</a>
        </body>
    </html>
    """
    
    return render_template_string(html)
