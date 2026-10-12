# -*- coding: utf-8 -*-
"""
A small utility module that safely updates product attributes.

The function ``update_item_details`` only allows modifications of a
pre‑defined set of fields (``PERMITTED_FIELDS``).  Any attempt to modify
other attributes raises a ``ValueError``.

This protects against CWE‑915 (Improperly Controlled Modification of
Dynamically-Determined Object Attributes) by ensuring that only
explicitly whitelisted fields can be changed.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
#  Configuration
# --------------------------------------------------------------------------- #

PERMITTED_FIELDS = ["price", "description", "stock", "category"]


# --------------------------------------------------------------------------- #
#  Core functionality
# --------------------------------------------------------------------------- #

def update_item_details(inventory: Dict[str, Any],
                        update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an inventory item's attributes safely.

    Parameters
    ----------
    inventory : dict
        The original product dictionary.  It will be modified in place.
    update_data : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated inventory dictionary.

    Raises
    ------
    TypeError
        If ``inventory`` or ``update_data`` are not dictionaries.
    ValueError
        If any key in ``update_data`` is not in ``PERMITTED_FIELDS``.

    Notes
    -----
    - The function mutates the input dictionary and also returns it for
      convenience.
    - No other keys are added or removed; only permitted ones are updated.

    Examples
    --------
    >>> product = {'price': 10.0, 'description': 'Old', 'stock': 5}
    >>> update_item_details(product, {'price': 12.0, 'stock': 3})
    {'price': 12.0, 'description': 'Old', 'stock': 3}
    """
    # Basic type checks
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    # Validate and apply updates
    for key, value in update_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")
        inventory[key] = value

    return inventory


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to run)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_product = {
        "price": 19.99,
        "description": "A nice widget",
        "stock": 42,
        "category": "gadgets"
    }

    updates = {"price": 17.99, "stock": 40}
    updated_product = update_item_details(sample_product, updates)
    print(updated_product)