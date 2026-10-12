# SPDX-License-Identifier: MIT
"""
Utility module for safely updating product dictionaries.

The `modify_item_details` function updates only the attributes that are
explicitly allowed via the global PERMITTED_FIELDS list.  All other keys in
the `details` dictionary are ignored, preventing accidental or malicious
modification of restricted fields.

CWE-913 (Improper Control of Dynamically-Managed Code Resources) is mitigated
by restricting updates to a predefined whitelist and by avoiding the use of
`eval`, `exec`, or other dynamic code execution mechanisms.
"""

from __future__ import annotations

from typing import Dict, Any, List

# Global whitelist of fields that may be updated.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
]

def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new details.

    Parameters
    ----------
    item : dict
        The original product dictionary. Must contain at least the keys in
        `PERMITTED_FIELDS`. Keys not present will be added if allowed.
    details : dict
        A dictionary of key/value pairs intended to update the product.

    Returns
    -------
    dict
        The updated product dictionary. A shallow copy of the original `item`
        is returned to avoid side‑effects on the caller's data.

    Raises
    ------
    TypeError
        If `item` or `details` is not a dictionary.
    ValueError
        If any key in `details` is not present in the global whitelist.

    Notes
    -----
    The function performs a shallow copy of `item` before applying updates.
    Nested mutable objects are not deeply copied, so callers should be
    aware of potential shared references.

    Examples
    --------
    >>> product = {"price": 10.0, "description": "Old", "stock": 5}
    >>> modify_item_details(product, {"price": 12.0, "stock": 7})
    {'price': 12.0, 'description': 'Old', 'stock': 7}
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary.")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary.")

    # Create a shallow copy to avoid mutating the original item.
    updated_item = dict(item)

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")
        updated_item[key] = value

    return updated_item