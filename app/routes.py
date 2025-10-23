from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
import math

main_bp = Blueprint('main', __name__)

# Sample data - In real app, replace with database
PRODUCTS_DATA = [
    {
        'id': 1,
        'name': 'Wireless Bluetooth Headphones',
        'slug': 'wireless-bluetooth-headphones',
        'price': 129.99,
        'compare_price': 199.99,
        'images': ['https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'],
        'category': 'electronics',
        'brand': 'AudioTech',
        'description': 'Premium wireless headphones with noise cancellation and 30-hour battery life.',
        'features': ['Noise Cancellation', '30h Battery', 'Fast Charge', 'Bluetooth 5.0'],
        'in_stock': True,
        'rating': 4.5,
        'review_count': 128,
        'sku': 'AUDIO-001'
    },
    {
        'id': 2,
        'name': 'Smart Fitness Watch',
        'slug': 'smart-fitness-watch',
        'price': 299.99,
        'compare_price': 399.99,
        'images': ['https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'],
        'category': 'electronics',
        'brand': 'FitPro',
        'description': 'Advanced fitness tracking with heart rate monitoring and GPS.',
        'features': ['Heart Rate Monitor', 'GPS', 'Waterproof', 'Sleep Tracking'],
        'in_stock': True,
        'rating': 4.8,
        'review_count': 89,
        'sku': 'FIT-001'
    },
    {
        'id': 3,
        'name': 'Organic Cotton T-Shirt',
        'slug': 'organic-cotton-tshirt',
        'price': 29.99,
        'compare_price': 39.99,
        'images': ['https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'],
        'category': 'fashion',
        'brand': 'EcoWear',
        'description': 'Comfortable organic cotton t-shirt available in multiple colors.',
        'features': ['100% Organic Cotton', 'Eco-Friendly', 'Multiple Colors'],
        'in_stock': True,
        'rating': 4.3,
        'review_count': 256,
        'sku': 'FASH-001'
    },
    {
        'id': 4,
        'name': 'Professional Camera',
        'slug': 'professional-camera',
        'price': 1299.99,
        'compare_price': 1599.99,
        'images': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'],
        'category': 'electronics',
        'brand': 'PhotoPro',
        'description': 'Professional DSLR camera with 4K video recording.',
        'features': ['4K Video', '24MP Sensor', 'Wi-Fi Connectivity', '3" LCD'],
        'in_stock': True,
        'rating': 4.9,
        'review_count': 67,
        'sku': 'CAM-001'
    },
    {
        'id': 5,
        'name': 'Designer Backpack',
        'slug': 'designer-backpack',
        'price': 89.99,
        'compare_price': 119.99,
        'images': ['https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'],
        'category': 'fashion',
        'brand': 'UrbanGear',
        'description': 'Stylish and functional backpack for everyday use.',
        'features': ['Waterproof', 'Laptop Compartment', 'Multiple Pockets'],
        'in_stock': True,
        'rating': 4.6,
        'review_count': 189,
        'sku': 'BAG-001'
    },
    {
        'id': 6,
        'name': 'Wireless Earbuds',
        'slug': 'wireless-earbuds',
        'price': 79.99,
        'compare_price': 99.99,
        'images': ['https://images.unsplash.com/photo-1590658165737-15a047b8b5e0?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'],
        'category': 'electronics',
        'brand': 'SoundWave',
        'description': 'Compact wireless earbuds with crystal clear sound.',
        'features': ['True Wireless', '24h Battery', 'Charging Case', 'Bluetooth 5.2'],
        'in_stock': True,
        'rating': 4.4,
        'review_count': 312,
        'sku': 'AUDIO-002'
    }
]

CATEGORIES = [
    {'id': 'electronics', 'name': 'Electronics', 'icon': '💻', 'count': 4},
    {'id': 'fashion', 'name': 'Fashion', 'icon': '👕', 'count': 2},
    {'id': 'home', 'name': 'Home & Garden', 'icon': '🏠', 'count': 0},
    {'id': 'sports', 'name': 'Sports', 'icon': '⚽', 'count': 0},
    {'id': 'books', 'name': 'Books', 'icon': '📚', 'count': 0},
    {'id': 'beauty', 'name': 'Beauty', 'icon': '💄', 'count': 0}
]

