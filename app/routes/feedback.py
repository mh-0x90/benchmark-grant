import logging
from flask import Blueprint, request, render_template_string, redirect, url_for, session

# Configure logging to write to a file
logging.basicConfig(
    filename='feedback.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@bp.route('/submit', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        user_message = request.form.get('message', '')

        session['latest_feedback'] = user_message

        logging.info(f"User feedback: {user_message}")

        return redirect(url_for('feedback.thank_you'))

    return render_template_string('''
        <form method="post" action="/feedback/submit">
            <textarea name="message"></textarea>
            <button type="submit">Submit</button>
        </form>
    ''')

@bp.route('/thank-you')
def thank_you():
    feedback = session.get('latest_feedback', '')
    return render_template_string(f'''
        <h1>Thank You!</h1>
        <p>Your feedback: {feedback}</p>
        <a href="/feedback/submit">Submit more</a>
    ''')