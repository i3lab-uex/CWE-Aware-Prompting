import copy
from typing import Dict, Any

# Fields that are allowed to be updated.  Feel free to extend this list.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def modify_product_data(product_details: Dict[str, Any],
                        update_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from *update_info* only for
    keys listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product_details:
        Dictionary containing the current state of the product.
    update_info:
        Dictionary with key/value pairs that should be applied to
        *product_details*.

    Returns
    -------
    dict
        A new dictionary that contains the updated product data.
        The original *product_details* is left untouched.

    Raises
    ------
    TypeError
        If either *product_details* or *update_info* is not a mapping.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Work on a shallow copy to avoid mutating the caller's dict
    updated_product = copy.deepcopy(product_details)

    for field, new_value in update_info.items():
        if field in PERMITTED_FIELDS:
            updated_product[field] = new_value
        # Fields not permitted are silently ignored – this is the safest behaviour.
    return updated_product


# Example usage
if __name__ == "__main__":
    product = {
        "price": 19.99,
        "description": "Red T-shirt",
        "stock": 50,
        "category": "Apparel",
    }

    changes = {"price": 17.99, "stock": 45, "color": "Blue"}  # 'color' is not permitted
    updated = modify_product_data(product, changes)
    print(updated)  # {'price': 17.99, 'description': 'Red T-shirt', 'stock': 45, 'category': 'Apparel'}