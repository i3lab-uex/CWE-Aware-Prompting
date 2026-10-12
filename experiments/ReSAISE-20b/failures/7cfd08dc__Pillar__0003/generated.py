#!/usr/bin/env python3
"""
Utility module for updating product attributes safely.

The function `update_product_attributes` updates a product dictionary only
for fields that are explicitly permitted.  Any attempt to modify disallowed
attributes is silently ignored – this avoids accidental tampering with
critical fields such as identifiers or internal state.

Security considerations:
- The update dictionary is shallow‑merged; nested structures are not
  recursively updated to prevent accidental overwrites of complex objects.
- No external resources are opened or closed, so there is no risk of
  CWE‑664 (improper control of a resource).  The function operates purely
  on in‑memory data structures.

"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Define the set of fields that may be updated.
PERMITTED_FIELDS = {
    "price",
    "description",
    "stock",
    "category",
}

def update_product_attributes(
    item: Dict[str, Any],
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with allowed fields.

    Parameters
    ----------
    item : dict
        The original product data.
    updates : dict
        Dictionary containing desired changes.

    Returns
    -------
    dict
        A new dictionary reflecting the updated product state.  The original
        `item` is left unmodified.

    Notes
    -----
    - Only keys present in ``PERMITTED_FIELDS`` are applied.
    - If a key appears in both `item` and `updates`, the value from
      `updates` replaces that in `item`.
    - The function performs a shallow copy of `item`; nested objects are
      not deeply cloned.
    """
    # Create a shallow copy to avoid mutating the original product
    updated_item = copy.copy(item)

    for key, value in updates.items():
        if key not in PERMITTED_FIELDS:
            # Skip any disallowed field to preserve integrity
            continue

        updated_item[key] = value

    return updated_item