from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import ActivityLog, Category, Customer, Order, Product, Role, User

admin_bp = Blueprint("admin", __name__)

ORDER_STATUSES = [
    ("new", "Новый"),
    ("processing", "В обработке"),
    ("paid", "Оплачен"),
    ("done", "Завершён"),
    ("cancelled", "Отменён"),
]


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.has_role(*roles):
                abort(403)
            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def log_action(action, entity_name, entity_id=None, description=""):
    db.session.add(
        ActivityLog(
            user_id=current_user.id,
            action=action,
            entity_name=entity_name,
            entity_id=entity_id,
            description=description,
            ip_address=request.remote_addr,
        )
    )


def paginate(query):
    page = request.args.get("page", 1, type=int)
    return query.paginate(page=page, per_page=10, error_out=False)


@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "products": Product.query.count(),
        "categories": Category.query.count(),
        "customers": Customer.query.count(),
        "orders": Order.query.count(),
    }
    latest_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    latest_actions = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(8).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        latest_orders=latest_orders,
        latest_actions=latest_actions,
    )


@admin_bp.route("/categories")
@login_required
def categories():
    q = request.args.get("q", "").strip()
    query = Category.query.order_by(Category.name)
    if q:
        query = query.filter(Category.name.ilike(f"%{q}%"))
    return render_template("admin/categories.html", pagination=paginate(query), q=q)


@admin_bp.route("/categories/create", methods=["GET", "POST"])
@admin_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin", "manager")
def category_form(category_id=None):
    category = db.session.get(Category, category_id) if category_id else Category()
    if category_id and category is None:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        slug = request.form.get("slug", "").strip()
        is_active = request.form.get("is_active") == "on"
        if not name or not slug:
            flash("Название и slug обязательны.", "error")
        else:
            category.name = name
            category.slug = slug
            category.is_active = is_active
            db.session.add(category)
            db.session.flush()
            log_action("update" if category_id else "create", "Category", category.id, category.name)
            db.session.commit()
            flash("Категория сохранена.", "success")
            return redirect(url_for("admin.categories"))

    return render_template("admin/category_form.html", category=category)


