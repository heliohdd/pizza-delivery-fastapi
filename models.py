from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship
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
    status = Column(String)  # Using ChoiceType for status
    user_id = Column(ForeignKey('users.id'), nullable=False)  # Assuming a foreign key relationship with User
    price = Column(Float, nullable=False)
    items = relationship('OrderItem', cascade="all, delete", backref='order', lazy=True)

    # Constructor to initialize the order
    def __init__(self, user_id, status='PENDING', price=0.0):
        self.user_id = user_id
        self.status = status
        self.price = price

    def calculate_total_price(self):
        """Calculate the total price of the order based on its items."""
        self.price = sum(item.unity_price * item.quantity for item in self.items)

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    flavor = Column(String, nullable=False)  # Assuming flavor is a string
    size = Column(String, nullable=False)  # Assuming size is a string
    unity_price = Column(Float, nullable=False)
    order_id = Column(ForeignKey('orders.id'), nullable=False)

    # Constructor to initialize the order item
    def __init__(self, quantity, flavor, size, unity_price, order_id):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unity_price = unity_price
        self.order_id = order_id