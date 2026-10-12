#!/usr/bin/env python3
"""
Utility module for safely updating product dictionaries.

The `modify_item_details` function applies updates only to attributes
listed in the global ``PERMITTED_FIELDS`` list, preventing accidental
or malicious modification of unintended fields.

CWE-915: Improperly Controlled Modification of Dynamically-Determined
Object Attributes is mitigated by explicit whitelisting.
"""

from __future__ import annotations

from typing import Dict, Any


# Whitelist of attributes that are allowed to be modified
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]


def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from ``details``,
    but only for fields that are explicitly permitted.

    Parameters
    ----------
    item : dict
        The original product dictionary. Must be a mutable mapping.
    details : dict
        Dictionary containing desired updates.

    Returns
    -------
    dict
        A new dictionary with the applied changes. The original ``item``
        remains unmodified.

    Raises
    ------
    TypeError
        If either ``item`` or ``details`` is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError(f"'item' must be a dict; got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"'details' must be a dict; got {type(details).__name__}")

    # Create a shallow copy to avoid mutating the input dictionary
    updated_item = dict(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
        else:
            # Log or ignore silently; here we simply skip.
            pass

    return updated_item