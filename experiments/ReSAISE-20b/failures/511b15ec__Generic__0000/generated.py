#!/usr/bin/env python3
"""
Utility module for product data updates.

The function `update_product_info` ensures that only fields listed in the
global `PERMITTED_FIELDS` constant can be modified.  All other keys are
ignored, and an exception is raised if a disallowed field is supplied.

This module contains no external dependencies beyond the Python standard
library.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from `change_data`.

    Parameters
    ----------
    prod : dict
        The original product data. It is modified in place.
    change_data : dict
        A mapping of fields to new values.

    Returns
    -------
    dict
        The updated product dictionary (the same object as `prod`).

    Raises
    ------
    ValueError
        If `change_data` contains a key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    - Only keys that are present in :data:`PERMITTED_FIELDS` will be updated.
    - Keys not present in `prod` but allowed are added.
    - All other keys in `change_data` trigger a :class:`ValueError`.
    """
    allowed_set = set(PERMITTED_FIELDS)

    # Identify any disallowed keys and raise an error early
    disallowed_keys = [k for k in change_data if k not in allowed_set]
    if disallowed_keys:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed_keys)}"
        )

    # Apply permitted updates
    for key, value in change_data.items():
        prod[key] = value

    return prod


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example product
    product = {
        "id": 123,
        "price": 19.99,
        "description": "A useful widget",
        "stock": 50,
        "category": "Gadgets",
    }

    # New data to apply
    updates = {"price": 17.99, "stock": 45}

    try:
        updated_product = update_product_info(product, updates)
        print("Updated product:", updated_product)
    except ValueError as exc:
        print(f"Error: {exc}")