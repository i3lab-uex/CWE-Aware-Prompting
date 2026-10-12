# -*- coding: utf-8 -*-
"""
Safe product information updater.

This module defines a single public function `edit_product_info` which updates
only the fields listed in the global `PERMITTED_FIELDS`.  It performs basic
type checks and avoids accidental modification of protected keys, mitigating
CWE‑913 risks.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Define the list of fields that may be updated.  Add or remove entries as needed.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with permitted fields.

    Parameters
    ----------
    item : dict
        The original product data.  It will be updated in place.
    details : dict
        A mapping of field names to new values.  Only keys present in
        `PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        The updated product dictionary (the same object as ``item``).

    Raises
    ------
    TypeError
        If either argument is not a dictionary, or if any key in ``details``
        is not a string.
    ValueError
        If an attempted update would change the type of a field in an
        unexpected way (e.g., setting ``price`` to a non‑numeric value).
    """
    # Basic type validation
    if not isinstance(item, dict):
        raise TypeError(f"'item' must be a dict; got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"'details' must be a dict; got {type(details).__name__}")

    for key, new_value in details.items():
        # Ensure keys are strings
        if not isinstance(key, str):
            raise TypeError(f"Field names must be strings; got {type(key).__name__}")

        # Skip disallowed fields
        if key not in PERMITTED_FIELDS:
            continue

        # Optional: enforce simple type checks per field
        if key == "price":
            if not isinstance(new_value, (int, float)):
                raise ValueError(f"Invalid type for 'price': expected int or float, got {type(new_value).__name__}")
        elif key == "stock":
            if not isinstance(new_value, int):
                raise ValueError(f"Invalid type for 'stock': expected int, got {type(new_value).__name__}")
        elif key == "description":
            if not isinstance(new_value, str):
                raise ValueError(f"Invalid type for 'description': expected str, got {type(new_value).__name__}")
        elif key == "category":
            if not isinstance(new_value, str):
                raise ValueError(f"Invalid type for 'category': expected str, got {type(new_value).__name__}")

        # Apply the update
        item[key] = new_value

    return item