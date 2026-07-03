from app.rag.chunk_service import (
    create_order_chunks,
    create_inventory_chunks,
    create_pricing_chunks
)

from app.rag.chunk_index_service import (
    index_order_chunks,
    index_inventory_chunks,
    index_pricing_chunks
)
from app.rag.vector_index_service import (
    generate_order_vectors,
    generate_inventory_vectors,
    generate_pricing_vectors
)

order_chunks = create_order_chunks()
inventory_chunks = create_inventory_chunks()
pricing_chunks = create_pricing_chunks()

index_order_chunks(order_chunks)
index_inventory_chunks(inventory_chunks)
index_pricing_chunks(pricing_chunks)

print("Semantic chunks generated and indexed successfully.")

generate_order_vectors()
generate_inventory_vectors()
generate_pricing_vectors()

print("Vector indices created successfully.")
