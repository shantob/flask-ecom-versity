from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import event
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON  # fallback
import json

# Use SQLAlchemy JSON type if available; fallback safe handling for sqlite
try:
    from sqlalchemy import JSON
except Exception:
    JSON = SQLITE_JSON

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='category', lazy=True)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    logo = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='brand', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, default=0.0)
    compare_price = db.Column(db.Float)
    sku = db.Column(db.String(100), unique=True)
    images = db.Column(JSON, nullable=False, default=[])  # careful with mutable defaults; handled below
    in_stock = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    features = db.Column(JSON, nullable=False, default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_images(self):
        # Ensure Python object from JSON column
        imgs = self.images or []
        # if DB returns string, parse it
        if isinstance(imgs, str):
            try:
                imgs = json.loads(imgs)
            except Exception:
                imgs = []
        return imgs

    @property
    def first_image(self):
        imgs = self.get_images()
        if imgs and isinstance(imgs, list) and len(imgs) > 0:
            return f"/static/{imgs[0].lstrip('/')}"
        return '/static/images/default.jpg'


# Ensure JSON columns default to empty list when inserted (avoid mutable default problem)
@event.listens_for(Product, 'load')
def receive_load(product, _):
    if product.images is None:
        product.images = []
    if product.features is None:
        product.features = []

# Automatically generate slug for Product/Category/Brand if missing
@event.listens_for(Product, 'before_insert')
def generate_product_slug(mapper, connection, target):
    if not target.slug and target.name:
        target.slug = slugify(target.name)

@event.listens_for(Category, 'before_insert')
def generate_category_slug(mapper, connection, target):
    if not target.slug and target.name:
        target.slug = slugify(target.name)

@event.listens_for(Brand, 'before_insert')
def generate_brand_slug(mapper, connection, target):
    if not target.slug and target.name:
        target.slug = slugify(target.name)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    payment_method = db.Column(db.String(20), default='cash_on_delivery')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)


class WebsiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='NexaStore')
    site_description = db.Column(db.Text)
    site_tags = db.Column(db.Text)
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    facebook_url = db.Column(db.String(200))
    twitter_url = db.Column(db.String(200))
    instagram_url = db.Column(db.String(200))
    logo = db.Column(db.String(200))
    favicon = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
