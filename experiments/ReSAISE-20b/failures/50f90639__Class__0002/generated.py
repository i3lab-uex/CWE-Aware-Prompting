# -*- coding: utf-8 -*-
"""
Utility module for updating product details with strict field validation.
"""

from copy import deepcopy
from typing import Dict, List

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
    # Add other permissible fields here.
]

def modify_product_details(product: Dict, data: Dict) -> Dict:
    """
    Update a product dictionary with new values provided in ``data``.

    Parameters
    ----------
    product : dict
        The original product data. It will not be modified in place.
    data : dict
        A dictionary containing the fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If ``data`` contains a key that is not present in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    * The function performs a shallow copy of ``product`` before applying updates.
      This protects the caller from accidental mutation of the original data.
    * Only keys listed in :data:`PERMITTED_FIELDS` are allowed to be updated.
      All other keys are ignored and a ``ValueError`` is raised to signal misuse.
    """
    # Create a copy so that the original product dict remains unchanged.
    updated_product = deepcopy(product)

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not permitted for update. "
                f"Allowed fields: {PERMITTED_FIELDS}"
            )
        # Optionally, add type or value checks here (e.g., price must be a non‑negative number).
        updated_product[key] = value

    return updated_product