from app import create_app, db
from app.models import ActivityLog, Category, Customer, Order, Product, Role, User


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin_role = Role(code="admin", name="Администратор")
        manager_role = Role(code="manager", name="Менеджер")
        viewer_role = Role(code="viewer", name="Наблюдатель")
        db.session.add_all([admin_role, manager_role, viewer_role])
        db.session.flush()

        admin = User(email="admin@example.local", full_name="Администратор", role_id=admin_role.id)
        admin.set_password("admin12345")
        manager = User(email="manager@example.local", full_name="Менеджер магазина", role_id=manager_role.id)
        manager.set_password("manager12345")
        viewer = User(email="viewer@example.local", full_name="Наблюдатель", role_id=viewer_role.id)
        viewer.set_password("viewer12345")
        db.session.add_all([admin, manager, viewer])
        db.session.flush()

        categories = [
            Category(name="Ноутбуки", slug="notebooks"),
            Category(name="Периферия", slug="peripherals"),
            Category(name="Мониторы", slug="monitors"),
            Category(name="Аксессуары", slug="accessories"),
        ]
        db.session.add_all(categories)
        db.session.flush()

        products = [
            Product(category_id=categories[0].id, name="Ноутбук Atlas 14", sku="NB-ATLAS-14", price=64990, stock_quantity=8),
            Product(category_id=categories[0].id, name="Ноутбук Vector Pro", sku="NB-VECTOR-PRO", price=94990, stock_quantity=4),
            Product(category_id=categories[1].id, name="Клавиатура OfficeKey", sku="KB-OFFICE", price=2490, stock_quantity=35),
            Product(category_id=categories[1].id, name="Мышь SilentClick", sku="MS-SILENT", price=1290, stock_quantity=52),
            Product(category_id=categories[2].id, name="Монитор View 27", sku="MN-VIEW-27", price=21990, stock_quantity=12),
            Product(category_id=categories[3].id, name="USB-C Hub 7-in-1", sku="AC-HUB-7", price=3990, stock_quantity=18),
        ]
        db.session.add_all(products)

        customers = [
            Customer(full_name="Иван Петров", email="ivan@example.local", phone="+7 900 100-20-30"),
            Customer(full_name="Мария Соколова", email="maria@example.local", phone="+7 900 200-30-40"),
            Customer(full_name="ООО Ромашка", email="office@romashka.local", phone="+7 900 300-40-50"),
        ]
        db.session.add_all(customers)
        db.session.flush()

        orders = [
            Order(customer_id=customers[0].id, status="new", total_amount=67480),
            Order(customer_id=customers[1].id, status="paid", total_amount=21990),
            Order(customer_id=customers[2].id, status="processing", total_amount=107760),
        ]
        db.session.add_all(orders)

        db.session.add_all(
            [
                ActivityLog(user_id=admin.id, action="create", entity_name="Product", entity_id=1, description="Добавлен тестовый товар"),
                ActivityLog(user_id=manager.id, action="update", entity_name="Order", entity_id=2, description="Изменён статус заказа"),
            ]
        )

        db.session.commit()
        print("Seed completed. Login: admin@example.local / admin12345")


if __name__ == "__main__":
    seed()