@admin_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def category_delete(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        abort(404)
    log_action("delete", "Category", category.id, category.name)
    db.session.delete(category)
    db.session.commit()
    flash("Категория удалена.", "success")
    return redirect(url_for("admin.categories"))


@admin_bp.route("/products")
@login_required
def products():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    query = Product.query.join(Category).order_by(Product.created_at.desc())
    if q:
        query = query.filter((Product.name.ilike(f"%{q}%")) | (Product.sku.ilike(f"%{q}%")))
    if status == "active":
        query = query.filter(Product.is_active.is_(True))
    elif status == "hidden":
        query = query.filter(Product.is_active.is_(False))
    return render_template("admin/products.html", pagination=paginate(query), q=q, status=status)


@admin_bp.route("/products/create", methods=["GET", "POST"])
@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin", "manager")
def product_form(product_id=None):
    product = db.session.get(Product, product_id) if product_id else Product()
    if product_id and product is None:
        abort(404)

    categories = Category.query.order_by(Category.name).all()
    if request.method == "POST":
        errors = []
        product.name = request.form.get("name", "").strip()
        product.sku = request.form.get("sku", "").strip()
        product.category_id = request.form.get("category_id", type=int)
        product.price = request.form.get("price", type=float)
        product.stock_quantity = request.form.get("stock_quantity", type=int)
        product.is_active = request.form.get("is_active") == "on"

        if not product.name:
            errors.append("Введите название товара.")
        if not product.sku:
            errors.append("Введите артикул.")
        if product.price is None or product.price < 0:
            errors.append("Цена не может быть меньше 0.")
        if product.stock_quantity is None or product.stock_quantity < 0:
            errors.append("Остаток не может быть меньше 0.")

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            db.session.add(product)
            db.session.flush()
            log_action("update" if product_id else "create", "Product", product.id, product.name)
            db.session.commit()
            flash("Товар сохранён.", "success")
            return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", product=product, categories=categories)


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def product_delete(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        abort(404)
    log_action("delete", "Product", product.id, product.name)
    db.session.delete(product)
    db.session.commit()
    flash("Товар удалён.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/customers")
@login_required
def customers():
    q = request.args.get("q", "").strip()
    query = Customer.query.order_by(Customer.created_at.desc())
    if q:
        query = query.filter((Customer.full_name.ilike(f"%{q}%")) | (Customer.email.ilike(f"%{q}%")))
    return render_template("admin/customers.html", pagination=paginate(query), q=q)


@admin_bp.route("/customers/create", methods=["GET", "POST"])
@admin_bp.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin", "manager")
def customer_form(customer_id=None):
    customer = db.session.get(Customer, customer_id) if customer_id else Customer()
    if customer_id and customer is None:
        abort(404)
    if request.method == "POST":
        customer.full_name = request.form.get("full_name", "").strip()
        customer.email = request.form.get("email", "").strip()
        customer.phone = request.form.get("phone", "").strip()
        if not customer.full_name:
            flash("Введите ФИО клиента.", "error")
        else:
            db.session.add(customer)
            db.session.flush()
            log_action("update" if customer_id else "create", "Customer", customer.id, customer.full_name)
            db.session.commit()
            flash("Клиент сохранён.", "success")
            return redirect(url_for("admin.customers"))
    return render_template("admin/customer_form.html", customer=customer)


@admin_bp.route("/customers/<int:customer_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def customer_delete(customer_id):
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        abort(404)
    log_action("delete", "Customer", customer.id, customer.full_name)
    db.session.delete(customer)
    db.session.commit()
    flash("Клиент удалён.", "success")
    return redirect(url_for("admin.customers"))


@admin_bp.route("/orders")
@login_required
def orders():
    status = request.args.get("status", "")
    query = Order.query.join(Customer).order_by(Order.created_at.desc())
    if status:
        query = query.filter(Order.status == status)
    return render_template("admin/orders.html", pagination=paginate(query), statuses=ORDER_STATUSES, status=status)


@admin_bp.route("/orders/create", methods=["GET", "POST"])
@admin_bp.route("/orders/<int:order_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin", "manager")
def order_form(order_id=None):
    order = db.session.get(Order, order_id) if order_id else Order()
    if order_id and order is None:
        abort(404)
    customers = Customer.query.order_by(Customer.full_name).all()
    if request.method == "POST":
        order.customer_id = request.form.get("customer_id", type=int)
        order.status = request.form.get("status", "new")
        order.total_amount = request.form.get("total_amount", type=float)
        if not order.customer_id or order.total_amount is None or order.total_amount < 0:
            flash("Выберите клиента и укажите корректную сумму.", "error")
        else:
            db.session.add(order)
            db.session.flush()
            log_action("update" if order_id else "create", "Order", order.id, f"Заказ #{order.id}")
            db.session.commit()
            flash("Заказ сохранён.", "success")
            return redirect(url_for("admin.orders"))
    return render_template("admin/order_form.html", order=order, customers=customers, statuses=ORDER_STATUSES)


@admin_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def order_delete(order_id):
    order = db.session.get(Order, order_id)
    if order is None:
        abort(404)
    log_action("delete", "Order", order.id, f"Заказ #{order.id}")
    db.session.delete(order)
    db.session.commit()
    flash("Заказ удалён.", "success")
    return redirect(url_for("admin.orders"))


@admin_bp.route("/users")
@login_required
@role_required("admin")
def users():
    users_list = User.query.join(Role).order_by(User.full_name).all()
    return render_template("admin/users.html", users=users_list)


@admin_bp.route("/users/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def user_create():
    roles = Role.query.order_by(Role.name).all()
    if request.method == "POST":
        user = User(
            full_name=request.form.get("full_name", "").strip(),
            email=request.form.get("email", "").strip().lower(),
            role_id=request.form.get("role_id", type=int),
            is_active=request.form.get("is_active") == "on",
        )
        password = request.form.get("password", "")
        if not user.full_name or not user.email or not password:
            flash("ФИО, email и пароль обязательны.", "error")
        else:
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            log_action("create", "User", user.id, user.email)
            db.session.commit()
            flash("Пользователь создан.", "success")
            return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", roles=roles)


@admin_bp.route("/activity-log")
@login_required
@role_required("admin", "manager")
def activity_log():
    action = request.args.get("action", "")
    query = ActivityLog.query.order_by(ActivityLog.created_at.desc())
    if action:
        query = query.filter(ActivityLog.action == action)
    return render_template("admin/activity_log.html", pagination=paginate(query), action=action)