BRANDS = [
    {'id': 'AudioTech', 'name': 'AudioTech', 'product_count': 1},
    {'id': 'FitPro', 'name': 'FitPro', 'product_count': 1},
    {'id': 'EcoWear', 'name': 'EcoWear', 'product_count': 1},
    {'id': 'PhotoPro', 'name': 'PhotoPro', 'product_count': 1},
    {'id': 'UrbanGear', 'name': 'UrbanGear', 'product_count': 1},
    {'id': 'SoundWave', 'name': 'SoundWave', 'product_count': 1}
]

def get_cart():
    return session.get('cart', {})

def get_cart_count():
    cart = get_cart()
    return sum(item['quantity'] for item in cart.values())

@main_bp.context_processor
def inject_global_data():
    return {
        'categories': CATEGORIES,
        'brands': BRANDS,
        'cart_count': get_cart_count()
    }

@main_bp.route('/')
def index():
    featured_products = [p for p in PRODUCTS_DATA if p['id'] in [1, 2, 3]]
    trending_products = [p for p in PRODUCTS_DATA if p['id'] in [4, 5, 6]]
    
    return render_template('index.html',
                         featured_products=featured_products,
                         trending_products=trending_products)

@main_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    brand = request.args.get('brand', '')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Filter products
    filtered_products = PRODUCTS_DATA.copy()
    
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if brand:
        filtered_products = [p for p in filtered_products if p['brand'] == brand]
    
    if search:
        filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower()]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] <= max_price]
    
    # Sort products
    if sort == 'price_low':
        filtered_products.sort(key=lambda x: x['price'])
    elif sort == 'price_high':
        filtered_products.sort(key=lambda x: x['price'], reverse=True)
    elif sort == 'rating':
        filtered_products.sort(key=lambda x: x['rating'], reverse=True)
    else:  # newest
        filtered_products.sort(key=lambda x: x['id'], reverse=True)
    
    # Pagination
    per_page = 6
    total_pages = math.ceil(len(filtered_products) / per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = filtered_products[start_idx:end_idx]
    
    return render_template('products.html',
                         products=paginated_products,
                         total_pages=total_pages,
                         current_page=page,
                         selected_category=category,
                         selected_brand=brand,
                         search_query=search,
                         sort_by=sort,
                         min_price=min_price,
                         max_price=max_price)

@main_bp.route('/product/<slug>')
def product_detail(slug):
    product = next((p for p in PRODUCTS_DATA if p['slug'] == slug), None)
    if not product:
        return "Product not found", 404
    
    related_products = [p for p in PRODUCTS_DATA if p['category'] == product['category'] and p['id'] != product['id']][:4]
    
    return render_template('product_detail.html',
                         product=product,
                         related_products=related_products)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    product = next((p for p in PRODUCTS_DATA if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'})
    
    cart = get_cart()
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'image': product['images'][0],
            'slug': product['slug']
        }
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({
        'success': True,
        'cart_count': get_cart_count(),
        'message': 'Product added to cart successfully!'
    })

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
    
    return jsonify({
        'success': True,
        'cart_count': get_cart_count()
    })

@main_bp.route('/remove-from-cart/<product_id>')
def remove_from_cart(product_id):
    cart = get_cart()
    
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        session.modified = True
        flash('Item removed from cart!', 'success')
    
    return redirect(url_for('main.cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = get_cart()
    if not cart:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('main.cart'))
    
    if request.method == 'POST':
        # Process the order
        order_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'total': sum(item['price'] * item['quantity'] for item in cart.values())
        }
        
        # Clear the cart after successful order
        session.pop('cart', None)
        session.modified = True
        
        flash('Order placed successfully! Thank you for your purchase.', 'success')
        return redirect(url_for('main.index'))
    
    cart_items = list(cart.values())
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

# Helper function for pagination URLs in templates
@main_bp.app_context_processor
def utility_processor():
    def update_page_url(page):
        from flask import request
        args = request.args.copy()
        args['page'] = page
        return '?' + '&'.join([f'{k}={v}' for k, v in args.items()])
    
    return dict(update_page_url=update_page_url)