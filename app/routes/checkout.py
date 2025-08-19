from flask import Blueprint, request, render_template_string, session, jsonify

bp = Blueprint('cart', __name__, url_prefix='/cart')

discount_codes = {
    'SAVE20': {'percent': 20, 'description': '20% off entire order'},
    'FIRST100': {'percent': 100, 'description': '100% off for first-time users'},
    'WELCOME10': {'percent': 10, 'description': '10% off for new customers'}
}

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session:
        session['cart'] = {'items': [{'name': 'Product A', 'price': 100.0}], 'total': 100.0, 'discounts_applied': []}

    if request.method == 'POST':
        discount_code = request.form.get('discount_code')
        if not discount_code:
            return jsonify({'error': 'No discount code provided'}), 400

        if discount_code in discount_codes:
            discount = discount_codes[discount_code]
            discount_percent = discount['percent']
            discount_amount = session['cart']['total'] * (discount_percent / 100)
            session['cart']['total'] -= discount_amount
            session['cart']['discounts_applied'].append({
                'code': discount_code,
                'amount': discount_amount,
                'description': discount['description']
            })
            session.modified = True
            return jsonify({
                'message': f'Discount {discount_code} applied',
                'new_total': session['cart']['total'],
                'discounts': session['cart']['discounts_applied']
            }), 200
        else:
            return jsonify({'error': 'Invalid discount code'}), 400

    return render_template_string('''
        <h1>Checkout</h1>
        <p>Cart Total: ${{ cart.total }}</p>
        <h3>Applied Discounts:</h3>
        <ul>
        {% for discount in cart.discounts_applied %}
            <li>{{ discount.description }} ({{ discount.code }}): -${{ discount.amount }}</li>
        {% endfor %}
        </ul>
        <form method="post">
            <label>Discount Code: <input type="text" name="discount_code"></label>
            <button type="submit">Apply Discount</button>
        </form>
        <p><a href="{{ url_for('cart.reset_cart') }}">Reset Cart</a></p>
    ''', cart=session['cart'])

@bp.route('/reset', methods=['GET'])
def reset_cart():
    session.pop('cart', None)
    return redirect(url_for('cart.checkout'))