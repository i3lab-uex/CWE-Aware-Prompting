#!/usr/bin/env python3
"""
Utility to update product information safely.

The module defines a global list `PERMITTED_FIELDS` that specifies which
attributes of a product can be modified.  The function `update_item_details`
creates a new dictionary containing the updated data, leaving the original
inventory untouched.

Security note:
The implementation avoids any dynamic code execution or reflection.  It only
accesses dictionary keys directly, preventing CWE‑913 vulnerabilities.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Only these fields may be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_details(
    inventory: Dict[str, Any],
    update_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new product dictionary with only permitted fields updated.

    Parameters
    ----------
    inventory : dict
        Original product information.
    update_data : dict
        Fields and values intended for update.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.
    """
    # Create a shallow copy to avoid mutating the original inventory
    updated = copy.deepcopy(inventory)

    for key, value in update_data.items():
        if key in PERMITTED_FIELDS:
            updated[key] = value
        else:
            # Silently ignore disallowed fields to prevent accidental injection.
            continue

    return updated