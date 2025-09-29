from main import db

class Orders(db.Model):
    __tablename__ = 'orders'
    order_no = db.Column(db.String(100), primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100))
    source = db.Column(db.String(100))
    platform = db.Column(db.String(100))
    order_amount = db.Column(db.Numeric(18,2))
    sales_tax = db.Column(db.Numeric(18,2))
    comments = db.Column(db.Text)

class ShipmentHeader(db.Model):
    __tablename__ = 'shipment_header'
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(255), nullable=False)
    shipment_no = db.Column(db.String(100), nullable=False)
    date_received = db.Column(db.Date, nullable=False)
    comments = db.Column(db.Text)
    details = db.relationship('ShipmentDetail', backref='header', cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='header', cascade="all, delete-orphan")

class ShipmentDetail(db.Model):
    __tablename__ = 'shipment_detail'
    id = db.Column(db.Integer, primary_key=True)
    shipment_header_id = db.Column(db.Integer, db.ForeignKey('shipment_header.id'), nullable=False)
    description = db.Column(db.Text)
    sku = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric(18,2))
    comments = db.Column(db.Text)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    shipment_header_id = db.Column(db.Integer, db.ForeignKey('shipment_header.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(18,2), nullable=False)
    fee = db.Column(db.Numeric(18,2), nullable=False)
    comments = db.Column(db.Text)

class Products(db.Model):
    __tablename__ = 'products'
    code = db.Column(db.String, primary_key=True)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Numeric(18,2), nullable=False)
    comments = db.Column(db.Text)
