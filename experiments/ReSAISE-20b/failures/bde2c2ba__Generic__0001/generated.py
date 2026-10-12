#!/usr/bin/env python3
"""
Utility module for updating product information.

The `update_item_information` function updates a product dictionary with
data supplied in ``new_data`` but only for keys that are listed in the global
``PERMITTED_FIELDS`` list.  The function returns a new dictionary containing
the updated product state and does not modify the original ``product_info``
dictionary in place.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Only these fields are allowed to be updated.  Add or remove field names as
# required by the application.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def update_item_information(
    product_info: dict,
    new_data: dict
) -> dict:
    """
    Update a product dictionary with values from ``new_data`` but only for
    fields listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product_info :
        A dictionary representing the original product.  It is **not**
        modified in place.
    new_data :
        A dictionary containing key/value pairs that represent the desired
        updates.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.

    Raises
    ------
    TypeError
        If ``product_info`` or ``new_data`` is not a dictionary.
    ValueError
        If any key in ``new_data`` is not present in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function performs a shallow copy of ``product_info``.  Nested mutable
    objects are not deep‑copied; if this is a concern, callers should provide
    immutable values or perform their own deep copy.

    Examples
    --------
    >>> product = {"price": 10.0, "stock": 5, "description": "Book"}
    >>> updates = {"price": 12.0, "stock": 4}
    >>> update_item_information(product, updates)
    {'price': 12.0, 'stock': 4, 'description': 'Book'}

    >>> bad_updates = {"unknown": "value"}
    >>> update_item_information(product, bad_updates)
    Traceback (most recent call last):
        ...
    ValueError: Attempted to update unpermitted field(s): ['unknown']
    """
    # Validate inputs
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Identify any unpermitted keys
    invalid_keys = [k for k in new_data if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update unpermitted field(s): {sorted(invalid_keys)}"
        )

    # Create a shallow copy of the original product
    updated_product = dict(product_info)

    # Apply permitted updates
    for key, value in new_data.items():
        updated_product[key] = value

    return updated_product