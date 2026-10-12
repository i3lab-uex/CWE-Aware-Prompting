# -*- coding: utf-8 -*-
"""
Utility module for updating product dictionaries in a safe manner.
"""

from __future__ import annotations

# List of fields that are allowed to be modified through the public API.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update only the permitted fields of a product dictionary.

    Parameters
    ----------
    item : dict
        The original product representation. It is modified in-place and also
        returned for convenience.
    payload : dict
        Mapping of field names to new values. Only keys that are present in
        :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        The updated product dictionary (identical to ``item``).

    Raises
    ------
    TypeError
        If either argument is not a mapping type.
    ValueError
        If ``payload`` contains keys that are not permitted.

    Notes
    -----
    The function performs an in-place update to avoid unnecessary copying of the
    product object. It also validates that no disallowed fields are present in
    ``payload`` to mitigate accidental exposure of sensitive attributes.
    """
    # Basic type validation
    if not isinstance(item, dict):
        raise TypeError(f"item must be a dict, got {type(item).__name__}")
    if not isinstance(payload, dict):
        raise TypeError(f"payload must be a dict, got {type(payload).__name__}")

    # Identify disallowed keys
    disallowed = set(payload) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify non‑permitted fields: {', '.join(sorted(disallowed))}"
        )

    # Apply permitted updates
    for key in PERMITTED_FIELDS:
        if key in payload:
            item[key] = payload[key]

    return item