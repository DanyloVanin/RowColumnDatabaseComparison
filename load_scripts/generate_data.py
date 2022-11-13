import json
import random

import requests
from faker import Faker

fake = Faker()

API_URL = "http://localhost:8000"
NUM_RECEIPTS = 100000


# Generate Shops
def create_shops():
    with open('resources/shops.json') as f:
        data = json.load(f)
        shops = []
        for shop in data:
            response = requests.post(API_URL + '/shop', json=shop).json()
            print('Created shop: ', response)
            shops.append(response)
        return shops


def get_shops():
    return requests.get(API_URL + '/shop').json()


# Generate Products
def create_products():
    with open('resources/products.json') as f:
        data = json.load(f)
        products = []
        for product in data:
            response = requests.post(API_URL + '/product', json=product).json()
            print('Created product: ', response)
            products.append(response)
        return products


def get_products():
    return requests.get(API_URL + '/product').json()


# Create/Get shops
full_shops = get_shops()
if not full_shops:
    full_shops = create_shops()
print("Shops: ", full_shops)

# Create/Get Products
full_products = get_products()
if not full_products:
    full_products = create_products()
print("Products: ", full_products)


# Generate Sales + Receipts
def generate_receipt_sales():
    # Generate sales
    num_sales = random.randint(1, 5)
    selected_products = random.sample(full_products, num_sales)
    sales = []
    total_price = 0.0
    for product in selected_products:
        quantity = random.randint(1, 5)
        price = quantity * product['price']
        data = {
            "product_id": product['id'],
            "quantity": quantity,
            "price": price
        }
        total_price += price
        sales.append(data)
    # Generate receipt
    date = fake.date_time_this_year()
    shop = random.choice(full_shops)
    receipt = {
        "date": date.isoformat(),
        "shop_id": shop['id'],
        "total_price": total_price
    }
    # Post Receipt
    receipt_response = requests.post(API_URL + '/receipt', json=receipt)
    if receipt_response.status_code == 200:
        print(f"===> Created receipt with {num_sales} sales: ", receipt)
    receipt_data = receipt_response.json()
    # Fill receipt_id for sales
    for sale in sales:
        sale['receipt_id'] = receipt_data['id']
        sale_response = requests.post(API_URL + '/sale', json=sale)
        if sale_response.status_code == 200:
            print("Created sale: ", sale)


for i in range(NUM_RECEIPTS):
    print(f"Generating receipt ({i}/{NUM_RECEIPTS})...")
    generate_receipt_sales()
