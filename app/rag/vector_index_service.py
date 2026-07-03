from elasticsearch import helpers

from app.elasticsearch_client import es
from app.rag.embedding_service import generate_embedding


def create_vector_index(index_name, dimensions):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    response = es.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "documentId": {"type": "keyword"},
                "sourceIndex": {"type": "keyword"},
                "region": {"type": "keyword"},
                "country": {"type": "keyword"},
                "category": {"type": "keyword"},
                "content": {"type": "text"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": dimensions,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    )


def bulk_index(index_name, documents):
    print(documents[0])
    actions = [
        {
            "_index": index_name,
            "_source": doc
        }
        for doc in documents
    ]

    success, errors = helpers.bulk(
        es,
        actions,
        raise_on_error=False,
        stats_only=False
    )

    print("SUCCESS =", success, "ERRORS =", errors)


def generate_vectors(
        source_index,
        destination_index
):
    response = es.search(
        index=source_index,
        body={
            "query": {
                "match_all": {}
            },
            "size": 1
        }
    )

    chunks = response["hits"]["hits"]
    vector_documents = []
    dimensions = None

    for hit in chunks:

        chunk = hit["_source"]

        embedding = generate_embedding(
            chunk["content"]
        )

        if dimensions is None:
            dimensions = len(embedding)

            create_vector_index(
                destination_index,
                dimensions
            )
        vector_documents.append({
            "documentId": chunk["documentId"],
            "sourceIndex": chunk["sourceIndex"],
            "region": chunk["region"],
            "country": chunk["country"],
            "category": chunk["category"],
            "content": chunk["content"],
            "embedding": embedding
        })
    bulk_index(
        destination_index,
        vector_documents
    )


def generate_order_vectors():
    generate_vectors(
        "chunks_orders",
        "vectors_orders"
    )


def generate_inventory_vectors():
    generate_vectors(
        "chunks_inventory",
        "vectors_inventory"
    )


def generate_pricing_vectors():
    generate_vectors(
        "chunks_pricing",
        "vectors_pricing"
    )
