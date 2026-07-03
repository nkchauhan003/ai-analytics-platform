def order_to_chunk(order):

    return (
        f"Customer {order['customerName']} from {order['country']} "
        f"purchased {order['quantity']} {order['productName']} "
        f"in the {order['category']} category for "
        f"{order['currency']} {order['totalAmount']:.2f}. "
        f"The order was fulfilled by the "
        f"{order['warehouse']} warehouse and paid using "
        f"{order['paymentMethod']}."
    )


def inventory_to_chunk(inventory):

    return (
        f"{inventory['availableQuantity']} units of "
        f"{inventory['productName']} are currently available "
        f"in the {inventory['warehouse']} warehouse located in "
        f"{inventory['country']}. The reorder level is "
        f"{inventory['reorderLevel']} units."
    )


def pricing_to_chunk(pricing):

    return (
        f"{pricing['productName']} is available in "
        f"{pricing['country']} for "
        f"{pricing['currency']} {pricing['sellingPrice']:.2f} "
        f"after a discount of "
        f"{pricing['discountPercentage']} percent."
    )