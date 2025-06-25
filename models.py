from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# Create an SQLite database 
db = create_engine('sqlite:///pizza_delivery_fastapi.db', echo=True)

# Create a base class for models
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    
    # Constructor to initialize the user
    def __init__(self, username, email, password, active=True, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

# Order model
class Order(Base):
    __tablename__ = 'orders'

    # STATUS_CHOICES = (
    #     ('pending', 'PENDING'),
    #     ('canceled', 'CANCELED'),
    #     ('completed', 'COMPLETED'),
    #     # Add more statuses as needed
    # )  # Define possible order statuses
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)  # Assuming a foreign key relationship with User
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String)  # Using ChoiceType for status
    # status = Column(ChoiceType(STATUS_CHOICES))  # Using ChoiceType for status
    price = Column(Float, nullable=False)
    # items = Column(Integer, nullable=False)

    # Constructor to initialize the order
    def __init__(self, user_id, product_id, quantity, status='pending'):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.status = status

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Constructor to initialize the order item
    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price