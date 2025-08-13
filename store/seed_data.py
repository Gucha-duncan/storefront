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

def create_customers(n=10):
    customers = []
    for _ in range(n):
        customer = Customer.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.random_int(min=100000000, max=999999999),
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
        promo = Promotion.objects.create(
            description=fake.sentence(),
            discount=round(random.uniform(5, 50), 2)
        )
        promotions.append(promo)
    print(f"✅ Created {n} promotions")
    return promotions

def create_collections(n=3):
    collections = []
    for _ in range(n):
        coll = Collection.objects.create(
            title=fake.word()
        )
        collections.append(coll)
    print(f"✅ Created {n} collections")
    return collections

def create_products(n=20, promotions=None, collections=None):
    products = []
    for _ in range(n):
        coll = random.choice(collections) if collections else None
        product = Product.objects.create(
            slug=fake.slug(),
            title=fake.word().capitalize(),
            description=fake.text(),
            unit_price=Decimal(random.uniform(10, 500)).quantize(Decimal('0.01')),
            inventory=random.randint(1, 100),
            Collection=coll
        )
        if promotions:
            product.promotions.add(random.choice(promotions))
        products.append(product)
    print(f"✅ Created {n} products")
    return products

def create_orders(customers, products, n=15):
    orders = []
    for _ in range(n):
        customer = random.choice(customers)
        order = Order.objects.create(
            customer=customer,
            payment_status=random.choice([Order.PENDING, Order.COMPLETE, Order.FAILED])
        )
        for _ in range(random.randint(1, 5)):
            product = random.choice(products)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=random.randint(1, 3),
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
                quantity=random.randint(1, 5)
            )
    print(f"✅ Created {n} carts with items")

def run():
    customers = create_customers(10)
    promotions = create_promotions(5)
    collections = create_collections(3)
    products = create_products(20, promotions, collections)
    create_orders(customers, products, 15)
    create_carts(products, 5)
    print("🎯 Seeding complete!")

if __name__ == "__main__":
    run()
