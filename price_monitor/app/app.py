from flask import Flask, jsonify
from price_monitor.db.database import db_connect, db_session
from price_monitor.db.models import Product, Price

app = Flask(__name__)


@app.route('/')
def index():
    session = db_session(db_connect())
    query = session.query(Product.name, Product.category).all()
    data = {}
    for item in query:
        category = data.get(item.category, [])
        category.append(item.name)
        data[item.category] = category
    return jsonify(**data)
