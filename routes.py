from models import Products
import psycopg2
from main import app, db
from flask import request, jsonify
from models import ShipmentHeader, ShipmentDetail, Payment
from datetime import datetime
from db_connection import create_connection
from products import get_all_products, add_new_product
from shipments import get_all_shipments_header, get_all_payments, get_payments_by_shipment_header_id, get_shipment_by_header_id, add_shipment_header, add_new_shipment_detail, get_shipment_details, add_new_payment

@app.route('/shipments', methods=['GET'])
def get_shipments():
    return get_all_shipments_header()

#Add new shipment
@app.route('/shipments', methods=['POST'])
def add_new_shipment():
    payload = request.json
    shipment_header_id = shipment_header_id =  add_shipment_header(payload)
    print ("New Shipment Header ID:", shipment_header_id)

    # Loop through details and add each one
    for shipment_detail in payload.get('Details'):
        add_new_shipment_detail(shipment_header_id, shipment_detail)
  
    return jsonify({'id': shipment_header_id}), 201

@app.route('/shipments/<int:shipment_header_id>', methods=['GET'])
def get_shipment(shipment_header_id):
   return get_shipment_by_header_id(shipment_header_id)

#Get shipment details by header id
@app.route('/shipments/<int:shipment_header_id>/details', methods=['GET'])
def shipment_details(shipment_header_id:int):
    return get_shipment_details(shipment_header_id)

# Add new shipment detail
@app.route('/shipments/<int:shipment_header_id>/details', methods=['POST'])
def add_shipment_detail(shipment_header_id: int):
    shipment_detail = request.json
    return add_new_shipment_detail(shipment_header_id, shipment_detail)

# Add new payment
@app.route('/payments', methods=['POST'])
def add_payment(shipment_header_id: int):
    payment = request.json
    payment_id = add_new_payment(shipment_header_id, payment)
    return jsonify({'id': payment_id}), 201

#Get all payments
@app.route('/payments', methods=['GET'])
def get_payments():
    return get_all_payments()

#Get all products
@app.route('/products', methods=['GET'])
def get_products():
    return get_all_products()

@app.route('/shipments/<int:shipment_header_id>/payments', methods=['GET'])
def get_payments_for_shipment(shipment_header_id: int):
    return get_payments_by_shipment_header_id(shipment_header_id)

# Route to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    print("Received data for new product:", data)
    product_code =  add_new_product(data)
    return jsonify({'product_code': product_code}), 201
    

