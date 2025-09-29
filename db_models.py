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
    __tablename__ = 'shipmentheader'
    id = db.Column(db.Integer, primary_key=True)
    suppliername = db.Column(db.String(255), nullable=False)
    shipmentno = db.Column(db.String(100), nullable=False)
    datereceived = db.Column(db.Date, nullable=False)
    comments = db.Column(db.Text)
    details = db.relationship('ShipmentDetail', backref='header', cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='header', cascade="all, delete-orphan")

class ShipmentDetail(db.Model):
    __tablename__ = 'shipmentdetail'
    id = db.Column(db.Integer, primary_key=True)
    shipmentheaderid = db.Column(db.Integer, db.ForeignKey('shipmentheader.id'), nullable=False)
    description = db.Column(db.Text)
    sku = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unitprice = db.Column(db.Numeric(18,2))
    comments = db.Column(db.Text)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    shipmentheaderid = db.Column(db.Integer, db.ForeignKey('shipmentheader.id'), nullable=False)
    paymentdate = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(18,2), nullable=False)
    fee = db.Column(db.Numeric(18,2), nullable=False)
    comments = db.Column(db.Text)

class Products(db.Model):
    __tablename__ = 'products'
    productcode = db.Column(db.String, primary_key=True)
    productcategory = db.Column(db.String, nullable=False)
    productdesc = db.Column(db.String, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    productcost = db.Column(db.Numeric(18,2), nullable=False)
    comments = db.Column(db.Text)
