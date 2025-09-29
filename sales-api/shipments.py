from flask import jsonify
from db_models import ShipmentHeader, ShipmentDetail, Payment
from main import db

def get_all_shipments_header():
    shipment_header = ShipmentHeader.query.all()
    return jsonify([
        {
            'id': p.id,
            'shipment_no': p.shipment_no,
            'supplie_rname': p.supplier_name,
            'date_received': p.date_received.isoformat(),
            'comments': p.comments
        } for p in shipment_header
    ])

def get_shipment_by_header_id(shipment_header_id):
    s = ShipmentHeader.query.get_or_404(shipment_header_id)
    return jsonify({
        'id': s.id,
        'supplier_name': s.supplier_name,
        'shipment_no': s.shipment_no,
        'date_received': s.date_received.isoformat(),
        'comments': s.comments
    })

#Get shipment details by header id
def get_shipment_details(shipment_header_id):
    details = ShipmentDetail.query.filter_by(shipment_header_id=shipment_header_id).all()
    return jsonify([
        {
            'id': d.id,
            'shipment_header_id': d.shipment_header_id,
            'description': d.description,
            'sku': d.sku,
            'quantity': d.quantity,
            'unit_price': float(d.unit_price),
            'comments': d.comments
        } for d in details
    ])

def add_shipment_header(data:any)->int:
    shipment = ShipmentHeader(
        suppliername=data.get('supplier_name'),
        shipmentno=data.get('shipment_no'),
        datereceived=data.get('date_received'),
        comments=data.get('comments')
    )
    db.session.add(shipment)
    db.session.commit()
    return jsonify(shipment.id)

def add_new_shipment_detail(shipment_header_id, detail):
    """
    Accepts either a single detail dict or a list of detail dicts.
    Returns a list of inserted detail IDs.
    """
    add_shipment_details = ShipmentDetail(
        shipment_header_id=shipment_header_id,
        description=detail.get('description'),
        sku=detail.get('sku'),
        quantity=detail.get('quantity'),
        unit_price=detail.get('unit_price'),
        comments=detail.get('comments')
    )

    db.session.add(add_shipment_details)      
    db.session.commit()

    return jsonify(shipment_header_id)

def get_all_payments():
    payments = Payment.query.all()
    return jsonify([
        {
            'id': p.id,
            'shipment_header_id': p.shipment_header_id,
            'payment_date': p.payment_date.isoformat(),
            'description': p.description,
            'amount': float(p.amount),
            'fee': float(p.fee),
        }
        for p in payments
    ])

def get_payments_by_shipment_header_id(shipment_header_id):
    payments = Payment.query.filter_by(shipment_header_id=shipment_header_id).all()
    return jsonify([
        {
            'id': p.id,
            'shipment_header_id': p.shipment_header_id,
            'payment_date': p.payment_date.isoformat() if p.payment_date else None,
            'description': p.description,
            'amount': float(p.amount) if p.amount is not None else None,
            'fee': float(p.fee) if p.fee is not None else None,
            'comments': p.comments
        } for p in payments
    ])


def add_new_payment(shipment_header_id,data)->int:
    payment = Payment(
        shipment_header_id=shipment_header_id,
        payment_date=data['payment_date'],
        description=data['description'],
        amount=data['amount'],
        fee=data['fee'],
        comments=data.get('comments')
    )

    db.session.add(payment)      
    db.session.commit()

    return jsonify(payment.id)