from flask import Flask, jsonify, Response
from price_monitor.db.database import db_connect, db_session
from price_monitor.db.models import Product
import json

app = Flask(__name__)


@app.route('/')
def index():
    session = db_session(db_connect())
    query = session.query(Product).all()
    buff = {}
    for item in query:
        category = buff.get(item.category, [])
        category.append({
            'id': item.id,
            'name': item.name,
            'rating': item.rating,
            'last_price': item.last_price,
            'on_last_scan': item.on_last_scan
        })
        buff[item.category] = category
    data = [{'name': k, 'products': v} for k, v in buff.iteritems()]
    session.close()
    return Response(json.dumps(data), mimetype='application/json')


@app.route('/p/<int:product_id>')
def get_product(product_id):
    session = db_session(db_connect())
    product = session.query(Product).get(product_id)
    data = {
        'id': product.id,
        'url': product.url,
        'name': product.name,
        'rating': product.rating,
        'last_price': product.last_price,
        'on_last_scan': product.on_last_scan,
        'prices': []
    }
    for price in product.prices:
        data['prices'].append({
            'value': price.value,
            'when_read': price.when_read
        })
    session.close()
    return jsonify(**data)
