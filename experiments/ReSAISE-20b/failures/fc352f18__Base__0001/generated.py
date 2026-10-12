#!/usr/bin/env python3
"""
Utility module for safely updating product dictionaries.

The function `amend_product_features` updates only the attributes that are
explicitly allowed by the global list ``PERMITTED_FIELDS``.  Any attempt to
modify a disallowed field raises a :class:`ValueError` to prevent accidental
or malicious changes (CWE‑915).
"""

from __future__ import annotations

from typing import Dict, Any

# Define the list of attributes that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from ``payload`` only for
    fields that are in the global ``PERMITTED_FIELDS`` list.

    Parameters
    ----------
    item : dict
        The original product dictionary.  This dictionary is modified in
        place and also returned for convenience.
    payload : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    ValueError
        If ``payload`` contains a key that is not in ``PERMITTED_FIELDS``.

    Notes
    -----
    The function deliberately rejects any attempt to change a field that is not
    explicitly permitted.  This mitigates the risk of CWE‑915 by ensuring
    that only a known set of attributes can be altered.
    """
    for key, value in payload.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Attempt to modify disallowed field: {key!r}")
        item[key] = value
    return item