# edit_product_info.py

"""
Utility to update product dictionaries with a whitelist of allowed fields.

The module defines a single public function `edit_product_info` that takes an
existing product dictionary and a second dictionary containing desired updates.
Only the keys listed in `PERMITTED_FIELDS` are applied to the product. All
other keys are ignored.

The function mutates the input `item` dictionary in place and also returns it,
allowing for both side‑effects and functional use.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with permitted fields.

    Parameters
    ----------
    item : dict
        Existing product data. Expected keys include at least those in
        `PERMITTED_FIELDS`. The dictionary is updated *in place*.
    details : dict
        Desired updates. Only keys present in `PERMITTED_FIELDS` are applied.
        Values are used verbatim; no type conversion is performed.

    Returns
    -------
    dict
        The updated product dictionary (same object as `item`).

    Notes
    -----
    * No validation of value types is performed; callers should ensure that
      the values in `details` are appropriate for the product schema.
    * Keys not listed in `PERMITTED_FIELDS` are silently ignored.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("details must be a dictionary")

    for key in PERMITTED_FIELDS:
        if key in details:
            item[key] = details[key]

    return item