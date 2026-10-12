# -*- coding: utf-8 -*-
"""
Utility module for safely updating product information.

The `update_product_info` function ensures that only attributes listed in the
global `PERMITTED_FIELDS` can be modified. Any attempt to modify a field not
in that list raises a `ValueError`. This protects against CWE‑915:
Improperly Controlled Modification of Dynamically-Determined Object Attributes.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Only these keys are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values while restricting modifications
    to the fields defined in ``PERMITTED_FIELDS``.

    Parameters
    ----------
    prod : dict
        The original product data.
    change_data : dict
        Mapping of field names to new values.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    ValueError
        If ``change_data`` contains keys that are not in ``PERMITTED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    The function performs an in-place update of ``prod`` and returns the same
    dictionary reference. This is intentional to avoid unnecessary copying.
    """
    # Basic type checks
    if not isinstance(prod, dict):
        raise TypeError(f"Expected prod to be a dict; got {type(prod).__name__}")
    if not isinstance(change_data, dict):
        raise TypeError(f"Expected change_data to be a dict; got {type(change_data).__name__}")

    # Identify disallowed fields
    disallowed = set(change_data) - PERMITTED_FIELDS
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Apply allowed updates
    for key, value in change_data.items():
        prod[key] = value

    return prod


# --------------------------------------------------------------------------- #
# Example usage (uncomment for quick test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    product = {"price": 19.99, "description": "A nice widget", "stock": 10, "category": "Tools"}
    updates = {"price": 17.99, "stock": 8}
    updated_product = update_product_info(product, updates)
    print(updated_product)   # {'price': 17.99, 'description': 'A nice widget', 'stock': 8, 'category': 'Tools'}