from elasticsearch import helpers

from app.elasticsearch_client import es
from app.rag.embedding_service import generate_embedding


def create_vector_index(index_name, dimensions):
    print(f"Creating {index_name}")

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

    print(response)


def bulk_index(index_name, documents):

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

    print("SUCCESS =", success)
    print("ERRORS =", errors)


def generate_vectors(
        source_index,
        destination_index
):
    print("Searching:", source_index)
    print(es.info())
    response = es.search(
        index=source_index,
        body={
            "query": {
                "match_all": {}
            },
            "size": 1500
        }
    )

    print(response)
    print(response["hits"]["total"])
    print(len(response["hits"]["hits"]))

    chunks = response["hits"]["hits"]

    print("Hits =", len(chunks))

    print(f"Reading from {source_index}")
    print(f"Found {len(chunks)} chunks")

    vector_documents = []

    dimensions = None

    for hit in chunks:

        chunk = hit["_source"]

        embedding = generate_embedding(
            chunk["content"]
        )
        print(f"Embedding dimension = {len(embedding)}")
        if dimensions is None:
            dimensions = len(embedding)

            create_vector_index(
                destination_index,
                dimensions
            )
        print(f"Creating index {destination_index}")
        vector_documents.append({
            "documentId": chunk["documentId"],
            "sourceIndex": chunk["sourceIndex"],
            "region": chunk["region"],
            "country": chunk["country"],
            "category": chunk["category"],
            "content": chunk["content"],
            "embedding": embedding
        })
    print(f"Indexing {len(vector_documents)} documents into {destination_index}")
    bulk_index(
        destination_index,
        vector_documents
    )
    print("Bulk indexing completed")


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
