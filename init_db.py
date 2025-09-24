from main import db
from models import ShipmentHeader, ShipmentDetail, Payment

def init_db():
    db.create_all()
    print("Database tables created.")

if __name__ == "__main__":
    init_db()
