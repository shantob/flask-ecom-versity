from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from app.models import Category, Brand, Product, Order, OrderItem, WebsiteSettings
from app.utils import generate_order_number
from app import db
import math

# Blueprints
main_bp = Blueprint('main', __name__)
cart_bp = Blueprint('cart', __name__)

# ============ Helper Functions ============

def get_cart():
    return session.get('cart', {})

def get_cart_count():
    cart = get_cart()
    return sum(item['quantity'] for item in cart.values())

@main_bp.app_context_processor
def inject_global_data():
    categories = Category.query.filter_by(is_active=True).all()
    brands = Brand.query.filter_by(is_active=True).all()
    settings = WebsiteSettings.query.first()
    cart_count = get_cart_count()
    return dict(categories=categories, brands=brands, settings=settings, cart_count=cart_count)

# ============ Main Routes ============

@main_bp.route('/')
def index():
    featured_products = Product.query.filter_by(featured=True, in_stock=True).limit(6).all()
    trending_products = Product.query.filter_by(in_stock=True).order_by(Product.created_at.desc()).limit(6).all()
    categories = Category.query.filter_by(is_active=True).limit(6).all()
    return render_template(
        'index.html',
        featured_products=featured_products,
        trending_products=trending_products,
        categories=categories
    )


@main_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    brand_id = request.args.get('brand', type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Product.query.filter_by(in_stock=True)

    if category_id:
        query = query.filter_by(category_id=category_id)
    if brand_id:
        query = query.filter_by(brand_id=brand_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    products_pagination = query.paginate(page=page, per_page=12, error_out=False)

    categories = Category.query.all()
    brands = Brand.query.all()

    # Precompute counts
    for cat in categories:
        cat.count = Product.query.filter_by(category_id=cat.id, in_stock=True).count()
    for brand in brands:
        brand.product_count = Product.query.filter_by(brand_id=brand.id, in_stock=True).count()

    return render_template(
        'products.html',
        products=products_pagination.items,
        pagination=products_pagination,
        selected_category=category_id,
        selected_brand=brand_id,
        search_query=search,
        sort_by=sort,
        min_price=min_price,
        max_price=max_price,
        categories=categories,
        brands=brands,
        current_page=page,
        total_pages=products_pagination.pages
    )


# ============ Product Detail ============

@main_bp.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.in_stock == True
    ).limit(4).all()

    return render_template('product_detail.html', product=product, related_products=related_products)


@main_bp.route('/about')
def about():
    return render_template('about.html', title='About Us')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')


# ============ Cart System ============

@main_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    cart = get_cart()

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'image': product.first_image,
            'slug': product.slug
        }

    session['cart'] = cart
    session.modified = True

    return jsonify({'success': True, 'cart_count': get_cart_count(), 'message': 'Added to cart'})


@main_bp.route('/cart')
def cart():
    cart = get_cart()
    cart_items = list(cart.values())
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


@main_bp.route('/update-cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()

    if product_id in cart:
        if quantity <= 0:
            del cart[product_id]
        else:
            cart[product_id]['quantity'] = quantity

    session['cart'] = cart
    session.modified = True
    return jsonify({'success': True, 'cart_count': get_cart_count()})


@main_bp.route('/remove-from-cart/<product_id>')
def remove_from_cart(product_id):
    cart = get_cart()
    if product_id in cart:
        del cart[product_id]
    session['cart'] = cart
    session.modified = True
    flash('Product removed from cart!', 'success')
    return redirect(url_for('main.cart'))


@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = get_cart()
    if not cart:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('main.cart'))

    if request.method == 'POST':
        order = Order(
            order_number=generate_order_number(),
            customer_name=request.form['name'],
            customer_email=request.form['email'],
            customer_phone=request.form['phone'],
            customer_address=request.form['address'],
            total_amount=sum(item['price'] * item['quantity'] for item in cart.values()),
            payment_method='cash_on_delivery'
        )
        db.session.add(order)
        db.session.flush()

        for item in cart.values():
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=item['id'],
                product_name=item['name'],
                product_price=item['price'],
                quantity=item['quantity'],
                total_price=item['price'] * item['quantity']
            ))

        db.session.commit()
        session.pop('cart', None)
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.index'))

    cart_items = list(cart.values())
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)
