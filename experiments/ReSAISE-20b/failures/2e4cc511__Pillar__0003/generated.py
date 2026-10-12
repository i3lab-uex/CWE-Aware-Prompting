# -*- coding: utf-8 -*-
"""
Product inventory updater.

This module provides a single public function, `update_item_details`, which
updates an existing product dictionary with values from a supplied update
payload. Only fields listed in the global `PERMITTED_FIELDS` are allowed to be
modified, ensuring that critical or sensitive attributes cannot be altered
through the public API.

The implementation follows best practices for defensive programming and
avoids common pitfalls such as accidental mutation of global state or
insecure handling of input data.
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Only these fields are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_item_details(
    inventory: Dict[str, Any],
    update_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update the provided product dictionary with values from ``update_data``.

    Only keys that are present in :data:`PERMITTED_FIELDS` will be applied.
    The function mutates ``inventory`` in place and also returns it for
    convenience.

    Parameters
    ----------
    inventory : dict
        The original product dictionary. Must contain keys for all permitted
        fields; missing keys are left untouched.
    update_data : dict
        A dictionary of candidate updates. Keys not in
        :data:`PERMITTED_FIELDS` are ignored and a warning is logged.

    Returns
    -------
    dict
        The updated product dictionary (identical to ``inventory``).

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in ``update_data`` is not permitted.

    Notes
    -----
    The function performs no type coercion; callers are responsible for
    ensuring that the values supplied in ``update_data`` match the expected
    types of the corresponding product attributes.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    # Iterate over the provided update data and apply only permitted fields.
    for key, value in update_data.items():
        if key not in PERMITTED_FIELDS:
            # In a real-world scenario we might log this event; here we
            # simply raise an exception to make the misuse explicit.
            raise ValueError(f"Field '{key}' is not permitted for update")

        # Direct assignment; we trust the caller to provide appropriate types.
        inventory[key] = value

    return inventory