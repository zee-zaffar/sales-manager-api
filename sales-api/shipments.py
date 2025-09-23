from flask import jsonify
from models import ShipmentHeader, ShipmentDetail, Payment
from main import db

def get_all_shipments_header():
    shipment_header = ShipmentHeader.query.all()
    return jsonify([
        {
            'id': p.id,
            'shipmentno': p.shipmentno,
            'suppliername': p.suppliername,
            'datereceived': p.datereceived.isoformat(),
            'comments': p.comments
        } for p in shipment_header
    ])

def get_shipment_by_header_id(shipment_header_id):
    s = ShipmentHeader.query.get_or_404(shipment_header_id)
    return jsonify({
        'id': s.id,
        'suppliername': s.suppliername,
        'shipmentno': s.shipmentno,
        'datereceived': s.datereceived.isoformat(),
        'comments': s.comments
    })

#Get shipment details by header id
def get_shipment_details(shipment_header_id):
    details = ShipmentDetail.query.filter_by(shipmentheaderid=shipment_header_id).all()
    return jsonify([
        {
            'id': d.id,
            'shipmentheaderid': d.shipmentheaderid,
            'description': d.description,
            'sku': d.sku,
            'quantity': d.quantity,
            'unitprice': float(d.unitprice),
            'comments': d.comments
        } for d in details
    ])

def add_shipment_header(data:any)->int:
    shipment = ShipmentHeader(
        suppliername=data.get('SupplierName'),
        shipmentno=data.get('ShipmentNo'),
        datereceived=data.get('DateReceived'),
        comments=data.get('Comments')
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
        shipmentheaderid=shipment_header_id,
        description=detail.get('Description'),
        sku=detail.get('SKU'),
        quantity=detail.get('Quantity'),
        unitprice=detail.get('UnitPrice'),
        comments=detail.get('Comments')
    )

    db.session.add(add_shipment_details)      
    db.session.commit()

    return jsonify(shipment_header_id)

def get_all_payments():
    payments = Payment.query.all()
    return jsonify([
        {
            'id': p.id,
            'shipmentheaderid': p.shipmentheaderid,
            'paymentdate': p.paymentdate.isoformat(),
            'description': p.description,
            'amount': float(p.amount),
            'fee': float(p.fee),
        }
        for p in payments
    ])

def get_payments_by_shipment_header_id(shipment_header_id):
    payments = Payment.query.filter_by(shipmentheaderid=shipment_header_id).all()
    return jsonify([
        {
            'id': p.id,
            'shipmentheaderid': p.shipmentheaderid,
            'paymentdate': p.paymentdate.isoformat() if p.paymentdate else None,
            'description': p.description,
            'amount': float(p.amount) if p.amount is not None else None,
            'fee': float(p.fee) if p.fee is not None else None,
            'comments': p.comments
        } for p in payments
    ])


def add_new_payment(shipment_header_id,data)->int:
    payment = Payment(
        shipmentheaderid=shipment_header_id,
        paymentdate=data['PaymentDate'],
        description=data['Description'],
        amount=data['Amount'],
        fee=data['Fee'],
        comments=data.get('Comments')
    )
    return jsonify(payment.id)