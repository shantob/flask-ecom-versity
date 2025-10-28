import os
import secrets
from PIL import Image
from flask import current_app, url_for, flash, redirect
from functools import wraps
from flask_login import current_user

def save_image(image_file, folder='products'):
    """Save uploaded image and return path relative to static (e.g. uploads/products/xxx.jpg)"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_file.filename)
    image_fn = random_hex + f_ext
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_folder, exist_ok=True)
    image_path = os.path.join(upload_folder, image_fn)

    output_size = (1200, 1200)
    img = Image.open(image_file)
    img.thumbnail(output_size)
    img.save(image_path)

    # return path used in DB (no leading slash)
    return f"uploads/{folder}/{image_fn}"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access admin panel.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_order_number():
    import random, string
    return 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
