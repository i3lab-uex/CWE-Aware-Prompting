# -*- coding: utf-8 -*-
"""
Utility module for product updates.

The `update_product_info` function safely applies changes to a product
dictionary, allowing only fields that are explicitly listed in the global
`PERMITTED_FIELDS`. Any attempt to modify a non‑permitted field will raise
a `ValueError`, protecting against CWE‑915.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# List of fields that may be updated.  Add or remove as needed.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def update_product_info(prod: dict, change_data: dict) -> dict:
    """
    Update a product dictionary with the values from `change_data`.

    Only keys that are present in :data:`PERMITTED_FIELDS` will be updated.
    Any attempt to update a key outside this list results in a
    :class:`ValueError`.

    Parameters
    ----------
    prod : dict
        The product dictionary to be updated.  It is modified in place.
    change_data : dict
        Dictionary containing the new values for product fields.

    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).

    Raises
    ------
    ValueError
        If `change_data` contains a key that is not in :data:`PERMITTED_FIELDS`.

    Examples
    --------
    >>> product = {'price': 10.0, 'description': 'Old', 'stock': 5}
    >>> update_product_info(product, {'price': 12.0, 'stock': 4})
    {'price': 12.0, 'description': 'Old', 'stock': 4}
    >>> update_product_info(product, {'unknown': 1})
      Traceback (most recent call last):
        ...
    ValueError: Attempt to modify non‑permitted field 'unknown'.
    """
    # Validate the input types early
    if not isinstance(prod, dict):
        raise TypeError("prod must be a dictionary")
    if not isinstance(change_data, dict):
        raise TypeError("change_data must be a dictionary")

    for key, value in change_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Attempt to modify non‑permitted field '{key}'.")
        prod[key] = value

    return prod