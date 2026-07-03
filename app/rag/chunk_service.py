from app.elasticsearch_client import es

from app.rag.chunk_generator import (
    order_to_chunk,
    inventory_to_chunk,
    pricing_to_chunk
)


def create_order_chunks():

    response = es.search(
        index="orders_*",
        size=1500
    )

    chunks = []

    for hit in response["hits"]["hits"]:

        order = hit["_source"]

        chunks.append({
            "documentId": order["orderId"],
            "sourceIndex": hit["_index"],
            "region": order["region"],
            "country": order["country"],
            "category": order["category"],
            "content": order_to_chunk(order)
        })

    return chunks


def create_inventory_chunks():

    response = es.search(
        index="inventory_*",
        size=1500
    )

    chunks = []

    for hit in response["hits"]["hits"]:

        inventory = hit["_source"]

        chunks.append({
            "documentId": inventory["inventoryId"],
            "sourceIndex": hit["_index"],
            "region": inventory["region"],
            "country": inventory["country"],
            "category": inventory["category"],
            "content": inventory_to_chunk(inventory)
        })

    return chunks


def create_pricing_chunks():

    response = es.search(
        index="pricing_*",
        size=1500
    )

    chunks = []

    for hit in response["hits"]["hits"]:

        pricing = hit["_source"]

        chunks.append({
            "documentId": pricing["pricingId"],
            "sourceIndex": hit["_index"],
            "region": pricing["region"],
            "country": pricing["country"],
            "category": pricing["category"],
            "content": pricing_to_chunk(pricing)
        })

    return chunks