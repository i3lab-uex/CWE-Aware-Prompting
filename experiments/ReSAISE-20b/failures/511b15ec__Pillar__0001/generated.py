# -*- coding: utf-8 -*-
"""
Product update module.

This module defines a single public function `update_product_info` that updates
a product dictionary with values from an incoming change payload.  Only the
fields listed in `PERMITTED_FIELDS` are allowed to be modified; attempting to
modify any other key raises a ``ValueError``.  The function mutates the supplied
product dictionary in place and also returns it for convenience.

Security considerations:
- The function performs explicit whitelist validation of keys to avoid
  accidental modification of sensitive or read‑only fields.
- No external resources are opened or closed; the function is pure and
  deterministic, mitigating CWE‑664 (Improper Control of a Resource Through its Lifetime).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

PERMITTED_FIELDS = {
    "price",
    "description",
    "stock",
    "category",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_change_keys(change_data: dict) -> None:
    """
    Ensure that all keys in `change_data` are allowed to be updated.

    Raises:
        ValueError: If any key is not in the PERMITTED_FIELDS set.
    """
    invalid_keys = set(change_data) - PERMITTED_FIELDS
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify forbidden fields: {sorted(invalid_keys)}"
        )

# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def update_product_info(prod: dict, change_data: dict) -> dict:
    """
    Update the supplied product dictionary with values from `change_data`.

    Only keys listed in :data:`PERMITTED_FIELDS` may be updated.  The function
    mutates ``prod`` in place and returns the modified dictionary.

    Args:
        prod: Dictionary representing a product.  Expected keys include
              'price', 'description', 'stock', and 'category'.
        change_data: Dictionary containing new values for fields to be updated.

    Returns:
        The same dictionary instance as ``prod`` but with the permitted fields
        updated.

    Raises:
        ValueError: If `change_data` contains keys that are not permitted.
        TypeError:  If ``prod`` or ``change_data`` is not a dictionary.

    Examples:
        >>> product = {"price": 10.0, "description": "Old", "stock": 5}
        >>> update_product_info(product, {"price": 12.5, "stock": 10})
        {'price': 12.5, 'description': 'Old', 'stock': 10}
    """
    if not isinstance(prod, dict):
        raise TypeError(f"Expected prod to be a dict, got {type(prod).__name__}")
    if not isinstance(change_data, dict):
        raise TypeError(f"Expected change_data to be a dict, got {type(change_data).__name__}")

    # Validate keys before performing any modifications
    _validate_change_keys(change_data)

    # Apply updates atomically (the operation is deterministic and side‑effect free)
    prod.update(change_data)

    return prod

# --------------------------------------------------------------------------- #
# End of module
# --------------------------------------------------------------------------- #