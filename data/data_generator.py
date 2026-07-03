from datetime import datetime, timedelta
from random import Random
from elasticsearch import Elasticsearch, helpers

ES_URL = "http://localhost:9200"
DOCS_PER_INDEX = 500

REGIONS = {
    "eu": {"currency": "EUR", "countries": ["Germany", "France", "Italy"]},
    "apac": {"currency": "USD", "countries": ["India", "Japan", "Australia"]},
    "latam": {"currency": "USD", "countries": ["Brazil", "Mexico", "Argentina"]}
}

CATEGORIES = [
    "Electronics",
    "Laptops",
    "Mobile Phones",
    "Accessories",
    "Home Appliances",
    "Furniture",
    "Kitchen",
    "Sports",
    "Books",
    "Fashion"
]
SUPPLIERS = [
    "Apple",
    "Samsung",
    "Dell",
    "HP",
    "Lenovo",
    "Sony",
    "LG",
    "Logitech",
    "Asus",
    "Acer",
    "Philips",
    "Canon",
    "Nike",
    "Adidas",
    "IKEA",
    "Whirlpool",
    "Bosch",
    "Panasonic",
    "Puma",
    "JBL"
]
WAREHOUSES = {
    "eu": {
        "Germany": "Berlin Distribution Center",
        "France": "Paris Fulfillment Center",
        "Italy": "Milan Regional Warehouse"
    },
    "apac": {
        "India": "Mumbai Distribution Center",
        "Japan": "Tokyo Fulfillment Center",
        "Australia": "Sydney Regional Warehouse"
    },
    "latam": {
        "Brazil": "São Paulo Distribution Center",
        "Mexico": "Mexico City Fulfillment Center",
        "Argentina": "Buenos Aires Regional Warehouse"
    }
}

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Apple Pay",
    "Google Pay",
    "Bank Transfer"
]

ORDER_STATUS = [
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned"
]

FIRST_NAMES = [
    "John", "Emma", "Olivia", "Liam", "Noah",
    "Sophia", "James", "Lucas", "Emily", "Daniel",
    "Michael", "David", "Ava", "Isabella", "Mia",
    "Benjamin", "Ethan", "Charlotte", "Amelia", "Henry"
]

LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Williams",
    "Jones", "Miller", "Davis", "Wilson",
    "Taylor", "Anderson", "Thomas",
    "Moore", "Martin", "Clark", "Walker"
]

rnd = Random(42)
es = Elasticsearch(ES_URL)

ORDER_MAPPING = {
    "mappings": {"properties": {
        "orderId": {"type": "keyword"},
        "customerId": {"type": "keyword"},
        "customerName": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "customerEmail": {"type": "keyword"},
        "country": {"type": "keyword"},
        "city": {"type": "keyword"},
        "region": {"type": "keyword"},
        "productId": {"type": "keyword"},
        "productName": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "category": {"type": "keyword"},
        "supplier": {"type": "keyword"},
        "warehouse": {"type": "keyword"},
        "quantity": {"type": "integer"},
        "unitPrice": {"type": "double"},
        "discount": {"type": "double"},
        "tax": {"type": "double"},
        "shippingCost": {"type": "double"},
        "totalAmount": {"type": "double"},
        "currency": {"type": "keyword"},
        "paymentMethod": {"type": "keyword"},
        "orderStatus": {"type": "keyword"},
        "isReturned": {"type": "boolean"},
        "orderDate": {"type": "date"}
    }}
}

INVENTORY_MAPPING = {
    "mappings": {"properties": {
        "inventoryId": {"type": "keyword"},
        "productId": {"type": "keyword"},
        "productName": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "category": {"type": "keyword"},
        "supplier": {"type": "keyword"},
        "warehouse": {"type": "keyword"},
        "country": {"type": "keyword"},
        "region": {"type": "keyword"},
        "availableQuantity": {"type": "integer"},
        "reservedQuantity": {"type": "integer"},
        "reorderLevel": {"type": "integer"},
        "reorderQuantity": {"type": "integer"},
        "unitCost": {"type": "double"},
        "inventoryValue": {"type": "double"},
        "lastRestocked": {"type": "date"},
        "nextRestockDate": {"type": "date"}
    }}
}

