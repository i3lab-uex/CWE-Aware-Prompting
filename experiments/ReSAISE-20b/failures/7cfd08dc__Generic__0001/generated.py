# -*- coding: utf-8 -*-

"""
Utility module for updating product attributes.

The function `update_product_attributes` updates a product dictionary
with new values supplied in the `updates` mapping.  Only keys that are
listed in the global list `PERMITTED_FIELDS` may be modified; attempting
to modify any other field will raise a ValueError.

Example
-------
>>> product = {"price": 10.0, "description": "Old", "stock": 5}
>>> updates = {"price": 12.5, "description": "New"}
>>> update_product_attributes(product, updates)
{'price': 12.5, 'description': 'New', 'stock': 5}
"""

from __future__ import annotations

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Update a product dictionary with the values from `updates`.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It will be updated in place and also returned.
    updates : dict
        A mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    ValueError
        If `updates` contains a key that is not in `PERMITTED_FIELDS`.

    Notes
    -----
    * The function modifies the original dictionary passed in `item`.
      If you need to preserve the original, pass a copy: ``update_product_attributes(item.copy(), updates)``.
    * No type validation is performed on the values; callers should ensure that
      the new values are of an appropriate type for the product model.
    """
    # Validate that all keys to be updated are permitted
    invalid_keys = [k for k in updates if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_keys)}"
        )

    # Apply the updates
    item.update(updates)

    return item

# If this module is executed directly, run a simple test
if __name__ == "__main__":
    sample_product = {"price": 20.0, "description": "Sample", "stock": 10}
    changes = {"price": 25.0, "category": "New Category"}
    print("Before:", sample_product)
    updated = update_product_attributes(sample_product, changes)
    print("After :", updated)