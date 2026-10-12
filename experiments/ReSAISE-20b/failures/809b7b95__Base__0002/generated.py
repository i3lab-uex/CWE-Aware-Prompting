#!/usr/bin/env python3
"""
Utility to safely update product attributes.
"""

from typing import Dict, Any

# Only these fields are allowed to be updated
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an item dictionary with new details only for permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary. It may contain any keys.
    details : dict
        A mapping of attribute names to new values.

    Returns
    -------
    dict
        The same dictionary object, updated with permitted fields.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in ``details`` is not a string or if a value is of an unexpected type.
    """
    # Basic input validation
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("details must be a dictionary")

    for key, value in details.items():
        # Ensure the key is a string
        if not isinstance(key, str):
            raise ValueError(f"Field name must be a string: {key!r}")

        # Only update permitted fields
        if key in PERMITTED_FIELDS:
            item[key] = value

    return item