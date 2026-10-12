# -*- coding: utf-8 -*-
"""
Utility module for updating product information.

The `update_item_information` function updates a product dictionary
with new values, but only for keys that are explicitly permitted.
"""

from typing import Dict

# Global list of fields that can be updated
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_item_information(
    product_info: Dict[str, any], new_data: Dict[str, any]
) -> Dict[str, any]:
    """
    Update a product dictionary with new data.

    Only keys listed in :data:`PERMITTED_FIELDS` are considered for update.
    Keys not present in the product dictionary are ignored.  Any keys
    in *new_data* that are not permitted raise a :class:`ValueError`.

    Parameters
    ----------
    product_info : dict
        Dictionary representing the current state of a product.
    new_data : dict
        Dictionary containing key-value pairs intended for update.

    Returns
    -------
    dict
        A new dictionary with the updates applied.  The original
        ``product_info`` is not modified.

    Raises
    ------
    TypeError
        If either ``product_info`` or ``new_data`` is not a dictionary.
    ValueError
        If *new_data* contains keys that are not in :data:`PERMITTED_FIELDS`.

    Examples
    --------
    >>> product = {'price': 10.0, 'description': 'old', 'stock': 5}
    >>> update_item_information(product, {'price': 12.0, 'stock': 3})
    {'price': 12.0, 'description': 'old', 'stock': 3}
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Check for disallowed keys
    disallowed = set(new_data) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Update contains disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Create a shallow copy to avoid mutating the original
    updated = product_info.copy()

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS and key in product_info:
            updated[key] = value

    return updated