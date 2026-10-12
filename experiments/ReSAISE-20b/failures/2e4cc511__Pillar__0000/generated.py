# update_item_details.py

from typing import Dict, Any

# Global list of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_details(inventory: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the attributes of a product in `inventory` with values from `update_data`.

    Only fields listed in the global PERMITTED_FIELDS list may be modified.
    If an attempt is made to update a field that is not permitted, a ValueError
    will be raised.

    Args:
        inventory: A dictionary containing the current product information.
        update_data: A dictionary with keys and values that should be applied
                     to the product.

    Returns:
        The updated inventory dictionary.

    Raises:
        ValueError: If `update_data` contains a field that is not in PERMITTED_FIELDS.
    """
    # Validate that update_data only contains permitted fields
    for key in update_data:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")

    # Apply updates
    inventory.update(update_data)

    return inventory


# Example usage (for testing purposes only)
if __name__ == "__main__":
    product = {
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 50,
        "category": "electronics"
    }

    # Valid update
    updated = update_item_details(product, {"price": 17.99, "stock": 45})
    print(updated)

    # Invalid update (will raise ValueError)
    try:
        update_item_details(product, {"owner": "Alice"})
    except ValueError as e:
        print(e)