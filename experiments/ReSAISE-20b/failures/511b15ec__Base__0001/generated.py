# -*- coding: utf-8 -*-
"""
Utility module for updating product information while guarding against
unauthorized attribute modifications (CWE-915).

Author: OpenAI ChatGPT
"""

from copy import deepcopy
from typing import Dict, Iterable

# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

def update_product_info(prod: Dict[str, any], change_data: Dict[str, any]) -> Dict[str, any]:
    """
    Update a product dictionary with new values from ``change_data``.
    
    Only fields listed in :data:`PERMITTED_FIELDS` may be modified. Any
    attempt to modify an unpermitted field will raise a ``ValueError``.
    
    Parameters
    ----------
    prod : dict
        The original product dictionary.  This is **not** modified in place.
    change_data : dict
        A mapping of field names to new values.  Only permitted fields are applied.
    
    Returns
    -------
    dict
        A new dictionary containing the updated product information.
    
    Raises
    ------
    ValueError
        If ``change_data`` contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    # Create a shallow copy to avoid mutating the caller's dictionary.
    updated_prod = deepcopy(prod)

    for key, value in change_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Attempt to modify unpermitted field: {key!r}")

        # Perform a simple type check if desired (e.g., price must be numeric).
        # This is optional and can be expanded based on business rules.
        if key == "price" and not isinstance(value, (int, float)):
            raise TypeError(f"The 'price' field must be a number, got {type(value).__name__}")

        if key == "stock" and not isinstance(value, int):
            raise TypeError(f"The 'stock' field must be an integer, got {type(value).__name__}")

        # Assign the new value.
        updated_prod[key] = value

    return updated_prod