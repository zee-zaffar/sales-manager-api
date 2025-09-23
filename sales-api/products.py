from flask import jsonify
from models import Products
from main import db
from typing import Any

def get_all_products():
    products = Products.query.all()
    return jsonify([
        {
            'productcode': p.productcode,
            'productcategory': p.productcategory,
            'productdesc': p.productdesc,
            'color': p.color,
            'productcost': float(p.productcost),
            'comments': p.comments
        } for p in products
    ])

def add_new_product(data: Any) -> int:
    product = Products(
        productcode=data.get('productcode'),
        productcategory=data.get('productcategory'),
        productdesc=data.get('productdesc'),
        color=data.get('color'),
        productcost=float(data.get('productcost')) if data.get('productcost') is not None else None,
        comments=data.get('comments')
    )
    db.session.add(product)
    db.session.commit()
    return product.productcode