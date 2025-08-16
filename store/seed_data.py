import os
import django
import random
from decimal import Decimal
from faker import Faker

# 1️⃣ Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storefront.settings")  # replace storefront with your project name
django.setup()

# 2️⃣ Import models
from store.models import (
    Customer, Address, Product, Order, OrderItem,
    Promotion, Collection, Cart, CartItem
)

fake = Faker()

PRODUCT_CATEGORIES = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Bluetooth Speaker"],
    "Clothing": ["T-Shirt", "Jeans", "Sneakers", "Jacket", "Dress"],
    "Home Appliances": ["Microwave", "Blender", "Coffee Maker", "Vacuum Cleaner", "Air Fryer"],
}

PROMO_TEMPLATES = [
    "Save {discount}% on all {category}!",
    "{discount}% off this week only!",
    "Flash Sale – {discount}% discount on {category}!",
]

def create_customers(n=10):
    customers = []
    for _ in range(n):
        customer = Customer.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            # ✅ numeric phone since your model expects an IntegerField
            phone=fake.random_int(min=700000000, max=799999999),  # e.g. Kenyan format 07xx...
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=60),
            membership=random.choice([
                Customer.MEMBERSHIP_BASIC,
                Customer.MEMBERSHIP_BRONZE,
                Customer.MEMBERSHIP_SILVER,
                Customer.MEMBERSHIP_GOLD
            ])
        )
        Address.objects.create(
            street=fake.street_address(),
            city=fake.city(),
            customer=customer
        )
        customers.append(customer)
    print(f"✅ Created {n} customers")
    return customers

def create_promotions(n=5):
    promotions = []
    for _ in range(n):
        discount = random.randint(5, 50)
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        promo = Promotion.objects.create(
            description=random.choice(PROMO_TEMPLATES).format(discount=discount, category=category),
            discount=discount
        )
        promotions.append(promo)
    print(f"✅ Created {n} promotions")
    return promotions

def create_collections():
    collections = []
    for category in PRODUCT_CATEGORIES.keys():
        coll = Collection.objects.create(title=category)
        collections.append(coll)
    print(f"✅ Created {len(collections)} collections")
    return collections

def create_products(promotions=None, collections=None):
    products = []
    for coll in collections:
        for item in PRODUCT_CATEGORIES[coll.title]:
            product = Product.objects.create(
                slug=f"{item.lower().replace(' ', '-')}-{fake.unique.uuid4()}",
                title=item,
                description=f"A high-quality {item.lower()} perfect for everyday use.",
                unit_price=Decimal(random.uniform(20, 1000)).quantize(Decimal('0.01')),
                inventory=random.randint(5, 50),
                collection=coll,
                # If you have image field, uncomment:
                # image=f"https://picsum.photos/seed/{item.lower()}/400/400"
            )
            if promotions:
                product.promotions.add(random.choice(promotions))
            products.append(product)
    print(f"✅ Created {len(products)} products")
    return products

def create_orders(customers, products, n=15):
    orders = []
    for _ in range(n):
        customer = random.choice(customers)
        order = Order.objects.create(
            customer=customer,
            payment_status=random.choice([Order.PENDING, Order.COMPLETE, Order.FAILED])
        )
        for _ in range(random.randint(1, 4)):
            product = random.choice(products)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=min(random.randint(1, 3), product.inventory),
                unit_price=product.unit_price
            )
        orders.append(order)
    print(f"✅ Created {n} orders with items")
    return orders

def create_carts(products, n=5):
    for _ in range(n):
        cart = Cart.objects.create()
        for _ in range(random.randint(1, 4)):
            product = random.choice(products)
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=min(random.randint(1, 5), product.inventory)
            )
    print(f"✅ Created {n} carts with items")

def run():
    customers = create_customers(10)
    promotions = create_promotions(5)
    collections = create_collections()
    products = create_products(promotions, collections)
    create_orders(customers, products, 15)
    create_carts(products, 5)
    print("🎯 Seeding complete!")

if __name__ == "__main__":
    run()