PRICING_MAPPING = {
    "mappings": {"properties": {
        "pricingId": {"type": "keyword"},
        "productId": {"type": "keyword"},
        "productName": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "category": {"type": "keyword"},
        "supplier": {"type": "keyword"},
        "region": {"type": "keyword"},
        "country": {"type": "keyword"},
        "currency": {"type": "keyword"},
        "listPrice": {"type": "double"},
        "sellingPrice": {"type": "double"},
        "discountPercentage": {"type": "double"},
        "taxPercentage": {"type": "double"},
        "effectiveFrom": {"type": "date"},
        "effectiveTo": {"type": "date"},
        "isPromotion": {"type": "boolean"}
    }}
}


def create_index(name, mapping):
    if es.indices.exists(index=name):
        es.indices.delete(index=name)
    es.indices.create(index=name, body=mapping)


PRODUCTS = [
    {
        "id": "P0001",
        "name": "MacBook Pro 16",
        "category": "Laptops",
        "supplier": "Apple",
        "price": 2799
    },
    {
        "id": "P0002",
        "name": "MacBook Air M4",
        "category": "Laptops",
        "supplier": "Apple",
        "price": 1499
    },
    {
        "id": "P0003",
        "name": "Dell XPS 15",
        "category": "Laptops",
        "supplier": "Dell",
        "price": 2199
    },
    {
        "id": "P0004",
        "name": "Dell Inspiron 15",
        "category": "Laptops",
        "supplier": "Dell",
        "price": 999
    },
    {
        "id": "P0005",
        "name": "HP Spectre x360",
        "category": "Laptops",
        "supplier": "HP",
        "price": 1699
    },
    {
        "id": "P0006",
        "name": "Lenovo ThinkPad X1",
        "category": "Laptops",
        "supplier": "Lenovo",
        "price": 1899
    },
    {
        "id": "P0007",
        "name": "Samsung Galaxy S25",
        "category": "Mobile Phones",
        "supplier": "Samsung",
        "price": 1199
    },
    {
        "id": "P0008",
        "name": "iPhone 17 Pro",
        "category": "Mobile Phones",
        "supplier": "Apple",
        "price": 1399
    },
    {
        "id": "P0009",
        "name": "Sony WH-1000XM6",
        "category": "Accessories",
        "supplier": "Sony",
        "price": 449
    },
    {
        "id": "P0010",
        "name": "Logitech MX Master 4",
        "category": "Accessories",
        "supplier": "Logitech",
        "price": 129
    },
    {
        "id": "P0011",
        "name": "LG OLED C5 TV",
        "category": "Electronics",
        "supplier": "LG",
        "price": 2499
    },
    {
        "id": "P0012",
        "name": "Canon EOS R8",
        "category": "Electronics",
        "supplier": "Canon",
        "price": 1599
    },
    {
        "id": "P0013",
        "name": "Bosch Dishwasher",
        "category": "Home Appliances",
        "supplier": "Bosch",
        "price": 899
    },
    {
        "id": "P0014",
        "name": "Whirlpool Refrigerator",
        "category": "Home Appliances",
        "supplier": "Whirlpool",
        "price": 1299
    },
    {
        "id": "P0015",
        "name": "Nike Air Max",
        "category": "Fashion",
        "supplier": "Nike",
        "price": 179
    },
    {
        "id": "P0016",
        "name": "Adidas Ultraboost",
        "category": "Fashion",
        "supplier": "Adidas",
        "price": 199
    },
    {
        "id": "P0017",
        "name": "Office Chair Ergo",
        "category": "Furniture",
        "supplier": "IKEA",
        "price": 349
    },
    {
        "id": "P0018",
        "name": "Dining Table Oak",
        "category": "Furniture",
        "supplier": "IKEA",
        "price": 799
    },
    {
        "id": "P0019",
        "name": "Air Fryer XL",
        "category": "Kitchen",
        "supplier": "Philips",
        "price": 249
    },
    {
        "id": "P0020",
        "name": "Bluetooth Speaker",
        "category": "Electronics",
        "supplier": "JBL",
        "price": 149
    }
]

