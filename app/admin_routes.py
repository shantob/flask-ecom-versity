import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Admin, Category, Brand, Product, Order, OrderItem, WebsiteSettings
from app.utils import admin_required, save_image, generate_order_number
from slugify import slugify
from flask import make_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates/admin')

# ---- AUTH ----
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password!', 'error')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin.login'))

# ---- DASHBOARD ----
@admin_bp.route('/')
@admin_required
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_categories = Category.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(6).all()
    return render_template('admin/dashboard.html',
                           total_products=total_products,
                           total_orders=total_orders,
                           total_categories=total_categories,
                           pending_orders=pending_orders,
                           recent_orders=recent_orders)

# ---- CATEGORIES ----
@admin_bp.route('/categories')
@admin_required
def categories():
    categories = Category.query.order_by(Category.created_at.desc()).all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug') or slugify(name)
        slug = slug.lower()
        if Category.query.filter_by(slug=slug).first():
            flash('Category slug already exists!', 'error')
            return redirect(url_for('admin.categories'))
        category = Category(name=name, slug=slug)
        # handle image
        img = request.files.get('image')
        if img:
            category.image = save_image(img, folder='categories')
        db.session.add(category)
        db.session.commit()
        flash('Category added!', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', category=None)

@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.slug = (request.form.get('slug') or slugify(category.name)).lower()
        img = request.files.get('image')
        if img:
            category.image = save_image(img, folder='categories')
        db.session.commit()
        flash('Category updated!', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', category=category)

@admin_bp.route('/categories/delete/<int:id>', methods=['POST'])
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.products:
        flash('Cannot delete category with products!', 'error')
        return redirect(url_for('admin.categories'))
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted!', 'success')
    return redirect(url_for('admin.categories'))

# ---- BRANDS ----
@admin_bp.route('/brands')
@admin_required
def brands():
    brands = Brand.query.order_by(Brand.created_at.desc()).all()
    return render_template('admin/brands.html', brands=brands)

@admin_bp.route('/brands/add', methods=['GET', 'POST'])
@admin_required
def add_brand():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = (request.form.get('slug') or slugify(name)).lower()
        if Brand.query.filter_by(slug=slug).first():
            flash('Brand slug already exists!', 'error')
            return redirect(url_for('admin.brands'))
        brand = Brand(name=name, slug=slug)
        logo = request.files.get('logo')
        if logo:
            brand.logo = save_image(logo, folder='brands')
        db.session.add(brand)
        db.session.commit()
        flash('Brand added!', 'success')
        return redirect(url_for('admin.brands'))
    return render_template('admin/brand_form.html', brand=None)

@admin_bp.route('/brands/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_brand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        brand.name = request.form.get('name')
        brand.slug = (request.form.get('slug') or slugify(brand.name)).lower()
        logo = request.files.get('logo')
        if logo:
            brand.logo = save_image(logo, folder='brands')
        db.session.commit()
        flash('Brand updated!', 'success')
        return redirect(url_for('admin.brands'))
    return render_template('admin/brand_form.html', brand=brand)

@admin_bp.route('/brands/delete/<int:id>', methods=['POST'])
@admin_required
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    if brand.products:
        flash('Cannot delete brand with products!', 'error')
        return redirect(url_for('admin.brands'))
    db.session.delete(brand)
    db.session.commit()
    flash('Brand deleted!', 'success')
    return redirect(url_for('admin.brands'))

# ---- PRODUCTS ----
@admin_bp.route('/products')
@admin_required
def products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template('admin/products.html', products=products, categories=categories, brands=brands)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = (request.form.get('slug') or slugify(name)).lower()
        price = float(request.form.get('price') or 0)
        sku = request.form.get('sku')
        quantity = int(request.form.get('quantity') or 0)
        category_id = int(request.form.get('category_id'))
        brand_id = int(request.form.get('brand_id'))
        featured = bool(request.form.get('featured'))
        description = request.form.get('description')
        short_description = request.form.get('short_description')
        images_files = request.files.getlist('images')
        images_list = []
        for img in images_files:
            if img and img.filename:
                images_list.append(save_image(img, folder='products'))
        product = Product(
            name=name,
            slug=slug,
            description=description,
            short_description=short_description,
            price=price,
            sku=sku,
            quantity=quantity,
            category_id=category_id,
            brand_id=brand_id,
            featured=featured,
            images=images_list
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added!', 'success')
        return redirect(url_for('admin.products'))
    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template('admin/product_form.html', product=None, categories=categories, brands=brands)

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.slug = (request.form.get('slug') or slugify(product.name)).lower()
        product.price = float(request.form.get('price') or 0)
        product.compare_price = float(request.form.get('compare_price') or 0)
        product.sku = request.form.get('sku')
        product.quantity = int(request.form.get('quantity') or 0)
        product.category_id = int(request.form.get('category_id'))
        product.brand_id = int(request.form.get('brand_id'))
        product.featured = bool(request.form.get('featured'))
        product.in_stock = bool(request.form.get('in_stock'))
        product.rating = float(request.form.get('rating') or 0)
        product.review_count = int(request.form.get('review_count') or 0)
        product.features = request.form.get('features')
        product.description = request.form.get('description')
        product.short_description = request.form.get('short_description')

        # ----- IMAGE UPDATE FIX -----
        new_files = request.files.getlist('images')
        existing_images = product.get_images() or []
        uploaded_new = []

        for img in new_files:
            if img and img.filename:
                uploaded_new.append(save_image(img, folder='products'))

        # ✅ If new images uploaded, replace old ones
        if uploaded_new:
            product.images = uploaded_new
        else:
            # ✅ Keep old images if no new upload
            product.images = existing_images

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))

    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template('admin/product_form.html', product=product, categories=categories, brands=brands)


@admin_bp.route('/products/delete/<int:id>', methods=['POST'])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    # optionally: delete images from disk
    # for img in product.get_images(): ...
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!', 'success')
    return redirect(url_for('admin.products'))

# ---- ORDERS ----
@admin_bp.route('/orders')
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/<int:id>')
@admin_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/<int:id>/status', methods=['POST'])
@admin_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f"Order status updated to {new_status.capitalize()}!", "success")
    else:
        flash("Invalid status!", "error")
    return redirect(url_for('admin.order_detail', id=order.id))


@admin_bp.route('/orders/<int:id>/download', methods=['GET'])
@admin_required
def download_order_pdf(id):
    order = Order.query.get_or_404(id)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, f"Order Invoice #{order.order_number}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 90, f"Customer: {order.customer_name}")
    pdf.drawString(50, height - 110, f"Email: {order.customer_email}")
    pdf.drawString(50, height - 130, f"Phone: {order.customer_phone}")
    pdf.drawString(50, height - 150, f"Address: {order.customer_address}")
    pdf.drawString(50, height - 170, f"Payment Method: {order.payment_method}")
    pdf.drawString(50, height - 190, f"Status: {order.status}")
    pdf.drawString(50, height - 210, f"Total Amount: {order.total_amount} BDT")

    # Table header
    y = height - 250
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Product")
    pdf.drawString(300, y, "Qty")
    pdf.drawString(400, y, "Total")

    pdf.setFont("Helvetica", 12)
    y -= 20
    for item in order.order_items:
        pdf.drawString(50, y, item.product_name)
        pdf.drawString(300, y, str(item.quantity))
        pdf.drawString(400, y, str(item.total_price))
        y -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=order_{order.order_number}.pdf'
    return response

# ---- SETTINGS ----
@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    settings = WebsiteSettings.query.first()
    if not settings:
        settings = WebsiteSettings()
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':

        # Text fields
        settings.site_name = request.form.get('site_name')
        settings.site_description = request.form.get('site_description')
        settings.site_tags = request.form.get('site_tags')

        settings.contact_email = request.form.get('contact_email')
        settings.contact_phone = request.form.get('contact_phone')
        settings.address = request.form.get('address')

        settings.facebook_url = request.form.get('facebook_url')
        settings.twitter_url = request.form.get('twitter_url')
        settings.instagram_url = request.form.get('instagram_url')

        # Image Upload
        logo = request.files.get('logo')
        favicon = request.files.get('favicon')

        if logo:
            settings.logo = save_image(logo, folder='settings')

        if favicon:
            settings.favicon = save_image(favicon, folder='settings')

        db.session.commit()
        flash("Settings updated successfully!", "success")
        return redirect(url_for('admin.settings'))

    return render_template("admin/settings.html", settings=settings)

