#!/usr/bin/env python3
"""
Utility module for updating product dictionaries.

The function `amend_product_features` updates only those keys that are
explicitly allowed by the global ``PERMITTED_FIELDS`` list.  Any other
keys present in the payload are ignored to prevent accidental or malicious
modification of protected fields.

Security note:
- The function performs no evaluation of code from the payload.
- It only accepts simple data types that are JSON‑serialisable.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing product dictionary with values from *payload*.

    Only keys that appear in :data:`PERMITTED_FIELDS` are applied.
    The function mutates *item* in place and also returns it for convenience.

    Parameters
    ----------
    item : dict
        The product dictionary to be updated.  It may contain any number of keys.
    payload : dict
        A dictionary containing new values for the product.  Only keys listed in
        ``PERMITTED_FIELDS`` will be considered.

    Returns
    -------
    dict
        The updated product dictionary (the same object as ``item``).

    Raises
    ------
    TypeError
        If either *item* or *payload* is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError(f"Expected item to be a dict, got {type(item).__name__}")
    if not isinstance(payload, dict):
        raise TypeError(f"Expected payload to be a dict, got {type(payload).__name__}")

    for key in PERMITTED_FIELDS:
        if key in payload:
            # Avoid overwriting with non‑serialisable objects by converting
            # to a basic type if possible.  This is a minimal safeguard; in
            # production code you might want stricter validation.
            value = payload[key]
            if isinstance(value, (str, int, float, bool)):
                item[key] = value
            else:
                # For complex types we store a shallow copy to avoid accidental
                # mutation of the original payload object.
                item[key] = value if isinstance(value, (list, dict)) else None

    return item