customers = []

for i in range(1, 201):
    first = rnd.choice(FIRST_NAMES)
    last = rnd.choice(LAST_NAMES)
    name = f"{first} {last}"

    customers.append({
        "id": f"C{i:04d}",
        "name": name,
        "email": f"{first.lower()}.{last.lower()}{i}@globalmart.com"
    })


def bulk(actions):
    helpers.bulk(es, actions)


for region in REGIONS:
    create_index(f"orders_{region}", ORDER_MAPPING)
    create_index(f"inventory_{region}", INVENTORY_MAPPING)
    create_index(f"pricing_{region}", PRICING_MAPPING)

for region, meta in REGIONS.items():
    pricing = []
    inventory = []
    orders = []
    for i in range(DOCS_PER_INDEX):
        p = rnd.choice(PRODUCTS)
        c = rnd.choice(customers)
        country = rnd.choice(meta["countries"])
        warehouse = WAREHOUSES[region][country]
        price = p["price"]
        discount = discount = rnd.choices(
            [0, 5, 10, 15, 20, 25],
            weights=[40, 20, 15, 10, 10, 5]
        )[0]
        selling = round(price * (1 - discount / 100), 2)

        pricing.append({
            "_index": f"pricing_{region}",
            "_source": {
                "pricingId": f"PRC-{region}-{i}",
                "productId": p["id"],
                "productName": p["name"],
                "category": p["category"],
                "supplier": p["supplier"],
                "region": region.upper(),
                "country": country,
                "currency": meta["currency"],
                "listPrice": price,
                "sellingPrice": selling,
                "discountPercentage": discount,
                "taxPercentage": 18,
                "effectiveFrom": "2026-01-01",
                "effectiveTo": "2026-12-31",
                "isPromotion": discount > 0
            }
        })

        qty = rnd.randint(20, 500)
        last_restock = datetime.now() - timedelta(days=rnd.randint(1, 90))
        inventory.append({
            "_index": f"inventory_{region}",
            "_source": {
                "inventoryId": f"INV-{region}-{i}",
                "productId": p["id"],
                "productName": p["name"],
                "category": p["category"],
                "supplier": p["supplier"],
                "warehouse": warehouse,
                "country": country,
                "region": region.upper(),
                "availableQuantity": qty,
                "reservedQuantity": rnd.randint(0, 50),
                "reorderLevel": rnd.randint(20, 80),
                "reorderQuantity": rnd.choice([50, 100, 150, 200]),
                "unitCost": round(selling * 0.7, 2),
                "inventoryValue": round(qty * selling * 0.7, 2),
                "lastRestocked": last_restock,
                "nextRestockDate": last_restock + timedelta(days=rnd.randint(30, 90))
            }
        })

        quantity = rnd.randint(1, 5)
        shipping = rnd.choice([0, 5, 10, 15, 20, 25])
        tax = rnd.choice([5, 12, 18, 20])
        order_date = datetime.now() - timedelta(days=rnd.randint(0, 365))
        orders.append({
            "_index": f"orders_{region}",
            "_source": {
                "orderId": f"ORD-{region}-{i}",
                "customerId": c["id"],
                "customerName": c["name"],
                "customerEmail": c["email"],
                "country": country,
                "city": warehouse,
                "region": region.upper(),
                "productId": p["id"],
                "productName": p["name"],
                "category": p["category"],
                "supplier": p["supplier"],
                "warehouse": warehouse,
                "quantity": quantity,
                "unitPrice": selling,
                "discount": discount,
                "tax": tax,
                "shippingCost": shipping,
                "totalAmount": round(quantity * selling + shipping, 2),
                "currency": meta["currency"],
                "paymentMethod": rnd.choice(PAYMENT_METHODS),
                "orderStatus": rnd.choice(ORDER_STATUS),
                "isReturned": rnd.random() < 0.05,
                "orderDate": order_date.isoformat()
            }
        })
    bulk(pricing)
    bulk(inventory)
    bulk(orders)

print("Done. Created 9 indices and indexed 500 documents into each.")
