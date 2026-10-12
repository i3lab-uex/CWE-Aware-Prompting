# -*- coding: utf-8 -*-

"""
Utility to safely edit product information.

The function `edit_product_info` accepts a mutable dictionary representing
a product and a second dictionary containing the desired updates. Only keys
present in the global `PERMITTED_FIELDS` list are applied to the product.
All other keys are ignored, protecting against accidental or malicious
modification of internal fields.

The implementation follows best practices for defensive programming and
avoids CWE-915 by explicitly controlling which attributes may be altered.
"""

from __future__ import annotations

# List of product fields that are allowed to be updated
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]


def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with permitted fields.

    Parameters
    ----------
    item : dict
        The original product data. It is modified in place.
    details : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        The updated product dictionary (same object as `item`).

    Notes
    -----
    - Only keys listed in :data:`PERMITTED_FIELDS` are applied.
    - Keys not present in `details` or not permitted are silently ignored.
    - The function performs type checks to ensure that keys are strings
      and values are JSON-serializable (basic check). If a key is not a string,
      it raises :class:`TypeError`.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary representing the product.")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary of updates.")

    for key, value in details.items():
        # Reject non-string keys to avoid accidental attribute creation
        if not isinstance(key, str):
            raise TypeError(f"Field name must be a string; got {type(key).__name__}")

        if key in PERMITTED_FIELDS:
            # Basic sanity check: value should be JSON-serializable
            try:
                import json

                json.dumps(value)
            except (TypeError, OverflowError):
                raise ValueError(f"Value for field '{key}' is not JSON-serializable.")

            item[key] = value

    return item