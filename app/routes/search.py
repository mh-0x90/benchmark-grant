from flask import Blueprint, request, render_template_string
from app import db

bp = Blueprint('search', __name__, url_prefix='/search')

def build_query(params):
    base = "SELECT * FROM products where 1=1 "
    filters = []

    for key, value in params.items():
        filters.append(f" AND {key} = '{value}'")

    return base + "".join(filters)

@bp.route('/items')
def items():
    params = {k: v for k, v in request.args.items() if k in ['category', 'brand', 'price']}
    
    query = build_query(params)

    results = db.engine.execute(query).fetchall()

    output = "<br>".join(str(row) for row in results)
    return render_template_string(output)
