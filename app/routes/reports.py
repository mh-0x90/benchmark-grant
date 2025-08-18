import os
from flask import Blueprint, request, redirect
from werkzeug.utils import secure_filename

bp = Blueprint('reports', __name__, url_prefix='/reports')
REPORT_UPLOAD_FOLDER = 'app/static/reports/' 
ALLOWED_REPORT_EXTENSIONS = {'pdf', 'docx', 'txt', 'csv', 'bat'} 

def is_report_allowed(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext in ALLOWED_REPORT_EXTENSIONS

@bp.route('/upload_report', methods=['POST'])
def upload_report():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return "No file uploaded.", 400

    filename = secure_filename(uploaded_file.filename)

    if not is_report_allowed(filename):
        return "Unsupported report type.", 400

    uploaded_file.seek(0, os.SEEK_END)  
    file_size = uploaded_file.tell() 
    uploaded_file.seek(0)  
    if file_size > 10240:
        return "File size exceeds 10 KB limit.", 400

    save_path = os.path.join(REPORT_UPLOAD_FOLDER, filename)
    uploaded_file.save(save_path)

    return redirect('/dashboard/home')