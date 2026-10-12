#!/usr/bin/env python3
"""
Utility module for safely updating product dictionaries.

The `amend_product_features` function updates only the fields that are
explicitly listed in the globally defined `PERMITTED_FIELDS`.  This
prevents accidental or malicious modification of disallowed attributes,
mitigating risks such as CWE‑913 (Improper Control of Dynamically-Managed
Code Resources).

Author: ChatGPT
"""

from __future__ import annotations

from typing import Dict, Iterable, Any

# Define the list of fields that are allowed to be modified.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the given product dictionary with values from `payload` but
    only for keys that are present in PERMITTED_FIELDS.

    Parameters
    ----------
    item : dict
        The product dictionary to be updated. It may contain arbitrary keys.
    payload : dict
        Dictionary containing new values for fields that should be updated.

    Returns
    -------
    dict
        The updated product dictionary. The original `item` is modified in
        place and returned for convenience.

    Raises
    ------
    TypeError
        If either `item` or `payload` is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")

    # Iterate over the intersection of payload keys and permitted fields
    for key in PERMITTED_FIELDS:
        if key in payload:
            # Direct assignment – no dynamic code execution
            item[key] = payload[key]

    return item

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     product = {"price": 10.0, "description": "Old", "stock": 5}
#     update = {"price": 12.0, "description": "New", "category": "Tools"}
#     amended = amend_product_features(product, update)
#     print(amended)  # {'price': 12.0, 'description': 'New', 'stock': 5, 'category': 'Tools'}