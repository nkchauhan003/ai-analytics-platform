from elasticsearch import helpers

from app.elasticsearch_client import es


def create_chunk_index(index_name):

    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    es.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "documentId": {
                    "type": "keyword"
                },
                "sourceIndex": {
                    "type": "keyword"
                },
                "region": {
                    "type": "keyword"
                },
                "country": {
                    "type": "keyword"
                },
                "category": {
                    "type": "keyword"
                },
                "content": {
                    "type": "text"
                }
            }
        }
    )


def index_chunks(index_name, chunks):

    create_chunk_index(index_name)

    actions = []

    for chunk in chunks:

        actions.append({
            "_index": index_name,
            "_source": chunk
        })

    helpers.bulk(es, actions)


def index_order_chunks(chunks):
    index_chunks("chunks_orders", chunks)


def index_inventory_chunks(chunks):
    index_chunks("chunks_inventory", chunks)


def index_pricing_chunks(chunks):
    index_chunks("chunks_pricing", chunks)