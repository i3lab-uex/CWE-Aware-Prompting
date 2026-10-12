# -*- coding: utf-8 -*-
"""
Utility to safely update product features.

This module defines a single function `amend_product_features` that updates
only the fields listed in the globally defined `PERMITTED_FIELDS`.  It
ensures that no unauthorized keys are added or modified, mitigating
CWE‑664 style resource misuse.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update a product dictionary with values from `payload`, but only for
    keys that are present in PERMITTED_FIELDS.

    Parameters
    ----------
    item : dict
        The original product dictionary.  This object is modified in place.
    payload : dict
        A dictionary containing new values for product fields.

    Returns
    -------
    dict
        The updated product dictionary (same object as `item`).

    Raises
    ------
    TypeError
        If either `item` or `payload` is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError(f"item must be a dict, got {type(item).__name__}")
    if not isinstance(payload, dict):
        raise TypeError(f"payload must be a dict, got {type(payload).__name__}")

    # Update only permitted fields
    for key in PERMITTED_FIELDS:
        if key in payload:
            item[key] = payload[key]

    return item