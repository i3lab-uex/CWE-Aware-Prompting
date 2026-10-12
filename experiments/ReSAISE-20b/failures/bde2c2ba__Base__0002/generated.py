# update_item_information.py

"""
A secure utility to update product dictionaries with only permitted fields.
"""

from copy import deepcopy
from typing import Dict, Any

# Global list of attributes that may be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_item_information(
    product_info: Dict[str, Any],
    new_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with values from ``new_data`` but only for
    fields listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product_info :
        The original product dictionary. It is not modified in place.
    new_data :
        A dictionary containing potential updates. Keys that are not
        present in :data:`PERMITTED_FIELDS` are ignored.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.

    Raises
    ------
    TypeError
        If either ``product_info`` or ``new_data`` is not a dictionary.
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Work on a copy to avoid side‑effects
    updated_product = deepcopy(product_info)

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value
    return updated_product