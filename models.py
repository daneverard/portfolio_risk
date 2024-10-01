from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random

# Initialize the SQLite database
engine = create_engine('sqlite:///factoring.db', echo=False)
Base = declarative_base()

# Define the Sender (Customer) model
class Sender(Base):
    __tablename__ = 'senders'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    collateral = Column(Float, default=0.0)
    
    invoices = relationship('Invoice', back_populates='sender')
    
    def __repr__(self):
        return f"<Sender(name='{self.name}', collateral={self.collateral})>"

# Define the Invoice model
class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('senders.id'), nullable=False)
    receiver = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    
    sender = relationship('Sender', back_populates='invoices')
    factoring_transactions = relationship('FactoringTransaction', back_populates='invoice')
    
    def __repr__(self):
        return f"<Invoice(sender='{self.sender.name}', receiver='{self.receiver}', amount={self.amount})>"

# Define the Factoring Transaction model
class FactoringTransaction(Base):
    __tablename__ = 'factoring_transactions'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    purchase_fee = Column(Float, nullable=False)
    paid_out_amount = Column(Float, nullable=False)
    
    invoice = relationship('Invoice', back_populates='factoring_transactions')
    
    def __repr__(self):
        return f"<FactoringTransaction(invoice_id={self.invoice_id}, purchase_fee={self.purchase_fee}, paid_out_amount={self.paid_out_amount})>"

# Create tables
Base.metadata.create_all(engine)

# Setup session
Session = sessionmaker(bind=engine)
session = Session()

def populate_database(num_senders=3, num_invoices=100, num_transactions=10):
    # Create senders
    senders = [
        Sender(name=f"Sender {i}", collateral=round(random.uniform(10000, 200000), 0))
        for i in range(1, num_senders + 1)
    ]
    session.add_all(senders)
    session.commit()
    
    # Create invoices and factoring transactions
    invoices = []
    for _ in range(num_invoices):
        sender = random.choice(senders)
        receiver_name = f"Receiver {random.randint(1, 5)}"
        invoice_amount = round(random.uniform(5000, 100000), 2)
        
        invoice = Invoice(sender=sender, receiver=receiver_name, amount=invoice_amount)
        session.add(invoice)

        fee = round(random.uniform(50, 300), 2)
        paid_out_amount = round((random.uniform(0.5, 0.9) * invoice.amount) - fee, 2)
        
        factoring_transaction = FactoringTransaction(invoice=invoice, purchase_fee=fee, paid_out_amount=paid_out_amount)
        session.add(factoring_transaction)
    
    session.commit()

    print("Database populated successfully.")

# Function to display data for verification
def display_data():
    senders = session.query(Sender).all()
    for sender in senders:
        print(sender)
        for invoice in sender.invoices:
            print(f"  {invoice}")
            for transaction in invoice.factoring_transactions:
                print(f"    {transaction}")

# Populate the database
populate_database()

# Display the data
display_data()

# Close session
session.close()
