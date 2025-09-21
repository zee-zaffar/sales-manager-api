import psycopg2
from app import app, db
from flask import request, jsonify
from models import ShipmentHeader, ShipmentDetail, Payment
from datetime import datetime
from db_connection import create_connection

@app.route('/shipments', methods=['GET'])
def get_shipments():
    try:
        connection = create_connection()
        cursor = connection.cursor()
     
        cursor.execute("SELECT ID, SupplierName, ShipmentNo, DateReceived, Comments FROM ShipmentHeader ORDER BY DateReceived DESC;")
        shipments = [
            {
                'ID': row[0],
                'SupplierName': row[1],
                'ShipmentNo': row[2],
                'DateReceived': row[3],
                'Comments': row[4]
            }
            for row in cursor.fetchall()
        ]
        print(f"Total shipments found: {len(shipments)}")
        return jsonify(shipments)
    
    except psycopg2.Error as db_error:
        print(f"Database Error: {db_error}")

    except Exception as error:
        print(f"General Exception Error:{error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/shipments', methods=['POST'])
def create_shipment():
    data = request.json
    shipment = ShipmentHeader(
        supplier_name=data['supplier_name'],
        shipment_no=data['shipment_no'],
        date_received=datetime.strptime(data['date_received'], '%Y-%m-%d').date(),
        comments=data.get('comments')
    )
    db.session.add(shipment)
    db.session.commit()
    return jsonify({'id': shipment.id}), 201

@app.route('/shipments/<int:shipment_id>', methods=['GET'])
def get_shipment(shipment_id):
    s = ShipmentHeader.query.get_or_404(shipment_id)
    return jsonify({
        'id': s.id,
        'supplier_name': s.supplier_name,
        'shipment_no': s.shipment_no,
        'date_received': s.date_received.isoformat(),
        'comments': s.comments
    })

@app.route('/shipments/<int:shipment_id>/details', methods=['GET'])
def get_shipment_details(shipment_id):
    details = ShipmentDetail.query.filter_by(shipmentheaderid=shipment_id).all()
    return jsonify([
        {
            'id': d.id,
            'description': d.description,
            'sku': d.sku,
            'quantity': d.quantity,
            'unit_price': float(d.unit_price),
            'comments': d.comments
        } for d in details
    ])

@app.route('/shipments/<int:shipment_id>/details', methods=['POST'])
def add_shipment_detail(shipment_id):
    data = request.json
    detail = ShipmentDetail(
        shipmentheaderid=shipment_id,
        description=data['description'],
        sku=data['sku'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        comments=data.get('comments')
    )
    db.session.add(detail)
    db.session.commit()
    return jsonify({'id': detail.id}), 201

@app.route('/payments', methods=['POST'])
def add_payment():
    data = request.json
    payment = Payment(
        shipmentheaderid=data['shipmentheaderid'],
        paymentdate=datetime.strptime(data['paymentdate'], '%Y-%m-%d').date(),
        description=data['description'],
        amount=data['amount'],
        fee=data['fee'],
        comments=data.get('comments')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'id': payment.id}), 201

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([
        {
            'id': p.id,
            'shipmentheaderid': p.shipmentheaderid,
            'paymentdate': p.paymentdate.isoformat(),
            'description': p.description,
            'amount': float(p.amount),
            'fee': float(p.fee),
            'comments': p.comments
        } for p in payments
    ])
