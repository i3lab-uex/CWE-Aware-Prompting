# -*- coding: utf-8 -*-

"""
Utility for updating product information with field-level permission checks.
"""

from typing import Dict, Any

# List of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from `change_data`, but only for
    fields that are present in the global PERMITTED_FIELDS list.

    Parameters
    ----------
    prod : dict
        The original product dictionary. It is modified in place.
    change_data : dict
        Dictionary containing new values for fields that should be updated.

    Returns
    -------
    dict
        The same dictionary reference as `prod`, now containing the updated values.

    Notes
    -----
    - Fields not listed in PERMITTED_FIELDS are ignored.
    - If `change_data` contains a key that is not a valid product field at all,
      it will also be ignored to avoid accidental injection of unwanted keys.
    """
    # Defensive copy of permitted fields for fast lookup
    allowed = set(PERMITTED_FIELDS)

    for key, value in change_data.items():
        if key in allowed:
            prod[key] = value
    return prod

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     product = {"price": 10.0, "description": "Old desc", "stock": 5, "category": "Books"}
#     changes = {"price": 12.5, "stock": 7, "invalid_field": "oops"}
#     updated = update_product_info(product, changes)
#     print(updated)  # {'price': 12.5, 'description': 'Old desc', 'stock': 7, 'category': 'Books'}