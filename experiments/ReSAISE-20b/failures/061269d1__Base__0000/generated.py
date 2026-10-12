# -*- coding: utf-8 -*-
"""
Utility module for safely editing product information.

This module contains the `edit_product_info` function, which updates a
product dictionary in place while strictly enforcing a whitelist of
editable fields.  The function is designed to mitigate CWE‑915 by ensuring
that only explicitly permitted attributes can be modified.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration – the only fields that may be changed
# --------------------------------------------------------------------------- #

PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _is_permitted(field: str) -> bool:
    """
    Determine if a field is allowed to be modified.

    Parameters
    ----------
    field : str
        The attribute name to check.

    Returns
    -------
    bool
        ``True`` if the field is in :data:`PERMITTED_FIELDS`, otherwise
        ``False``.
    """
    return field in PERMITTED_FIELDS

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with only the permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary.  This dictionary is modified in
        place and also returned.
    details : dict
        A mapping of field names to new values that should be applied to
        ``item``.  Only keys present in :data:`PERMITTED_FIELDS` are
        considered; all others are silently ignored.

    Returns
    -------
    dict
        The updated product dictionary (the same object as ``item``).

    Raises
    ------
    TypeError
        If either ``item`` or ``details`` is not a dictionary.
    ValueError
        If any permitted field in ``details`` has an invalid type for that
        attribute.  For example, ``price`` must be a number, ``stock``
        must be an integer, and ``category``/``description`` must be a
        string.  This validation can be extended as needed.

    Notes
    -----
    The function performs a shallow update: nested structures are not
    deep‑merged.  It is intentionally conservative to avoid accidental
    modifications of unrelated fields.

    Examples
    --------
    >>> prod = {'price': 10.0, 'description': 'Old', 'stock': 5}
    >>> edit_product_info(prod, {'price': 12.0, 'stock': 10})
    {'price': 12.0, 'description': 'Old', 'stock': 10}
    >>> edit_product_info(prod, {'price': 15.0, 'color': 'red'})
    # ``color`` is ignored because it is not permitted
    """
    if not isinstance(item, dict):
        raise TypeError(f"item must be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"details must be a dict, got {type(details).__name__}")

    # Validation helpers
    def _validate_value(field: str, value):
        if field == "price":
            if not isinstance(value, (int, float)):
                raise ValueError(f"price must be numeric, got {type(value).__name__}")
        elif field == "stock":
            if not isinstance(value, int):
                raise ValueError(f"stock must be an integer, got {type(value).__name__}")
        elif field in ("description", "category"):
            if not isinstance(value, str):
                raise ValueError(f"{field} must be a string, got {type(value).__name__}")

    # Apply updates
    for key, new_value in details.items():
        if _is_permitted(key):
            _validate_value(key, new_value)
            item[key] = new_value
        else:
            # For security and debugging, we log the ignored attempt.
            # In production code you might use logging instead of print.
            print(f"[edit_product_info] Ignoring unauthorized field: {key!r}")

    return item